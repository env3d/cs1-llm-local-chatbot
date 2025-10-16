from chat import chat

def main():
    while True:
        # Get input from the user
        user_input = input("You: ")
        
        # Check if the user wants to exit
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Build the prompt for the chat function
        prompt = [
            {"role": "user", "content": user_input}
        ]

        # Call the chat function with the prompt
        response = chat(prompt)

        # Print the response from the AI
        print("AI:", response)

if __name__ == '__main__':
    main()
