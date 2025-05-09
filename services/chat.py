from services.user_query_context import UserQueryContext


class ChatApplication:
    def __init__(self, chat_api, chat_history, query_processor, seg_ai_chat):
        self.chat_api = chat_api
        self.chat_history = chat_history
        self.query_processor = query_processor
        self.seg_ai_chat = seg_ai_chat

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
            structured_output = self.query_processor.structuring_query(
                improved_query,
                conversation,
                context=UserQueryContext().get_query_context(improved_query, 5)
            )
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

            structured_output = self.query_processor.structuring_query(
                improved_query,
                conversation,
                context=UserQueryContext().get_query_context(improved_query, 5)
            )
            if not structured_output:
                print("\n[S1] Failed to get structured response after retries. Moving to the next interaction.")
                continue

            conversation.append({"role": "user", "content": improved_query})
            conversation.append({"role": "assistant", "content": structured_output})
            loaded_data.append({"Improved Query": improved_query, "Structured Output": structured_output})

    def new_seg_ai_conversation(self):
        print("Starting a new SegAI conversation. Type 'exit' to end.")
        print("Sample prompts: ")
        sample_prompts_dict = self.seg_ai_chat.get_sample_prompts().get("sample-prompts", {})
        indexed_prompts = {}
        num_prompts = len(sample_prompts_dict)
        i = 1
        for key, value in sample_prompts_dict.items():
            print(f"{i}. {value}")
            indexed_prompts[str(i)] = value  # Store the mapping of number to key
            i += 1
        print(f"{i}. Custom prompt")
        while True:
            print(f"Enter a number to select a sample prompt or {i} for custom prompt , anything else to exit.")
            user_input = input("Enter your choice: ")
            if user_input in indexed_prompts or user_input == f"{i}":
                if user_input in indexed_prompts:
                    selected_prompt = indexed_prompts[user_input]
                else:
                    selected_prompt = input("Enter your custom prompt: ")
                prompt_filter = self.seg_ai_chat.generate_filter(selected_prompt, regenerate=False)
                print(prompt_filter)
                while True:
                    regenerate = input("Do you want to regenerate the filter? (y/n)")
                    if regenerate.lower() == 'y':
                        prompt_filter = self.seg_ai_chat.generate_filter(selected_prompt, regenerate=True)
                        print(prompt_filter)
                    else:
                        break
            else:
                print("Ending SegAI conversation.")
                break

    def main_menu(self):
        while True:
            print("\n--- Modular Chat Application Menu ---")
            print("1. Start a new conversation.")
            print("2. Continue a saved conversation.")
            print("3. View saved conversations.")
            print("4. Generate segmentation filters.")
            print("5. Exit.")
            choice = input("Select an option: ")

            if choice == "1":
                self.new_conversation()
            elif choice == "2":
                self.continue_conversation()
            elif choice == "3":
                self.chat_history.list_histories()
            elif choice == "4":
                self.new_seg_ai_conversation()
            else:
                print("Exiting the application. Goodbye!")
                break