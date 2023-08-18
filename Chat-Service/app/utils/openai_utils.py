import openai
from app.config import settings
from typing import List


class OpenAIUtils:
    def __init__(self):
        openai.api_key = settings.openai_api_key

    @staticmethod
    def form_messages(query: str, context: List[str]) -> List[dict]:
        context_paragraphs = "\n".join(f"[{i + 1}] {paragraph}" for i, paragraph in enumerate(context))
        messages = [
            {
                "role": "system",
                "content":
                    "You are a question-answering bot skilled at interpreting context paragraphs to answer queries. "
                    "But are also well versed in answering questions based on your own knowledge should there be a small piece of information missing."
                    "Answer the query using the provided context. Cite relevant paragraphs by denoting the number in brackets (e.g., [1]). "
                    "Assume the user has no knowledge of the context. Use a maximum of 2-3 citations per sentence. Quote if necessary. "
                    "If the information is insufficient, respond with 'I wasn't able to answer the question with the paragraphs provided.' "
                    "Though ensure that if the information was insufficient you dont provide an answer."
                    "Utilize Github-flavored Markdown for readability. Use bold subheadings, line breaks, and other markdown formatting for a visually appealing response."
            },
            {
                "role": "user",
                "content": f"###\nContext:\n{context_paragraphs}\n###\nQuery:\n{query}"
            }
        ]
        return messages

    @staticmethod
    def chat_completion(messages: List[dict]) -> str:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
        response = completion.choices[0].message.content
        print(completion.usage, flush=True)

        return response


openai_utils = OpenAIUtils()

