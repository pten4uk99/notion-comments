from typing import TypeVar

from services.notion import NotionComment

TitleList = TypeVar('TitleList', bound=list[str])
ResultData = TypeVar('ResultData', bound=list)


def format_notion_comments_to_csv(comments: list[NotionComment]) -> tuple[TitleList, ResultData]:
    title_list = ['Статья', 'Автор', 'Комментарий', 'Дата']
    result = []

    for notion_comment in comments:
        comment = notion_comment.comment
        user = notion_comment.user

        comment_text = ''

        for elem in notion_comment.comment.rich_text:
            comment_text = elem.plain_text

        row = [comment.parent.block_id, f'{user.name} {user.person.email}', comment_text, comment.created_time]
        result.append(row)

    return title_list, result
