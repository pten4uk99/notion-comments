import logging

from services.connection.managers.base import NotionIntegrationManager
from services.connection.managers.comment.types import ResponseDataComment
from services.connection.managers.types import DataObjectType


logger = logging.getLogger(__name__)


class CommentManager(NotionIntegrationManager):
    API_POSTFIX = 'comments'

    def _get_url(self, endpoint: str):
        return self._build_api_url() + f'?block_id={endpoint}'

    async def get(self, block_id: str):
        logger.info(f'Получаем информацию о комментариях блока "{block_id}"')

        response = await self._client.get(self._get_url(block_id))
        data = self._check_data(response.json(), DataObjectType.list)
        pydantic_data = ResponseDataComment(**data)
        return pydantic_data
