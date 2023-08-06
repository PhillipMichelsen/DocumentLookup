from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.listeners.job_response_listener import job_response_callback
from app.listeners.update_result_listener import update_result_callback
from app.routers import core_tasks
from app.utils.pika_utils import pika_utils

# Create FastAPI app, setup logging
app = FastAPI()

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
    await pika_utils.init_connection(
        host=settings.rabbitmq_host,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password
    )

    await pika_utils.declare_exchanges(settings.exchanges_file)

    await pika_utils.register_consumer(
        f'{pika_utils.service_id}_{settings.job_response_queue}',
        f'{pika_utils.service_id}_{settings.job_response_queue_routing_key}',
        job_response_callback
    )

    await pika_utils.register_consumer(
        f'{pika_utils.service_id}_{settings.update_result_queue}',
        f'{pika_utils.service_id}_{settings.update_result_queue_routing_key}',
        update_result_callback
    )

    print(f"Service {pika_utils.service_id} is listening for messages...")


# Root Route
@app.get("/")
def root():
    return {"message": "Working!!"}
