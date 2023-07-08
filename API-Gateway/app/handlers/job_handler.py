from app.utils.task_utils import job_executor


async def handle_job(message, headers):
    task_id = message["task_id"]
    await job_executor.execute_job(task_id, headers)
