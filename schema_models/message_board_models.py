from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from fastapi import Query

from schema_models.base_model import RespModel


class CreateMessageModel(BaseModel):
    """
    新建留言
    """

    enterprise_id: int = Field(..., description="企业id")
    reply_message_id: Optional[int] = Field(None, description="被回复消息id,新留言不填")
    message: str = Field(..., description="留言内容")


class CreateMessageOutModel(RespModel):
    data: Optional[int] = Field(None, description="创建成功")


class MessageDetailsModel(CreateMessageModel):
    """
    留言详情
    """
    # reply_user_id: Optional[int] = Field(None, description="被回复用户id")
    id: int = Field(..., description="被回复用户名")
    reply_user_name: Optional[str] = Field(None, description="被回复用户名")
    reply_message_id: Optional[int] = Field(None, description="被回复消息id")
    user_name: str = Field(..., description="用户名")
    comment_number: int = Field(..., description="回复次数,暂未启用")
    like_number: int = Field(..., description="点赞次数,暂未启用")
    create_time: datetime = Field(..., description="创建时间")

    class Config:
        orm_mode = True


class MessageOutListModel(RespModel):
    data: List[MessageDetailsModel] = Field([], description="留言列表, 可能为空")
