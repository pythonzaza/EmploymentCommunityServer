from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class UserModel(Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    account: str = Column(String)
    password: str = Column(String)
    email: str = Column(String)
    token: str = Column(String, server_default="")
    register_time: DATETIME = Column(DATETIME, server_default=func.now())
    register_ip: str = Column(String)
