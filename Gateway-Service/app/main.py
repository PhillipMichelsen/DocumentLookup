import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.listeners.job_listener import job_callback
from app.listeners.response_listener import response_callback
from app.routers import core_tasks
from app.utils.pika_async_utils import pika_helper
from app.utils.task_utils import task_helper, task_redis

# Create FastAPI app, setup logging
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Routers
app.include_router(core_tasks.router, prefix="/core-tasks", tags=["core-tasks"])

# Middleware
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
    logging.info('Starting up...')

    await pika_helper.init_connection()
    await task_redis.connect_redis()
    await task_helper.load_tasks_yaml()

    await pika_helper.declare_exchanges()
    await pika_helper.declare_queues()

    await pika_helper.service_queues['job_queue'].consume(job_callback)
    await pika_helper.service_queues[f'{pika_helper.service_id}_job_queue'].consume(job_callback)
    await pika_helper.service_queues['response_queue'].consume(response_callback)
    await pika_helper.service_queues[f'{pika_helper.service_id}_response_queue'].consume(job_callback)

    logging.info('***** Started up! *****')


# Root Route
@app.get("/")
def root():
    return {"message": "Working!!"}
