from attrs import define, field

from ...enums import GauntletID, MapPackDifficulty
from .gd_object import GDObject


@define
class BaseMapPack(GDObject):
    levels: list[int]
    pack_id: int

    object_type = "MapPack"


@define
class Gauntlet(BaseMapPack):
    # this should work... despite the error
    pack_id: GauntletID = field(converter=GauntletID) # zuban: ignore

    @property
    def name(self):
        return str(self.pack_id)


@define
class BeatenMapPack(BaseMapPack):
    """Returned by syncGJAccountNew.php"""
    stars: int
    coins: int


@define
class MapPack(BeatenMapPack):
    pack_name: str
    difficulty: MapPackDifficulty
    text_color: list[int]
    bar_color: list[int]
