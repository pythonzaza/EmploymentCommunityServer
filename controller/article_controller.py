from fastapi import APIRouter, Request

from schema_models.article_models.article_models import (
    CreateArticleModel, ArticleDetailsOutModel
)

article_router = APIRouter()


@article_router.post("create", response_model=ArticleDetailsOutModel)
async def create_article(new_article: CreateArticleModel):
    return {}
