from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from schema_models.base_model import RespModel


class CreateArticleModel(BaseModel):
    type_id: int = Field(..., description="分类ID")  # 分类
    # type_name: int = Field(...,description="分类名称")  # 分类
    title: str = Field(..., description="文章标题")  # 标题
    subtitle: str = Field(..., description="副标题")  # 副标题
    content: str = Field(..., description="正文")  # 正文
    # user_id: str = Field(..., description="")  # 作者
    # create_time: datetime = Field(...,description="")  # 创建时间


class AuthorInfo(BaseModel):
    id: int = Field(..., description="作者用户id", alias="author_id")
    name: str = Field(..., description="作者昵称", alias="author_name")
    account: str = Field(..., description="作者账号", alias="author_account")
    # email: str = Field(..., description="作者邮箱", alias="author_email")


class ArticleDetailsModel(BaseModel):
    id: int = Field(..., description="文章id")
    type_id: int = Field(..., description="分类ID")  # 分类
    # type_name: int = Field(...,description="分类名称")  # 分类
    title: str = Field(..., description="文章标题")  # 标题
    subtitle: str = Field(..., description="副标题")  # 副标题
    content: str = Field(..., description="文章正文")  # 正文
    author_info: Optional[AuthorInfo] = Field(None, description="作者资料")  # 作者

    create_time: datetime = Field(..., description="")  # 创建时间

    praise: str = Field(0, description="点赞数")  # 点赞
    read: str = Field(0, description="阅读数")  # 阅读
    last_reply_time: Optional[str] = Field(..., description="最后回复时间")  # 最后回复时间
    recommended: int = Field(..., description="推荐")
    status: int = Field(0, description="文章状态,1 正常,-1 封禁")


class ArticleDetailsOutModel(RespModel):
    data: ArticleDetailsModel
