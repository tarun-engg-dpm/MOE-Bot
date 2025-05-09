
class QueryProcessor:
    def __init__(self, chat_api):
        self.chat_api = chat_api

    def optimize_query(self, user_query):
        model_name = "gpt-4o"
        system_message = {
            "role": "system",
            "content": """You are an advanced language model specifically designed to transform structured logical
            conditions into concise, clear, and fluent natural language. Your primary goal is to maintain the original
            intent, logical accuracy, and meaning of the input while ensuring ease of understanding for a human audience."""
        }
        messages = [
            system_message,
            {"role": "user", "content": user_query}
        ]
        return self.chat_api.retry_on_failure(lambda: self.chat_api.send_message(model_name, messages))

    def structuring_query(self, improved_query, conversation, context):
        model_name = "gpt-4o"
        system_message = {
            "role": "system",
            "content": """You are an advanced system tasked with processing user queries by converting them into either:
            Structured Steps (if the query involves a detailed procedure or process to be communicated) or Concise Explanations."""
        }
        context_message = {
            "role": "system",
            "content": "This is the full extent of the context available to address the user's query. " + context
        }
        messages = [context_message, system_message] + conversation + [{"role": "user", "content": improved_query}]
        return self.chat_api.retry_on_failure(lambda: self.chat_api.send_message(model_name, messages))
