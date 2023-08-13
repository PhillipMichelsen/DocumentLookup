from fastapi import APIRouter

router = APIRouter()


@router.get(path="/health-check",
            name="Health Check",
            description="Provides a health check for a service",
            # response_model=
            )
async def route_health_check():
    # TODO: Implement health check (LATER)
    raise NotImplementedError
