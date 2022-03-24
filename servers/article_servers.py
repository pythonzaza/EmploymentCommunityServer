from typing import Union
from sqlalchemy import select, insert, update
from sqlalchemy.engine.result import ChunkedIteratorResult

from common.err import HTTPException, ErrEnum
from servers.base_server import BaseServer
from schema_models.article_models.article_models import CreateArticleModel
from models.article_models import ArticleListModel, ArticleTypeModel


class ArticleServer(BaseServer):

    async def get_article_type_by_id(self, type_id) -> Union[ArticleTypeModel, HTTPException]:
        """
        根据文章分类id查询文章分类
        """
        smtp = select(ArticleTypeModel).where(ArticleTypeModel.id == type_id)
        result: ChunkedIteratorResult = await self.db.execute(smtp)
        article_type = result.scalars().first()
        if not article_type:
            return HTTPException(status=ErrEnum.Article.TYPE_NOT_EXIST, message="分类不存在")
        return article_type

    async def create(self, new_article: CreateArticleModel):
        """
        创建文章
        """
        article_type = await self.get_article_type_by_id(new_article.type_id)
        new_article_dict = {}

    async def update(self):
        """
        修改文章
        """
        pass

    async def delete(self):
        """
        删除文章
        """
        pass

    async def reply(self):
        """
        回复文章
        """
        pass

    async def comments_article(self):
        """
        评论文章
        """
        pass

    async def comments_reply(self):
        """
        评论回复
        """
        pass
