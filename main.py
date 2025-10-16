from chat import chat

# Modify the main function as per requirements from README.md
# Below is a simple example of how to use the chat function

def main():

    # Ask user for input and call the chat function
    user_input = input("User: ")

    # Call the chat function with user input
    response = chat( [{"role": "user", "content": user_input}] )

    # Print the AI's response and exit
    print("AI:", response)

if __name__ == '__main__':
    # Launch the main() function if `python main.py` is entered from the terminal
    main()
