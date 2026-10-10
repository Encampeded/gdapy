from ...enums.levels import Difficulty
from .gd_object import GDObject
from .gd_types import B64String


class List(GDObject):
    list_id: int
    list_name: str
    description: B64String
    version: int
    difficult: Difficulty
    likes: int
    downloads: int
    rated: bool  # TODO

    # TODO: "The Unix timestamp of when..." so int?
    upload_date: str
    update_date: str

    account_id: int
    username: str
    level_ids: list[int]
    list_reward: int
    list_reward_requirement: int


"""

"""
