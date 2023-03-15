import csv
import logging

from services.settings import settings


logger = logging.getLogger(__name__)


class CSVException(Exception):
    pass


class CSVFileManager:
    def __init__(self, title_list: list[str], data: list[list]):
        self.data = data
        self.title_list = title_list
        self.columns = len(title_list)

        self._check_data()

    def _check_data(self):
        for item in self.data:
            if len(item) != self.columns:
                raise CSVException(f'Неверное количество столбцов в элементе {item}, ожидалось {self.columns}')
        return True

    def save(self):
        logger.info(f'Открываем файл {settings.PATH_TO_FILE}')

        with open(settings.PATH_TO_FILE, 'w', encoding='utf8') as f:
            logger.info('Файл успешно открыт. Записываем данные')
            writer = csv.writer(f)

            writer.writerow(self.title_list)

            for item in self.data:
                writer.writerow(item)
                logger.info(f'Записана строка {item}')

        logger.info('Данные сохранены!')


