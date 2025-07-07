import pytest
import chat
from unittest.mock import patch, MagicMock
import sys

# Mock the chat function to simply return its argument
def mock_chat(prompt):    
    return str(prompt)

# Helper to simulate input() and capture print()
def run_main_with_inputs(inputs):

    # Store original function
    original_chat = chat.chat
    
    # Replace with mock
    mock_chat_func = MagicMock(side_effect=mock_chat)
    chat.chat = mock_chat_func
        
    output = []
    def fake_input(prompt=None):
        return inputs.pop(0)
    def fake_print(*args, **kwargs):
        output.append(' '.join(str(a) for a in args))
        
    try:
        if 'main' in sys.modules:
            del sys.modules['main']
        with patch('builtins.input', side_effect=fake_input), \
            patch('builtins.print', side_effect=fake_print):
            from main import main
            main()
    finally:
        # Restore original chat function
        chat.chat = original_chat

    return output, mock_chat_func

def test_main_exit():
    # Should print goodbye and exit immediately
    out, _ = run_main_with_inputs(['exit'])
    assert any('Goodbye!' in line for line in out), f"Expected 'Goodbye!' in output, but got: {out}"

def test_main_chat():
    # Should call chat and print AI response, then exit
    out, chat_mock = run_main_with_inputs(['hello', 'exit'])
    
    # Check that chat function was called
    assert chat_mock.called, "Chat function should have been called"
    assert chat_mock.call_count >= 1, "Chat function should have been called at least once"
    
    # Should see the prompt and the AI response
    assert any('hello' in line for line in out), f"Expected 'hello' in output, but got: {out}"
    assert any('Goodbye!' in line for line in out), f"Expected 'Goodbye!' in output, but got: {out}"

def test_main_chat_with_memory():
    # Should call chat and print AI response, then exit
    commands = ['hello', 'test', 'exit']
    out, chat_mock = run_main_with_inputs(commands[:])    
    assert chat_mock.call_count == 2, f"Chat function should have been called twice, but was called {chat_mock.call_count} times"
    # Make sure the entire conversation history is on one of the lines    
    # Use regex to check if all commands are present in the output
    regex = '.*'.join(commands[:-1])  # Exclude 'exit'
    import re
    assert any(re.search(regex, line) for line in out), f"Expected conversation history pattern '{regex}' in output, but got: {out}"
    assert any('Goodbye!' in line for line in out), f"Expected 'Goodbye!' in output, but got: {out}"

def test_main_chat_with_fake_history():
    # Should call chat and print AI response, then exit
    commands = ['hello', 'exit']
    out, chat_mock = run_main_with_inputs(commands[:])    
    assert chat_mock.call_count == 1, "Chat function should have been called once"
    # Make sure we have some additional history after first command
    # we do this by counter the number of the words 'content' in the output
    assert out[0].count('content') > 1, f"Expected more than 1 'content' in first output line, but got {out[0].count('content')} in: {out[0]}"
