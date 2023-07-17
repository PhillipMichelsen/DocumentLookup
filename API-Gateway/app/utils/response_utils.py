import asyncio


class ResponseUtils:
    def __init__(self):
        self.responses_pending = {}

    async def create_response(self, task_id: str) -> asyncio.Future:
        """Creates a response future for a given task_id

        :param task_id:
        :return: The response future
        """
        future = asyncio.Future()
        self.responses_pending[task_id] = future
        return future

    async def update_response(self, task_id: str, response: str) -> None:
        """Updates the response future for a given task_id

        :param task_id:
        :param response:
        """
        self.responses_pending[task_id].set_result(response)

    async def clear_response(self, task_id: str) -> None:
        """Clears the response future for a given task_id

        :param task_id:
        """
        del self.responses_pending[task_id]


# Singleton
response_utils = ResponseUtils()
