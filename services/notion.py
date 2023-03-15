import asyncio
import logging

from pydantic import BaseModel

from services.connection.base import NotionAPIConnector
from services.connection.managers.block import BlockManager
from services.connection.managers.block.types import ResponseDataBlock
from services.connection.managers.comment.manager import CommentManager
from services.connection.managers.comment.types import Comment
from services.connection.managers.user.manager import UserManager
from services.connection.managers.user.types import User

logger = logging.getLogger(__name__)


class NotionComment(BaseModel):
    comment: Comment
    user: User


class Notion:
    def __init__(self):
        connector = NotionAPIConnector()

        self.block_manager = connector.init_manager(BlockManager)
        self.comment_manager = connector.init_manager(CommentManager)
        self.user_manager = connector.init_manager(UserManager)

        self.__comments_data: list[NotionComment] = []

    async def _get_block_children(self, block: ResponseDataBlock) -> list[ResponseDataBlock]:
        results = [block]

        if block.has_children:
            children_data = await self.block_manager.get_children(block.id)
            children = children_data.results

            for child in children:
                results.extend(await self._get_block_children(child))

        return results

    async def _get_block_comments(self, block: ResponseDataBlock):
        """
        Добавляет комментарии и соответственную информацию о
        пользователях из блока в self.__comments_data
        """

        comment_data = await self.comment_manager.get(block.id)
        comments: list[NotionComment] = []

        tasks = []
        for comment in comment_data.results:
            task = asyncio.create_task(
                self._task_to_append_user_info_in_comments_list(
                    comments_list=comments,
                    user_id=comment.created_by.id,
                    current_comment=comment
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
        self.__comments_data.extend(comments)

    async def _task_to_append_user_info_in_comments_list(self, comments_list: list[NotionComment],
                                                         current_comment: Comment, user_id: str):
        """ Получает и добавляет полученного пользователя в comments_list """

        user = await self._get_user_by_id(user_id)
        comments_list.append(NotionComment(comment=current_comment, user=user))

    async def _get_user_by_id(self, user_id: str):
        """ Получает информацию пользователя по идентификатору """

        return await self.user_manager.get(user_id)

    async def get_comments_from_block(self, block_id: str):
        """
        Рекурсивно получает все комментарии из блока и вложенных в него блоков.
        Так же можно передавать в аргумент идентификатор страницы, так как
        id блока и id страницы равны.
        """

        block = await self.block_manager.get(block_id)
        page_blocks = await self._get_block_children(block)

        tasks = []
        for block in page_blocks:
            tasks.append(self._get_block_comments(block))

        await asyncio.gather(*tasks)

        comments = self.__comments_data.copy()
        self.__comments_data = []

        logger.info(f'Сформирован список из {len(comments)} комментариев')
        return comments
