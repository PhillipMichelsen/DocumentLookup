from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import file_service_router
from app.utils.pika_utils import pika_helper
from app.utils.task_utils import task_helper

app = FastAPI()

# Add routers
app.include_router(file_service_router.router, prefix="/files", tags=["files"])

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
    await pika_helper.load_exchanges()
    await pika_helper.load_queues()

    await task_helper.load_tasks_yaml()


# Root route
@app.get("/")
def root():
    return {"message": "Working!!"}
