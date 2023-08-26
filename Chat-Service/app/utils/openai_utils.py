import json

import openai
from app.config import settings
from typing import List, Tuple


class OpenAIUtils:
    def __init__(self):
        openai.api_key = settings.openai_api_key

    @staticmethod
    def form_messages(query: str) -> List[dict]:
        messages = [
            {
                "role": "system",
                "content":
                    "You are a question-answering bot which makes a function call to request context to answer the question. Phrase context requests as questions."
                    "As soon as you have enough context to answer the question, answer it. Do not make more than 5 context requests."
                    "Answer the question only using the provided context. Cite relevant paragraphs at the end of a sentence like so: '[1].'."
                    "If you are unable to answer the question after several context requests, inform the user that you are unable to answer the question"
                    "Utilize Github-flavored Markdown for readability and a visually appealing response."
            },
            {
                "role": "user",
                "content": f"Question:\n{query}"
            }
        ]
        return messages

    @staticmethod
    def add_messages(messages: List[dict], context: List[str]) -> List[dict]:
        context_paragraphs = "\n".join(f"[{i + 1}] {paragraph}" for i, paragraph in enumerate(context))
        messages.append(
            {
                "role": "user",
                "content": f"###\nRequested Context:\n{context_paragraphs}"
            }
        )
        return messages

    @staticmethod
    def chat_completion(messages: List[dict]) -> Tuple[str, bool]:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            functions=[
                {
                    "name": "retrieve_context",
                    "description": "Retrieves the 2 most relevant context paragraphs for a given question.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "context_query": {
                                "type": "string",
                                "description": "The query to retrieve context for. Best phrased as a question as a QA embedding model is used."
                            }
                        },
                        "required": ["context_query"]
                    }
                }
            ],
            function_call="auto"
        )
        # print(completion.usage, flush=True)

        completion_message = completion.choices[0].message

        if completion_message.get('function_call'):
            function_arguments = json.loads(completion_message.function_call.arguments)
            return function_arguments['context_query'], True
        else:
            return completion_message.content, False


openai_utils = OpenAIUtils()

