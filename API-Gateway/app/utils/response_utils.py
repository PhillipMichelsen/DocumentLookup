import asyncio


class ResponseUtils:
    def __init__(self):
        self.responses_pending = {}

    async def create_response(self, job_id: str) -> asyncio.Future:
        """Creates a response future for a given task_id

        :param job_id:
        :return: The response future
        """
        future = asyncio.Future()
        self.responses_pending[job_id] = future
        return future

    async def update_response(self, job_id: str, response: str) -> None:
        """Updates the response future for a given task_id

        :param job_id:
        :param response:
        """
        self.responses_pending[job_id].set_result(response)

    async def clear_response(self, job_id: str) -> None:
        """Clears the response future for a given job_id

        :param job_id:
        """
        del self.responses_pending[job_id]


# Singleton
response_utils = ResponseUtils()
