from attrs import define

from ...key import KEY
from .gd_object import GDObject


@define
class BaseMapPack(GDObject):
    pack_id: int
    levels: list[int]

    object_type = "MapPack"


@define
class Gauntlet(BaseMapPack):
    @property
    def gauntlet_name(self):
        return KEY["gauntletID"][str(self.pack_id)]


@define
class BeatenMapPack(BaseMapPack):
    """Returned by syncGJAccountNew.php"""

    stars: int
    coins: int


@define
class MapPack(BeatenMapPack):
    pack_name: str
    difficulty: str
    text_color: list[int]
    bar_color: list[int]
