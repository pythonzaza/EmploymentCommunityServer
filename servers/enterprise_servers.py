from servers.base_server import BaseServer
from sqlalchemy import insert, update, select, or_, func
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm import selectinload

from common.err import HTTPException, ErrEnum
from schema_models.enterprise_models import CreateEnterPriseModel, UpdateEnterPriseModel
from models.enterprise_models import EnterPriseModel


class EnterPriseServer(BaseServer):

    async def check_enterprise(self, new_enterprise: CreateEnterPriseModel):
        """
        检查企业是否存在
        """
        if new_enterprise.code is not None:
            stmt = select(EnterPriseModel).where(or_(EnterPriseModel.name == new_enterprise.name,
                                                     EnterPriseModel.code == new_enterprise.code),
                                                 EnterPriseModel.status != -1)
        else:
            stmt = select(EnterPriseModel).where(EnterPriseModel.name == new_enterprise.name,
                                                 EnterPriseModel.status != -1)

        result: ChunkedIteratorResult = await self.db.execute(stmt)

        enterprise = result.scalars().first()
        if enterprise:
            raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_EXIST, message="企业已存在")

    async def create_enterprise(self, new_enterprise: CreateEnterPriseModel) -> EnterPriseModel:
        """
        创建新企业
        """
        # async with self.db.begin():
        await self.check_enterprise(new_enterprise)

        try:
            # _new_enterprise = EnterPriseModel(create_user_id=self.request.user, **new_enterprise.dict())
            # self.db.add(_new_enterprise)
            insert_stmt = insert(EnterPriseModel).values(create_user_id=self.request.user, **new_enterprise.dict())
            result: CursorResult = await self.db.execute(insert_stmt)
            if result.is_insert:
                await self.db.commit()
            else:
                raise HTTPException(status=ErrEnum.Common.NETWORK_ERR, message="网络异常")
            select_stmt = select(EnterPriseModel).where(EnterPriseModel.id == result.lastrowid)
            result: ChunkedIteratorResult = await self.db.execute(select_stmt)
            _new_enterprise = result.scalars().first()

            return _new_enterprise
        except Exception as err:
            raise HTTPException(status=ErrEnum.Common.NETWORK_ERR, message="网络异常", data=str(err))

    async def get_enterprise_list(self, key: str, page_index: int, page_size: int):
        """
        根据code精确查询或根据名字模糊查询企业列表
        @param key: 关键字
        @param page_index: 页码
        @param page_size: 分页大小
        """

        stmt = select(func.count(EnterPriseModel.id)).where(EnterPriseModel.status != -1, ).where(
            or_(EnterPriseModel.code == key,
                EnterPriseModel.name.like(f"%{key}%")))

        result: ChunkedIteratorResult = await self.db.execute(stmt)
        total = result.scalars().first()

        offset = (page_index - 1) * page_size

        if offset > total:
            return HTTPException(status=ErrEnum.Common.INDEX_ERR, message="请求参数异常")

        stmt = select(EnterPriseModel).where(EnterPriseModel.status != -1, ).where(
            or_(EnterPriseModel.code == key, EnterPriseModel.name.like(f"%{key}%"))).limit(page_size).offset(offset)

        result: ChunkedIteratorResult = await self.db.execute(stmt)
        enterprise_list = result.scalars().fetchall()
        return enterprise_list, total

    async def get_enterprise_by_id(self, enterprise_id: int) -> EnterPriseModel:
        """
        根据code精确查询或根据名字模糊查询企业列表
        @param enterprise_id: 企业id
        """

        stmt = select(EnterPriseModel).where(or_(EnterPriseModel.id == enterprise_id), EnterPriseModel.status != -1, )
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        enterprise_details = result.scalars().first()

        if not enterprise_details:
            raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_NOT_EXIST, message="企业不存在")

        return enterprise_details

    async def update_enterprise_by_id(self, new_enterprise_details: UpdateEnterPriseModel):
        """
        根据code精确查询或根据名字模糊查询企业列表
        @param new_enterprise_details: 企业新资料
        """

        async with self.db.begin():
            params: dict = new_enterprise_details.dict(exclude={"enterprise_id"})
            _new_enterprise_details = {k: v for k, v in params.items() if v}
            stmt = update(EnterPriseModel).where(EnterPriseModel.id == new_enterprise_details.enterprise_id)
            result: CursorResult = await self.db.execute(stmt, _new_enterprise_details)

            if result.rowcount == 1:
                await self.db.commit()
            else:
                # await self.db.rollback()
                raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_NOT_EXIST, message="企业不存在")
