import json
from sqlalchemy import insert, update, select, or_, func
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm import selectinload

from common.err import HTTPException, ErrEnum
from schema_models.enterprise_models import CreateEnterPriseModel, UpdateEnterPriseModel
from models.enterprise_models import EnterpriseModel, EnterpriseLog
from servers.base_server import BaseServer


class EnterPriseServer(BaseServer):

    async def check_enterprise(self, new_enterprise: CreateEnterPriseModel):
        """
        检查企业是否存在
        """
        if new_enterprise.code is not None:
            stmt = select(EnterpriseModel).where(EnterpriseModel.status != -1) \
                .where(or_(EnterpriseModel.name == new_enterprise.name, EnterpriseModel.code == new_enterprise.code))
        else:
            stmt = select(EnterpriseModel).where(EnterpriseModel.name == new_enterprise.name,
                                                 EnterpriseModel.status != -1)

        result: ChunkedIteratorResult = await self.db.execute(stmt)

        enterprise = result.scalars().first()
        if enterprise:
            raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_EXIST, message="企业已存在")

    async def check_enterprise_by_id(self, enterprise_id: int):
        """
        检查企业是否存在
        """

        stmt = select(EnterpriseModel).where(EnterpriseModel.id == enterprise_id, EnterpriseModel.status != -1)

        result: ChunkedIteratorResult = await self.db.execute(stmt)

        enterprise = result.scalars().first()
        if not enterprise:
            raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_NOT_EXIST, message="企业不存在")

    async def create_enterprise(self, new_enterprise: CreateEnterPriseModel) -> EnterpriseModel:
        """
        创建新企业
        """
        # async with self.db.begin():
        await self.check_enterprise(new_enterprise)

        # _new_enterprise = EnterPriseModel(create_user_id=self.request.user, **new_enterprise.dict())
        # self.db.add(_new_enterprise)
        insert_stmt = insert(EnterpriseModel).values(create_user_id=self.request.user, **new_enterprise.dict())
        result: CursorResult = await self.db.execute(insert_stmt)
        if not result.is_insert:
            raise Exception("create err")
        await self.db.commit()

        select_stmt = select(EnterpriseModel).where(EnterpriseModel.id == result.lastrowid)
        result: ChunkedIteratorResult = await self.db.execute(select_stmt)
        _new_enterprise = result.scalars().first()

        return _new_enterprise

    async def get_enterprise_list(self, key: str, page_index: int, page_size: int):
        """
        根据code精确查询或根据名字模糊查询企业列表
        @param key: 关键字
        @param page_index: 页码
        @param page_size: 分页大小
        """

        stmt = select(func.count(EnterpriseModel.id)).where(EnterpriseModel.status != -1, ) \
            .where(or_(EnterpriseModel.code == key, EnterpriseModel.name.like(f"%{key}%")))

        result: ChunkedIteratorResult = await self.db.execute(stmt)
        total = result.scalars().first()

        offset = (page_index - 1) * page_size

        if offset > total:
            return HTTPException(status=ErrEnum.Common.INDEX_ERR, message="请求参数异常")

        stmt = select(EnterpriseModel).where(EnterpriseModel.status != -1, ).where(
            or_(EnterpriseModel.code == key, EnterpriseModel.name.like(f"%{key}%"))).limit(page_size).offset(offset)

        result: ChunkedIteratorResult = await self.db.execute(stmt)
        enterprise_list = result.scalars().fetchall()
        return enterprise_list, total

    async def get_enterprise_by_id(self, enterprise_id: int) -> EnterpriseModel:
        """
        根据id查询企业信息
        @param enterprise_id: 企业id
        """

        stmt = select(EnterpriseModel).where(or_(EnterpriseModel.id == enterprise_id), EnterpriseModel.status != -1, )
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

            enterprise: EnterpriseModel = await self.get_enterprise_by_id(new_enterprise_details.enterprise_id)

            # 修改数据
            params: dict = new_enterprise_details.dict(exclude={"enterprise_id"})
            _params = {k: v for k, v in params.items() if v and v != getattr(enterprise, k)}

            if not _params:
                raise HTTPException(status=ErrEnum.Common.PARAMS_ERR, message="无数据变动")

            stmt = update(EnterpriseModel).where(EnterpriseModel.id == new_enterprise_details.enterprise_id)
            result: CursorResult = await self.db.execute(stmt, _params)

            if result.rowcount != 1:
                raise HTTPException(status=ErrEnum.EnterPrise.ENTERPRISE_NOT_EXIST, message="企业不存在")

            # 写修改日志
            insert_stmt = insert(EnterpriseLog).values(user_id=self.request.user) \
                .values(enterprise_id=new_enterprise_details.enterprise_id) \
                .values(data=json.dumps(_params, ensure_ascii=False))
            result: CursorResult = await self.db.execute(insert_stmt)

            if result.rowcount != 1:
                raise HTTPException(status=ErrEnum.EnterPrise.CREATE_LOG_ERR, message="日志添加失败")

            await self.db.commit()

        return True
