from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utils.pika_async_utils import pika_helper
from app.utils.task_utils import task_helper, task_redis, job_executor
from app.routers import core_tasks
from app.listeners.job_listener import job_callback
from app.listeners.response_listener import response_callback


app = FastAPI()

# Add routers
app.include_router(core_tasks.router, prefix="/core-tasks", tags=["core-tasks"])

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup():
    await pika_helper.init_connection()
    task_redis.connect_redis()
    task_helper.load_tasks_yaml()

    await pika_helper.declare_exchanges()
    await pika_helper.declare_queues()

    await pika_helper.service_queues['job_queue'].consume(job_callback)
    await pika_helper.service_queues['response_queue'].consume(response_callback)

    print("Startup complete", flush=True)


# Root route
@app.get("/")
def root():
    return {"message": "Working!!"}
