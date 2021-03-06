from servers.base_server import BaseServer
from sqlalchemy import insert, update, select, or_, func, join
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.engine.cursor import CursorResult
from typing import Optional
from sqlalchemy.orm import selectinload

from common.err import HTTPException, ErrEnum
from servers.enterprise_servers import EnterPriseServer
from servers.user_servers import UserServer
from schema_models.message_board_models import CreateMessageModel
from models.message_board_models import MessageBoardModel, MessageLikeLogModel
from models.user_models import UserModel


class MessageBoardServer(BaseServer):
    async def check_message(self, enterprise_id: int, message_id: int) -> MessageBoardModel:
        """
        根据企业id和留言id检查留言是否存在
        """
        stmt = select(MessageBoardModel).where(MessageBoardModel.enterprise_id == enterprise_id,
                                               MessageBoardModel.id == message_id, MessageBoardModel.status != -1)
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        _reply_message = result.scalars().first()
        if not _reply_message:
            raise HTTPException(status=ErrEnum.MessageBoard.MESSAGE_NOT_EXIST, message="留言不存在")
        return _reply_message

    async def check_message_by_id(self, message_id: int) -> MessageBoardModel:
        """
        根据id检查留言是否存在
        """
        stmt = select(MessageBoardModel).where(MessageBoardModel.id == message_id)
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        _reply_message = result.scalars().first()
        if not _reply_message:
            raise HTTPException(status=ErrEnum.MessageBoard.MESSAGE_NOT_EXIST, message="留言不存在")
        return _reply_message

    async def create(self, new_message: CreateMessageModel):
        """

        """
        enterprise_server = EnterPriseServer(self.request)

        async with self.db.begin():

            await enterprise_server.check_enterprise_by_id(new_message.enterprise_id)

            user_server = UserServer(self.request)
            user = await user_server.get_user_by_id(self.request.user)

            new_message_dict = new_message.dict()
            new_message_dict["user_id"] = user.id
            new_message_dict["user_name"] = user.name

            if new_message.reply_message_id:
                _reply_message = await self.check_message(new_message.enterprise_id, new_message.reply_message_id)
                new_message_dict["reply_user_id"] = _reply_message.user_id
                new_message_dict["reply_user_name"] = _reply_message.user_name

            stmt = insert(MessageBoardModel).values(**new_message_dict)
            result: CursorResult = await self.db.execute(stmt)
            if not result.is_insert:
                raise

            await enterprise_server.message_autoincrement(new_message.enterprise_id)

            await self.db.commit()
        return result.lastrowid

    async def get_message(self, enterprise_id: int, page: int = 0, size: int = 10):
        total_stmt = select(func.count(MessageBoardModel.id)).where(MessageBoardModel.enterprise_id == enterprise_id)
        result: ChunkedIteratorResult = await self.db.execute(total_stmt)
        total = result.scalars().first()

        offset = (page - 1) * size

        if offset > total:
            raise HTTPException(status=ErrEnum.Common.INDEX_ERR, message="分页数据异常")

        stmt = select(MessageBoardModel).where(MessageBoardModel.enterprise_id == enterprise_id) \
            .where(MessageBoardModel.status != -1).limit(size).offset(offset)

        result: ChunkedIteratorResult = await self.db.execute(stmt)
        message_list = result.scalars().fetchall()

        # from sqlalchemy.orm import aliased
        # user = aliased(UserModel)
        # reply_user = aliased(UserModel)
        # sql = select(MessageBoardModel, user.name, reply_user.name) \
        #     .join((user, MessageBoardModel.user_id == user.id))\
        #     .join((reply_user, MessageBoardModel.reply_user_id == reply_user.id))
        # print(sql)

        return message_list

    async def delete(self, message_id: int):
        message = await self.check_message_by_id(message_id)

        if message.user_id != self.request.user:
            raise HTTPException(status=ErrEnum.MessageBoard.PERMISSIONS_ERR, message="权限异常")

        if message.status == -1:
            raise HTTPException(status=ErrEnum.MessageBoard.STATUS_ERR, message="留言已删除")

        stmt = update(MessageBoardModel).where(MessageBoardModel.id == message_id).values(status=-1)
        result: CursorResult = await self.db.execute(stmt)
        if result.rowcount == 1:
            await self.db.commit()
        else:
            raise Exception("删除失败")

        return message.id

    async def check_message_like_log(self, message_id: int) -> Optional[MessageLikeLogModel]:
        """
        根据用户id和留言id查询点赞记录
        """
        stmt = select(MessageLikeLogModel).where(MessageLikeLogModel.message_id == message_id) \
            .where(MessageLikeLogModel.user_id == self.request.user)
        result: ChunkedIteratorResult = await self.db.execute(stmt)
        like_log = result.scalars().first()
        if not like_log:
            return None
        else:
            return like_log

    async def like(self, message_id: int):
        """
        点赞
        """
        async with self.db.begin():
            message: MessageBoardModel = await self.check_message_by_id(message_id)

            if message.status == -1:
                raise HTTPException(status=ErrEnum.MessageBoard.STATUS_ERR, message="留言已删除")

            like_log: MessageLikeLogModel = await self.check_message_like_log(message.id)

            if not like_log:
                stmt = insert(MessageLikeLogModel).values(message_id=message_id, user_id=self.request.user)
            elif like_log.status == 1:
                stmt = update(MessageLikeLogModel).values(status=-1).where(MessageLikeLogModel.message_id == message_id) \
                    .where(MessageLikeLogModel.user_id == self.request.user)
            else:
                stmt = update(MessageLikeLogModel).values(status=1).where(MessageLikeLogModel.message_id == message_id) \
                    .where(MessageLikeLogModel.user_id == self.request.user)

            result: CursorResult = await self.db.execute(stmt)
            if result.rowcount != 1:
                raise Exception("操作失败")

            if not like_log or like_log.status == -1:
                add_like_num_stmt = update(MessageBoardModel).where(MessageBoardModel.id == message_id) \
                    .values(like_number=MessageBoardModel.like_number + 1)
            else:
                add_like_num_stmt = update(MessageBoardModel).where(MessageBoardModel.id == message_id) \
                    .values(like_number=MessageBoardModel.like_number + 1)

            result: CursorResult = await self.db.execute(add_like_num_stmt)
            if result.rowcount != 1:
                raise Exception("操作失败")

            await self.db.commit()

        return message.id
