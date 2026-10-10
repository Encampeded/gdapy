from datetime import datetime

from attrs import define

from .gd_object import GDObject
from .gd_types import B64String
from .user import CommentUser, ModLevel


@define
class Comment(GDObject):
    object_type = "Comment"


@define
class AccountComment(Comment):
    ## BEGIN AUTO GENERATED FIELDS
    comment: B64String
    likes: int
    message_id: int
    age: str
    timestamp: datetime
    ## END AUTO GENERATED FIELDS


@define
class LevelComment(Comment):
    ## BEGIN AUTO GENERATED FIELDS
    comment: B64String
    user_id: int
    likes: int
    message_id: int
    spam: bool
    age: str
    percent: int
    timestamp: datetime
    mod_badge: ModLevel | None = None
    moderator_chat_color: list[int] | None = None
    ## END AUTO GENERATED FIELDS

    user: CommentUser = None  # type: ignore


@define
class LevelHistoryComment(Comment):
    ## BEGIN AUTO GENERATED FIELDS
    level_id: int
    comment: B64String
    user_id: int
    likes: int
    message_id: int
    age: str
    percent: int
    timestamp: datetime
    mod_badge: ModLevel | None = None
    moderator_chat_color: list[int] | None = None
    ## END AUTO GENERATED FIELDS

    user: CommentUser = None  # type: ignore


# type Comment = AccountComment | LevelComment | LevelHistoryComment
