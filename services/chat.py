class ChatApplication:
    def __init__(self, chat_api, chat_history, query_processor):
        self.chat_api = chat_api
        self.chat_history = chat_history
        self.query_processor = query_processor

    def new_conversation(self):
        print("Starting a new modular conversation. Type 'exit' to end.")
        conversation = []
        history = []

        while True:
            user_query = input("\nYou: ")
            if user_query.lower() in ["exit", "quit"]:
                self.chat_history.save_history(history)
                print("Exiting the conversation.")
                break

            print("\n[Processing query with S0 to improve its quality...]")
            improved_query = self.query_processor.optimize_query(user_query)
            if not improved_query:
                print("\n[S0] Failed to improve query after retries. Moving to the next interaction.")
                continue
            print(f"\nS0 Improved Query: {improved_query}")

            print("\n[Processing improved query with S1 for a structured response...]")
            structured_output = self.query_processor.structuring_query(improved_query, conversation, context="") # ADD Context
            if not structured_output:
                print("\n[S1] Failed to generate structured response after retries. Moving to the next interaction.")
                continue
            print(f"\nS1 Structured Output:\n{structured_output}")

            conversation.append({"role": "user", "content": improved_query})
            conversation.append({"role": "assistant", "content": structured_output})
            history.append({"Improved Query": improved_query, "Structured Output": structured_output})

    def continue_conversation(self):
        files = self.chat_history.list_histories()
        if not files:
            return
        choice = int(input("\nEnter the number of the conversation to continue: ")) - 1
        loaded_data = self.chat_history.load_history(files[choice])

        conversation = []
        for item in loaded_data:
            conversation.append({"role": "user", "content": item["Improved Query"]})
            conversation.append({"role": "assistant", "content": item["Structured Output"]})

        print("Continuing the conversation. Type 'exit' to end.")
        while True:
            user_query = input("\nYou: ")
            if user_query.lower() in ["exit", "quit"]:
                self.chat_history.save_history(loaded_data)
                print("Exiting the conversation.")
                break

            improved_query = self.query_processor.optimize_query(user_query)
            if not improved_query:
                print("\n[S0] Failed to improve the query after retries. Moving to the next interaction.")
                continue

            structured_output = self.query_processor.structuring_query(improved_query, conversation, context="")#ADD context
            if not structured_output:
                print("\n[S1] Failed to get structured response after retries. Moving to the next interaction.")
                continue

            conversation.append({"role": "user", "content": improved_query})
            conversation.append({"role": "assistant", "content": structured_output})
            loaded_data.append({"Improved Query": improved_query, "Structured Output": structured_output})

    def main_menu(self):
        while True:
            print("\n--- Modular Chat Application Menu ---")
            print("1. Start a new conversation")
            print("2. Continue a saved conversation")
            print("3. View saved conversations")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.new_conversation()
            elif choice == "2":
                self.continue_conversation()
            elif choice == "3":
                self.chat_history.list_histories()
            elif choice == "4":
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")