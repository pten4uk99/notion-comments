import logging

from services.connection.managers.base import NotionIntegrationManager
from services.connection.managers.block.types import ResponseDataBlock, ResponseDataBlockChildren
from services.connection.managers.types import DataObjectType


logger = logging.getLogger(__name__)


class BlockManager(NotionIntegrationManager):
    API_POSTFIX = 'blocks'

    async def get_children(self, block_id: str):
        logger.info(f'Получаем информацию о вложенных элементах блока "{block_id}"')

        response = await self._client.get(self._get_url(f'{block_id}/children?page_size=100'))
        data = self._check_data(response.json(), DataObjectType.list)
        pydantic_data = ResponseDataBlockChildren(**data)
        return pydantic_data

    async def get(self, block_id: str):
        logger.info(f'Получаем информацию о блоке страницы "{block_id}"')

        response = await self._client.get(self._get_url(block_id))
        data = self._check_data(response.json(), DataObjectType.block)
        pydantic_data = ResponseDataBlock(**data)
        return pydantic_data
