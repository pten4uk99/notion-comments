import logging

from services.connection.managers.base import NotionIntegrationManager
from services.connection.managers.types import DataObjectType
from services.connection.managers.user.types import User


logger = logging.getLogger(__name__)


class UserManager(NotionIntegrationManager):
    API_POSTFIX = 'users'

    def _get_url(self, endpoint: str):
        """ endpoint - идентификатор пользователя """

        return self._build_api_url() + f'/{endpoint}'

    async def get(self, user_id: str):
        logger.info(f'Получаем информацию о пользователе "{user_id}"')

        response = await self._client.get(self._get_url(user_id))
        data = self._check_data(response.json(), DataObjectType.user)
        pydantic_data = User(**data)
        return pydantic_data
