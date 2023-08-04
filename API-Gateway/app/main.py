from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.listeners.job_response_listener import job_response_callback
from app.routers import core_tasks
from app.utils.pika_utils import pika_helper

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
    await pika_helper.init_connection(
        host=settings.rabbitmq_host,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password
    )

    await pika_helper.declare_exchanges(
        service_exchange=settings.service_exchange,
        task_orchestration_exchange=settings.task_orchestrator_exchange
    )

    await pika_helper.declare_queues(
        task_request_queue=settings.task_orchestrator_request_queue,
        task_request_routing_key=settings.task_orchestrator_request_routing_key
    )

    await pika_helper.response_queue.consume(job_response_callback)


# Root Route
@app.get("/")
def root():
    return {"message": "Working!!"}
