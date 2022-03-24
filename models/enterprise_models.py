from typing import Optional, Union
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class EnterPriseModel(Base):
    __tablename__ = "enterprises"
    id: int = Column(Integer, primary_key=True, autoincrement=True)  # 公司id
    name: Union[str, Column] = Column(String)  # 公司名称
    legal_person: str = Column(String, )  # 公司法人
    address: str = Column(String)  # 公司地址
    details: str = Column(String)  # 公司详情
    code: Optional[str] = Column(String, default=None)  # 公司统一社会信用码,可在天眼查查询
    TYX_url: str = Column(String, default="")  # 天眼查中的公司链接
    create_time: datetime = Column(DATETIME, default=func.now())  # 天眼查中的公司链接
    create_user_id: int = Column(Integer, default=None)
    update_time: datetime = Column(DATETIME, default=func.now())  # 天眼查中的公司链接
    status: int = Column(Integer, default=1)  # 状态, 1正常, -1删除
