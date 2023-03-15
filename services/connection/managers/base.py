import os

from httpx import AsyncClient

from services.connection.exceptions import NotionIntegrationException
from services.connection.managers.types import DefaultResponseData, DataObjectType, ResponseDataError


class NotionIntegrationManager:
    """
    Менеджер для доступа к конкретным частям Notion API.
    """

    API_POSTFIX: str = None

    def __init__(self, client: AsyncClient):
        if self.API_POSTFIX is None:
            raise NotionIntegrationException('Обязательный атрибут API_POSTFIX')

        self._client = client
        self._api_url = self._build_api_url()

    def _build_api_url(self):
        return f'v1/{self.API_POSTFIX}'

    def _get_url(self, endpoint: str):
        """
        Метод для использования при наследовании.
        Соединяет префикс ссылки и переданный endpoint.
        """

        return os.path.join(self._build_api_url(), endpoint)

    def _check_data(self, data: dict, type_to_check: DataObjectType) -> dict:
        """
        Проверяет нет ли ошибки в ответе сервера и соответствует ли
        тип полученного ответа, ожидаемому (type_to_check).
        Выбрасывает исключение NotionIntegrationException если проверка не пройдена.
        """

        default_data = DefaultResponseData(**data)

        if default_data.object == DataObjectType.error:
            current_data = ResponseDataError(**data)
            raise NotionIntegrationException(current_data.message)
        elif default_data.object != type_to_check:
            msg = f'Получен неверный тип данных ({default_data.object}). Ожидался ({type_to_check})'
            raise NotionIntegrationException(msg)

        return data

