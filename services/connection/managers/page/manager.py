from services.connection.managers.base import NotionIntegrationManager
from services.connection.managers.page.types import ResponseDataPage
from services.connection.managers.types import DataObjectType


class PageManager(NotionIntegrationManager):
    API_POSTFIX = 'pages'

    async def get(self, page_id: str):
        response = await self._client.get(self._get_url(page_id))
        data = response.json()
        data = self._check_data(data, DataObjectType.page)
        pydantic_data = ResponseDataPage(**data)
        return pydantic_data
