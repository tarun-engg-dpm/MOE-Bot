from services.chat import ChatApplication
from services.history import ChatHistory
from services.openai import ChatAPI
from services.query import QueryProcessor
from services.seg_ai_chat import SegAIChat

if __name__ == "__main__":
    api_url = "https://openweb-ui.moengage.ai/api/chat/completions"
    api_key = "sk-3fb98a5d15cf4797a96256d2ada05c0e"

    chat_api = ChatAPI(api_url, api_key)
    chat_history = ChatHistory()
    query_processor = QueryProcessor(chat_api)
    seg_ai_chat = SegAIChat('DS_Staging')
    app = ChatApplication(chat_api, chat_history, query_processor, seg_ai_chat)
    app.main_menu()
