import asyncio
import os.path
import sys
import logging
from pathlib import Path

from services.file_manager import CSVFileManager
from services.utils import format_notion_comments_to_csv

sys.path.append(os.path.join(Path(__file__).resolve(), ''))


from services.settings import settings
from services.notion import Notion


LOG_FMT = "%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"
LOG_DATE_FMT = "%Y-%m-%d %H:%M:%S"

fmt = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATE_FMT)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(fmt)

# Application
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(sh)


async def main():
    logger.info('Запуск парсера...')

    parser = Notion()
    comment_list = await parser.get_comments_from_block(settings.PAGE_ID)

    title_list, data = format_notion_comments_to_csv(comment_list)

    file_manager = CSVFileManager(title_list=title_list, data=data)
    file_manager.save()


if __name__ == '__main__':
    asyncio.run(main())
