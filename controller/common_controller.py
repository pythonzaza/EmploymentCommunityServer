from fastapi import APIRouter
from schema_models.user_models import UserRegisterIn

common_router = APIRouter()


@common_router.get("/test")
async def test(string: str):
    return string


@common_router.post("/register")
def register(user: UserRegisterIn):
    return user
