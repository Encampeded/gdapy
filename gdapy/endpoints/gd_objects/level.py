from base64 import b64decode, urlsafe_b64decode
from datetime import datetime
from zlib import decompress

from attrs import define, field

from ...enums.misc import XORKeys
from ...KEY import KEY  # TODO: Move whatever is in/uses KEY to an enum
from ...utils import gd_xor_cipher
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

    # TODO: Is using properties really the best way to do this?
    # I think it is.

    @property
    def length_text(self) -> str:
        return KEY["length"][self.raw_dict["length"]]

    @property
    def difficulty(self) -> str:
        if self.raw_dict["auto"] == "1":
            return "Auto"

        elif self.raw_dict["demon"] == "1":
            return KEY["demonDifficulty"][self.raw_dict["demonDifficulty"]] + " Demon"

        return KEY["difficulty"][self.raw_dict["difficultyNumerator"]]

    @property
    def rating(self) -> str:
        if self.raw_dict["stars"] == "0":
            return "Unrated"
        elif self.raw_dict["featureScore"] == "0":
            return "Star Rated"

        return KEY["rating"][self.raw_dict["epic"]]

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
        return KEY["officialSong"][self.raw_dict["officialSong"]]


@define
class SearchLevel(Level):
    ## BEGIN AUTO GENERATED FIELDS
    level_id: int
    level_name: str
    description: B64String
    version: int
    user_id: int
    difficulty_denominator: int
    difficulty_numerator: int
    downloads: int
    official_song: int
    game_version: int
    likes: int
    length: int
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
    epic: int
    demon_difficulty: int
    objects: int
    editor_time: int
    editor_time_copies: int | None = None
    ## END AUTO GENERATED FIELDS


@define
class DownloadLevel(Level):
    ## BEGIN AUTO GENERATED FIELDS
    level_id: int
    level_name: str
    description: B64String
    level_string: str = field(repr=lambda s: s[:64] + '...' if len(s) > 64 else s)
    version: int
    user_id: int
    difficulty_denominator: int
    difficulty_numerator: int
    downloads: int
    official_song: int
    game_version: int
    likes: int
    length: int
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
    epic: int
    demon_difficulty: int
    objects: int
    exact_upload_time: datetime
    exact_update_time: datetime
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
        if raw_dict["password"] == "0":
            raw_dict["password"] = 0

        else:
            # Password decoding code adapted from GDDocs and George https://stackoverflow.com/a/20558041
            # decode the password from base64

            decoded_b64 = b64decode(
                raw_dict["password"].encode()
            ).decode()  # TODO: This feels familiar...
            password = gd_xor_cipher(decoded_b64, XORKeys.LEVEL_PASSWORD)

            raw_dict["password"] = int(password)

        return super()._clean(raw_dict)
