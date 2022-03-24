from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class UserModel(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)  # id
    name: str = Column(String)  # 昵称
    account: str = Column(String)  # 账号
    password: str = Column(String)  # 密码
    email: str = Column(String)  # 邮箱
    token: str = Column(String, server_default="")  # 根token
    register_time: DATETIME = Column(DATETIME, server_default=func.now())  # 注册时间
    register_ip: str = Column(String)  # 注册ip
    status: int = Column(Integer, default=1)  # 用户状态 1正常,-1禁用
