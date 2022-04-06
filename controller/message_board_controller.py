from fastapi import APIRouter, Request, Query, Depends

from common.depends import jwt_auth
from servers.message_board_servers import MessageBoardServer
from schema_models.message_board_models import CreateMessageModel, CreateMessageOutModel, MessageOutListModel

message_board_router = APIRouter()


@message_board_router.post("/create", response_model=CreateMessageOutModel, name="企业留言")
async def create(request: Request, new_message: CreateMessageModel, _=Depends(jwt_auth)):
    """
    ### 创建留言
    任何人均可操作
    """
    message_board_server = MessageBoardServer(request)
    message_id = await message_board_server.create(new_message)
    return CreateMessageOutModel(data=message_id)


@message_board_router.get("/list", response_model=MessageOutListModel, name="获取企业留言列表")
async def create(request: Request, enterprise_id: int = Query(..., description="企业id"),
                 page: int = Query(1, description="页码"), size: int = Query(10, description="分页大小")):
    """
    ### 获取企业下的留言
    """
    message_board_server = MessageBoardServer(request)
    message_list = await message_board_server.get_message(enterprise_id, page, size)
    return MessageOutListModel(data=message_list)


@message_board_router.delete("/delete", response_model=CreateMessageOutModel, name="删除留言")
async def create(request: Request, message_id: int = Query(..., description="留言id"), _=Depends(jwt_auth)):
    """
    ### 删除留言
    仅可删除自己的留言
    """
    message_board_server = MessageBoardServer(request)
    del_id = await message_board_server.delete(message_id)
    return CreateMessageOutModel(data=del_id)


# @message_board_router.post("/like", response_model=CreateMessageOutModel, name="留言点赞")
# async def create(request: Request, message_id: int = Query(..., description="留言id"), _=Depends(jwt_auth)):
#     message_board_server = MessageBoardServer(request)
#     del_id = await message_board_server.delete(message_id)
#     return CreateMessageOutModel(data=del_id)
