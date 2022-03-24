from servers.base_server import BaseServer
from sqlalchemy import insert, update, select, or_, func
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.orm import selectinload
from typing import Union

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

    async def create_enterprise(self, new_enterprise: CreateEnterPriseModel) -> Union[EnterPriseModel, HTTPException]:
        """
        创建新企业
        """
        # async with self.db.begin():
        await self.check_enterprise(new_enterprise)

        # stmt = insert(EnterPriseModel)
        # result = await self.db.execute(stmt, new_enterprise.dict())
        # if result.is_insert:
        #     await self.db.commit()
        try:
            _new_enterprise = EnterPriseModel(create_user_id=self.request.user, **new_enterprise.dict())

            self.db.add(_new_enterprise)
            await self.db.commit()
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

    async def get_enterprise_by_id(self, enterprise__id: int):
        """
        根据code精确查询或根据名字模糊查询企业列表
        @param enterprise__id: 企业id
        """

        stmt = select(EnterPriseModel).where(or_(EnterPriseModel.id == enterprise__id), EnterPriseModel.status != -1, )
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        enterprise_details = result.scalars().first()

        if not enterprise_details:
            raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_NOT_EXIST, message="企业不存在")

        return enterprise_details
