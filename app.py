from services.chat import ChatApplication
from services.history import ChatHistory
from services.openai import ChatAPI
from services.query import QueryProcessor

if __name__ == "__main__":
    api_url = "https://openweb-ui.moengage.ai/api/chat/completions"
    api_key = "sk-3fb98a5d15cf4797a96256d2ada05c0e"

    chat_api = ChatAPI(api_url, api_key)
    chat_history = ChatHistory()
    query_processor = QueryProcessor(chat_api)
    app = ChatApplication(chat_api, chat_history, query_processor)
    app.main_menu()
