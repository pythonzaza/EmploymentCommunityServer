from sqlalchemy.future import Select
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy import select, insert, or_, update
from sqlalchemy.sql.expression import Insert, Update
from datetime import datetime

from configs import EncryptConfig
from common.err import HTTPException, ErrEnum
from common.encrypt import Encrypt
from common.jwt import get_token_key
from common.logger import logger
from common.ip import query_ip
from servers.base_server import BaseServer
from schema_models.user_models import UserRegisterIn, UserLoginIn
from schema_models.common_models import TokenData, IpDetailsModel
from models.user_models import UserModel, UserLoginLogModel


class UserServer(BaseServer):

    async def get_user_by_user_name(self, user: UserRegisterIn) -> UserModel.id:
        """
        根据账号及邮箱查找用户是否存在
        """
        stmt = select([UserModel.id]).where(or_(UserModel.account == user.account, UserModel.email == user.email))

        result = await self.db.execute(stmt)
        user = result.scalars().first()
        return user

    async def register(self, user: UserRegisterIn) -> UserModel:
        """
        注册新用户
        """
        async with self.db.begin():
            old_user = await self.get_user_by_user_name(user)
            if old_user:
                raise HTTPException(status=ErrEnum.User.USER_REPEAT, message="账户已存在", data="账户已存在")

            try:
                user.password = await Encrypt.encrypt_password(user.password)
                new_user = user.dict()
                root_token = await Encrypt.encrypt_password(f'{user.account}-{user.email}')
                new_user.update({
                    "register_ip": self.request.client.host,
                    "register_time": datetime.now(),
                    "token": root_token
                })

                stmt = insert(UserModel).values(**new_user)

                result = await self.db.execute(stmt)
                if result.is_insert:
                    await self.db.commit()
                    new_user["id"] = result.inserted_primary_key[0]
                    new_user = UserModel(**new_user)
                else:
                    logger.error(f"数据写入失败->{stmt}")
                    raise Exception("数据写入失败")
                return new_user

            except Exception as err:
                logger.error(err)
                raise HTTPException(status=ErrEnum.Common.NETWORK_ERR, message="系统异常", data=err)

    async def create_token(self, user: UserModel, platform: str = "web") -> str:
        """
        创建token
        """
        token_data = {
            "user_id": user.id,
            "account": user.account,
            "ip": self.request.client.host,
            "platform": platform,
        }
        token_data = TokenData(**token_data)
        token = await Encrypt.create_token(token_data)
        token_key = await get_token_key(user.id, platform)
        result = await self.redis.set(token_key, 1, ex=EncryptConfig.ACCESS_TOKEN_EXPIRE_SECONDS * 2)
        if result:
            # user.token = token
            return token
        else:
            raise HTTPException(message='Redis写入失败', status=ErrEnum.Common.REDIS_ERR)

    async def _find_user(self, user: UserLoginIn) -> UserModel:
        """
        根据账号或邮箱查找用户
        """
        stmt: Select = select(UserModel).where(
            or_(UserModel.account == user.account, UserModel.email == user.email),
            UserModel.password == user.password)
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status=ErrEnum.User.ACCOUNT_OR_PWD_ERR, message="账号或密码错误")
        return user

    async def login(self, login_user: UserLoginIn, platform: str) -> UserModel:
        """
        登录
        """
        login_user.password = await Encrypt.encrypt_password(login_user.password)
        ip_details = await query_ip(self.request.client.host)

        user = await self._find_user(login_user)

        if user.status == -1:
            await self.write_login_log(user.id, ip_details, is_login=0, remark="账号已被禁用")

            raise HTTPException(status=ErrEnum.User.ACCOUNT_DISABLE, message="账号被禁用")

        new_token = await self.create_token(user=user, platform=platform)

        await self.write_login_log(user.id, ip_details, is_login=1, remark="登录成功")

        user.token = new_token
        return user

    async def get_user_by_id(self, user_id: int) -> UserModel:
        """
        根据id查找用户
        """
        stmt: Select = select(UserModel).where(UserModel.id == user_id, UserModel.status != -1)
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status=ErrEnum.User.USER_NOT_EXIST, message="用户不存在")
        return user

    async def write_login_log(self, user_id: int, ip_data: IpDetailsModel, is_login: int = 1, remark: str = None):
        """
        写用户登录日志
        """
        stmt: Insert = insert(UserLoginLogModel).values(user_id=user_id, login_ip=ip_data.ip, city=ip_data.city,
                                                        coordinates=ip_data.coordinates, is_login=is_login,
                                                        remark=remark)
        result: CursorResult = await self.db.execute(stmt)
        if result.is_insert:
            await self.db.commit()
            log_id = result.inserted_primary_key[0]
            return log_id

    # 更新登录日志
    async def update_login_log(self, log_id: int, is_login: int, remark: str = None):
        """
        更新用户登录日志
        city: str = Column(String)  # 城市,
        coordinates: str = Column(String)  # 坐标
        verify: str = Column(String)  # 验证
        """
        stmt: Update = update(UserLoginLogModel).where(UserLoginLogModel.id == log_id) \
            .values(is_login=is_login, remark=remark)

        res = await self.db.execute(stmt)
        print(res)

    async def update_password(self, new_password: str):
        """
        更新密码
        """
        new_password = await Encrypt.encrypt_password(new_password)
        user_id = self.request.user
        stmt: Update = update(UserModel).where(UserModel.id == user_id).values(password=new_password)
        res: CursorResult = await self.db.execute(stmt)

        return True if res.rowcount else False
