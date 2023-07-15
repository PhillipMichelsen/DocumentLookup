import asyncio


class ResponseUtils:
    def __init__(self):
        self.responses_pending = {}

    async def create_response(self, task_id: str) -> asyncio.Future:
        future = asyncio.Future()
        self.responses_pending[task_id] = future
        return future

    async def update_response(self, task_id: str, response: str):
        self.responses_pending[task_id].set_result(response)

    async def clear_response(self, task_id: str):
        del self.responses_pending[task_id]


# Singleton
response_utils = ResponseUtils()
