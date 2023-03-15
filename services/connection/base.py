from typing import TypeVar, Type

import httpx
from services.connection.managers.base import NotionIntegrationManager
from services.settings import settings

NotionIntegrationManagerType = TypeVar('NotionIntegrationManagerType', bound=NotionIntegrationManager)


class NotionAPIConnector:
    """
    Класс который отвечает за соединение с сервером Notion API.

    Обращение к API происходит через подключение менеджеров,
    наследуемых от базового класса NotionIntegrationManager.

    Пример использования:
    connector = NotionAPIConnector() # инициализируем коннектор
    my_manager = connector.init_manager(MyManager) # инициализируем менеджер и получаем доступ к его объекту.
    """

    API_URL = 'https://api.notion.com'

    def __init__(self, auth_token: str = settings.AUTH_TOKEN):
        self.__auth_token = auth_token
        self._client = self._get_client()

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.__auth_token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        }

    def _get_client(self):
        client = httpx.AsyncClient(base_url=self.API_URL)
        client.headers.update(self._get_headers())
        return client

    def init_manager(self, manager_class: Type[NotionIntegrationManagerType]) -> NotionIntegrationManagerType:
        """ Возвращает объект переданного менеджера для соединения с частью Notion API """

        return manager_class(client=self._client)

