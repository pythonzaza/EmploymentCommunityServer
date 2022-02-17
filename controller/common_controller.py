from fastapi import APIRouter

common_router = APIRouter()


@common_router.get("/index")
def index():
    return {}
