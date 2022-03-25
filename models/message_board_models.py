from typing import Optional, Union
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class MessageBoardModel(Base):
    """
    留言板
    """
    __tablename__ = "message_board"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    enterprise_id: int = Column(Integer)  # 企业ID
    reply_message_id: int = Column(Integer)  # 回复留言id
    reply_user_id: int = Column(Integer)  # 被回复用户id
    reply_user_name: str = Column(Integer, default="")  # 被回复用户名
    user_id: int = Column(Integer)  # 回用户id
    user_name: str = Column(String)  # 回复用户名
    message: str = Column(String)  # 留言内容
    comment_number: int = Column(Integer, default=0)  # 回复次数
    like_number: int = Column(Integer, default=0)  # 点赞次数
    create_time: datetime = Column(DATETIME, default=func.now())  # 创建时间
    status: int = Column(Integer, default=1)  # 状态 1正常 -1删除
    # last_time = Column(DATETIME, default=func.now())  # 最后回复时间
