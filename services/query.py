class QueryProcessor:
    def __init__(self, chat_api):
        self.chat_api = chat_api

    def optimize_query(self, user_query):
        model_name = "gpt-4o"
        system_message = {
            "role": "system",
            "content": """You are an advanced language model specifically designed to optimize user-provided queries 
            within the strict context of the MoEngage platform. Your task is to improve the quality and clarity of 
            the given query while ensuring that the output aligns solely with MoEngage-related tasks, features, 
            and functionalities.Guidelines: Strictly adhere to the context of the MoEngage platform and its features. 
            Do not include or assume information irrelevant to MoEngage. Do not ask for clarifications, 
            counter questions, or additional context, even if the input is vague or ambiguous. Your job is only to 
            enhance the provided query based on the given information. Focus on optimizing the query for clarity, 
            structure, and alignment with MoEngage’s platform, ensuring it is actionable and precise. Do not make 
            assumptions unless the input provides specific indicators, and always preserve the original intent of the 
            query. Use natural, conversational, and LLM-friendly language in the improved query. Provide the enhanced 
            query only, prefixed with 'Optimized Query:', and do not include explanations or additional commentary. 
            Your sole responsibility is optimizing user-provided queries within the MoEngage platform context for 
            better clarity and usability. Strictly follow these instructions without deviation."""
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
        Structured Steps (if the query involves a detailed procedure or process to be communicated) using the prefix 
        'Steps:', or Concise Explanations (if the query requires brief and clear information about a topic) using the 
        prefix 'Explanation:'. Key Guidelines: Focus strictly on the intent of the query, regardless of tone, 
        wording, phrasing, typos, spelling errors, slang, or informal language. Extract and convey only meaningful, 
        actionable, or informative content aligned with the user’s request. Maintain a consistent structure and 
        formatting to ensure outputs are clear, regardless of how the input is phrased. Avoid: interpreting emotions, 
        opinions, or unrelated requests; adding additional context not explicitly required; or deviating from the 
        intended logic. Ensure that a query expressing the same intent always produces the exact same structured 
        output, no matter the style or variation in input phrasing. Outputs should remain error-free and logically 
        coherent. You must strictly follow the above rules for every response. If a procedure is identified, 
        begin with 'Steps:'; if a topic explanation is identified, begin with 'Explanation:'. Avoid including 
        extraneous details or ambiguities."""
        }
        context_message = {
            "role": "system",
            "content": "This is the full extent of the context available to address the user's query. "
                       "Use this context exclusively to generate your response. If the provided context "
                       "is sufficient to fully understand and answer the query, proceed as instructed while "
                       "adhering strictly to logical accuracy and user intent. If additional context is required "
                       "to produce a complete and precise response, indicate this explicitly and request further "
                       "clarification. Refrain from making assumptions or introducing information not present in the "
                       "provided context. Maintain clarity, precision, and relevance at all times." + context
        }
        messages = [context_message, system_message] + conversation + [{"role": "user", "content": improved_query}]
        return self.chat_api.retry_on_failure(lambda: self.chat_api.send_message(model_name, messages))
