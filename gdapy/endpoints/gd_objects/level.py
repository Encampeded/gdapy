from base64 import urlsafe_b64decode
from datetime import datetime
from typing import TYPE_CHECKING
from zlib import decompress

from attrs import define, field

from ...enums.levels import (
    DifficultyNumerator,
    EpicRating,
    LevelDemonDifficulty,
    LevelLength,
    OfficialSong,
)
from ...enums.misc import XORKeys
from ...utils import gd_xor_cipher, gdb64_decode
from .gd_object import GDObject
from .gd_types import B64String


@define
class BeatenLevel:
    """Returned by syncGJAccountNew.php"""

    level_id: int
    stars: int


@define
class Level(GDObject):
    object_type = "Level"

    # this feels mildly unholy
    # so does writing typed python so
    if TYPE_CHECKING:
        auto: bool
        demon: bool
        demon_difficulty: LevelDemonDifficulty
        difficulty_numerator: DifficultyNumerator
        stars: int
        feature_score: int
        epic: EpicRating
        official_song: OfficialSong

    @property
    def difficulty(self) -> str:
        if self.auto:
            return "Auto"

        if self.demon:
            return str(self.demon_difficulty)

        return str(self.difficulty_numerator)

    @property
    def rating(self) -> str:
        if not self.stars:
            return "Unrated"

        elif not self.feature_score:
            return "Star Rated"

        return str(self.epic)

    @property
    def game_version_semantic(self) -> float:
        game_version = int(self.raw_dict["gameVersion"])
        if int(game_version) <= 7:
            return float(f"1.{game_version - 1}")

        elif int(game_version) == 10:
            return 1.7

        return game_version / 10

    @property
    def official_song_name(self) -> str:
        return str(self.official_song)


@define
class SearchLevel(Level):
    ## BEGIN AUTO GENERATED FIELDS
    id: int = field(alias="level_id")
    name: str = field(alias="level_name")
    description: B64String
    version: int
    user_id: int
    difficulty_denominator: int
    difficulty_numerator: DifficultyNumerator
    downloads: int
    official_song: OfficialSong
    game_version: int
    likes: int
    length: LevelLength
    demon: bool
    stars: int
    feature_score: int
    auto: bool
    copied_id: int
    two_player: bool
    custom_song_id: int
    coins: int
    verified_coins: bool
    stars_requested: int
    epic: EpicRating
    demon_difficulty: LevelDemonDifficulty
    objects: int
    editor_time: int
    editor_time_copies: int | None = None
    ## END AUTO GENERATED FIELDS


@define
class DownloadLevel(Level):
    ## BEGIN AUTO GENERATED FIELDS
    id: int = field(alias="level_id")
    name: str = field(alias="level_name")
    description: B64String
    level_string: str = field(repr=lambda s: "'" + s[:64] + "...'")
    version: int
    user_id: int
    difficulty_denominator: int
    difficulty_numerator: DifficultyNumerator
    downloads: int
    official_song: OfficialSong
    game_version: int
    likes: int
    length: LevelLength
    demon: bool
    stars: int
    feature_score: int
    auto: bool
    password: int
    upload_date: str
    update_date: str
    copied_id: int
    two_player: bool
    custom_song_id: int
    extra_string: str
    coins: int
    verified_coins: bool
    stars_requested: int
    low_detail_mode: bool
    epic: EpicRating
    demon_difficulty: LevelDemonDifficulty
    objects: int
    exact_upload_time: datetime
    exact_update_time: datetime
    daily_number: int | None = None
    editor_time: int | None = None
    editor_time_copies: int | None = None
    song_ids: list[int] | None = None
    sfx_ids: list[int] | None = None
    song_size: int | None = None
    verification_time: int | None = None
    ## END AUTO GENERATED FIELDS

    @classmethod
    def _clean(cls, raw_dict: dict) -> dict:

        # Decode level_string
        raw_dict["levelString"] = decompress(
            urlsafe_b64decode(raw_dict["levelString"].encode()), 15 | 32
        ).decode()

        # Decode password
        raw_dict["password"] = int(
            0
            if raw_dict["password"] == "0"
            else (
                gd_xor_cipher(
                    gdb64_decode(raw_dict["password"]), XORKeys.LEVEL_PASSWORD
                )
            )
        )

        return super()._clean(raw_dict)
