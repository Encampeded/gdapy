from ..gd_objects.comment import AccountComment, LevelComment, LevelHistoryComment
from ..gd_objects.page import PageInfo
from attrs import define

@define
class CommentPage:
    comments: list[AccountComment] | list[LevelComment] | list[LevelHistoryComment]
    page_info: PageInfo
