from attrs import define

from ...KEY import KEY
from .gd_object import GDObject


@define
class Gauntlet(GDObject):
    gauntlet_id: int
    levels: list[int]

    @property
    def gauntlet_name(self) -> str:
        return KEY["gauntletID"][str(self.gauntlet_id)]
