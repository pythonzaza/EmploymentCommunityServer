from fastapi import APIRouter, Request, Query, Depends

from common.err import HTTPException
from common.depends import jwt_auth
from schema_models.enterprise_models import (CreateEnterPriseModel, EnterPriseDetailsModel, EnterPriseListModel, )
from servers.enterprise_servers import EnterPriseServer

enterprise_router = APIRouter()


@enterprise_router.post("/create", response_model=EnterPriseDetailsModel, name="新增企业资料")
async def create_enter_prise(request: Request, new_enterprise: CreateEnterPriseModel, _=Depends(jwt_auth)):
    """
    ## 创建公司信息
    """
    server = EnterPriseServer(request)
    new_enterprise_base_model = await server.create_enterprise(new_enterprise)
    new_enterprise_out_model = EnterPriseDetailsModel(data=new_enterprise_base_model)
    return new_enterprise_out_model


@enterprise_router.get("/enterprise/list", response_model=EnterPriseListModel, name="获取企业列表")
async def enter_prise_list(request: Request, key: str = Query("", description="关键字,名称或信用码"),
                           page_index: int = Query(1, description="页码", ge=0),
                           page_size: int = Query(10, description="分页大小", ge=0, le=30)):
    server = EnterPriseServer(request)
    enterprise_list, total = await server.get_enterprise_list(key, page_index, page_size)
    return EnterPriseListModel(data=enterprise_list, total=total)


@enterprise_router.get("/enterprise/details", response_model=EnterPriseDetailsModel, name="获取企业详情")
async def enter_prise_list(request: Request, enterprise_id: int = Query(1, description="企业id", ge=0)):
    server = EnterPriseServer(request)
    enterprise_details = await server.get_enterprise_by_id(enterprise_id)
    return EnterPriseDetailsModel(data=enterprise_details)
