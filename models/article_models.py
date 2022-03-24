from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy import func

from common.db import Base


class ArticleTypeModel(Base):
    __tablename__ = "article_type"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    type_name: str = Column(String)
    type_description: str = Column(String)
    create_time: DATETIME = Column(DATETIME, server_default=func.now())  # 创建时间
    update_time: DATETIME = Column(DATETIME, server_default=func.now())  # 修改时间


class ArticleListModel(Base):
    __tablename__ = "article_list"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    type_id: int = Column(Integer)  # 分类
    type_name: int = Column(String)  # 分类
    title: str = Column(String)  # 标题
    subtitle: str = Column(String)  # 副标题
    content: str = Column(String)  # 正文
    user_id: str = Column(String)  # 作者
    create_time: DATETIME = Column(DATETIME, server_default=func.now())  # 创建时间
    praise: int = Column(Integer, default=0)  # 点赞
    # read: int = Column(Integer, server_default=0)  # 阅读
    # last_reply_time: str = Column(DATETIME, server_default=func.now())  # 最后回复时间
    # recommended: int = Column(Integer, server_default=0)  # 推荐
    # status: int = Column(Integer, server_default=1)  # 状态
