from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import embedding_service_router, file_service_router
from app.utils.pika_helper_gateway import pika_handler

app = FastAPI()

# Add routers
app.include_router(embedding_service_router.router, prefix="/embedding", tags=["embedding"])
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
    print("Starting!!!")

    await pika_handler.init_connection()


# Root route
@app.get("/")
def root():
    return {"message": "Working!!"}
