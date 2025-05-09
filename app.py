from services.chat import ChatApplication
from services.history import ChatHistory
from services.openai import ChatAPI
from services.query import QueryProcessor

if __name__ == "__main__":
    api_url = "https://openweb-ui.moengage.ai/api/chat/completions"
    api_key = "sk-ffdbf96f654f405b8511165aac6bce72"

    chat_api = ChatAPI(api_url, api_key)
    chat_history = ChatHistory()
    query_processor = QueryProcessor(chat_api)
    app = ChatApplication(chat_api, chat_history, query_processor)
    app.main_menu()
