from attrs import define, field

from .gd_object import GDObject
from .gd_types import B64String


class List(GDObject):
    object_type = "Level"


@define
class SearchList(List):
    ## BEGIN AUTO GENERATED FIELDS
    id: int = field(alias='level_id')
    name: str = field(alias='level_name')
    description: B64String
    version: int
    difficulty: int
    downloads: int
    likes: int
    upload_date: str
    update_date: str
    account_id: int
    username: str
    level_ids: list[int]
    list_reward: int
    list_reward_requirement: int
    feature_score: int | None = None
    ## END AUTO GENERATED FIELDS

    @property
    def rated(self) -> bool:
        return self.feature_score is not None

    @property
    def difficulty_text(self) -> str:
        match self.difficulty:
            case -1:
                return "N/A"
            case 0:
                return "Auto"
            case 1:
                return "Easy"
            case 2:
                return "Normal"
            case _:
                return ""
