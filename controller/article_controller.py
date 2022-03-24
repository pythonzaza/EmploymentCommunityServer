from fastapi import APIRouter, Request, Depends

from schema_models.article_models.article_models import (
    CreateArticleModel, ArticleDetailsOutModel
)
from common.depends import jwt_auth
from servers.article_servers import ArticleServer

article_router = APIRouter()


@article_router.post("create", response_model=ArticleDetailsOutModel)
async def create_article(request: Request, new_article: CreateArticleModel, user_id=Depends(jwt_auth)):
    article_server = ArticleServer(request)

    return {}
