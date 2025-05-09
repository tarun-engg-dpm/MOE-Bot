import os
import json
from colorama import Fore, init

init(autoreset=True)

class ChatHistory:
    def __init__(self, history_dir="chat_history"):
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def save_history(self, history):
        filename = input("\nEnter a filename to save this conversation (e.g., 'chat1.json'): ")
        filepath = os.path.join(self.history_dir, filename)
        with open(filepath, "w") as f:
            json.dump(history, f, indent=4)
        print(f"Conversation saved to {filepath}.")

    def list_histories(self):
        files = [f for f in os.listdir(self.history_dir) if f.endswith(".json")]
        if not files:
            print("No saved conversations found.")
        else:
            print("\nSaved Conversations:")
            for i, file in enumerate(files, 1):
                print(Fore.BLUE + f"{i}. {file}")
        return files

    def load_history(self, filename):
        filepath = os.path.join(self.history_dir, filename)
        with open(filepath, "r") as f:
            return json.load(f)
