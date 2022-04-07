from typing import Optional, Union
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class EnterpriseModel(Base):
    __tablename__ = "enterprises"
    id: int = Column(Integer, primary_key=True, autoincrement=True)  # 公司id
    name: Union[str, Column] = Column(String)  # 公司名称
    legal_person: str = Column(String, )  # 公司法人
    address: str = Column(String)  # 公司地址
    details: str = Column(String)  # 公司详情
    code: Optional[str] = Column(String, default=None)  # 公司统一社会信用码,可在天眼查查询
    TYX_url: str = Column(String, default="")  # 天眼查中的公司链接
    create_time: datetime = Column(DATETIME, default=func.now())  # 创建时间
    create_user_id: int = Column(Integer, default=None)
    update_time: datetime = Column(DATETIME, default=func.now())  # 资料更新时间
    message_count: int = Column(Integer, default=0)  # 留言数量
    status: int = Column(Integer, default=1)  # 状态, 1正常, -1删除


class EnterpriseLog(Base):
    __tablename__ = "enterprises_log"
    id: int = Column(Integer, primary_key=True, autoincrement=True)  # 日志id
    enterprise_id = Column(Integer)  # 企业id
    user_id: int = Column(Integer)  # 操作用户
    data: str = Column(String)  # 修改后的内容
    create_time: datetime = Column(DATETIME, default=func.now())  # 创建时间
