from attrs import define

from ..gd_objects.comment import AccountComment, LevelComment, LevelHistoryComment
from .page import PageInfo


@define
class CommentPage:
    comments: list[AccountComment] | list[LevelComment] | list[LevelHistoryComment]
    page_info: PageInfo
