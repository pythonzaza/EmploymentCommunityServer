from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class UserModel(Base):
    """
    User Model
    """
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True, autoincrement=True)  # id
    name: str = Column(String)  # 昵称
    account: str = Column(String)  # 账号
    password: str = Column(String)  # 密码
    email: str = Column(String)  # 邮箱
    token: str = Column(String, server_default="")  # 根token
    register_time: DATETIME = Column(DATETIME, server_default=func.now())  # 注册时间
    register_ip: str = Column(String)  # 注册ip
    status: int = Column(Integer, default=1)  # 用户状态 1正常,-1禁用


class UserLoginLogModel(Base):
    """
    User Login Log Model
    """
    __tablename__ = "user_login_log"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer)  # 用户id
    login_ip: str = Column(String)  # 登录ip
    city: str = Column(String)  # 城市,
    coordinates: str = Column(String)  # 坐标
    is_login: int = Column(Integer, default=0)  # 是否登录成功 1登录 0未登录
    remark: str = Column(String, default="")  # 备注
    verify: str = Column(String, default="")  # 验证
    create_time: DATETIME = Column(DATETIME, server_default=func.now())  # 登录时间
