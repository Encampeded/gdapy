from ast import literal_eval
from base64 import urlsafe_b64decode
from enum import IntEnum, StrEnum
from typing import Self

from attrs import define, field

from ...enums.misc import Gamemode
from .gd_converter import gd_converter
from .gd_object import GDObject


@define
class TinyUser:
    name: str
    account_id: int
    user_id: int

    # Returned as `userID:username:accountID` in many miscellaneous endpoints
    @classmethod
    def from_string(cls, user: str) -> Self:
        user_id, username, account_id = user.split(":")
        return cls(name=username, account_id=int(account_id), user_id=int(user_id))


# Enjoy this amazing table featuring what endpoints return what user keys.
# Keys with curly bracket(s) are optional afaik
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# getInfoFull:    01 02 03 04       08    10 11 13       16 17 18 19 20 21 22 23 24 25 26 28 29 30 31 {32 35 37 38 39 40}     43 44 45 46 48 49 50 51 52 53 54 55 56 57 58 59 60 61
# getInfoRandUsr: 01 02 03 04       08    10 11 13       16 17 18 19 20 21 22 23 24 25 26 28 29 30 31                         43 44 45 46 48 49 50 51 52 53 54 55 56 57 58 59 60 61
# getUsers:       01 02 03 04 06    08 09 10 11 13 14 15 16 17                                                                         46          51 52
# getScores:      01 02 03 04 06 {7 08 09 10 11 13 14 15 16 17                                                                         46             52
# getScoresGlbl:  01 02 03 04 06 {7 08 09 10 11 13 14 15 16 17                                                                         46             52
# getScoresLvl:   01 02 03    06       09 10 11 13 14 15 16                                                                42
# getFriendReqs:  01 02                09 10 11    14 15 16                                            32 35 37         41                         51
# CommentUser:    01                   09 10 11    14 15 16                                                                                        51
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TinyUser:       01 02                                     16 (Returned as `userID:username:accountID` in many miscellaneous endpoints)


class FriendState(StrEnum):
    # This is only a strenum because the server sends an empty string
    # to represent unfriended, and not 0. Thanks rob...
    UNFRIENDED = ""
    FRIENDED = "1"
    REQUEST_SENT = "3"
    REQUEST_RECEIVED = "4"


class State(IntEnum):
    ALL = 0
    FRIENDS = 1
    NONE = 2


class FriendRequestState(IntEnum):
    ALL = 0
    NONE = 1


# TODO: Should this go in enums.py? Other endpoints might use a similar enum
class ModLevel(StrEnum):
    NONE = "0"
    MOD = "1"
    ELDER_MOD = "2"
    LEADERBOARD_MOD = "3"


@define
class Breakdown:
    pass


@gd_converter.register_structure_hook
def breakdown_hook(value: str, t: type[Breakdown]) -> Breakdown:
    breakdown_tuple: tuple[int, ...] = literal_eval(f"({value})")
    return gd_converter.structure_attrs_fromtuple(breakdown_tuple, t)


@define
class Demons(Breakdown):
    easy: int
    medium: int
    hard: int
    insane: int
    extreme: int

    easy_plat: int
    medium_plat: int
    hard_plat: int
    insane_plat: int
    extreme_plat: int

    weekly: int
    gauntlet: int


@define
class ClassicLevels(Breakdown):
    auto: int
    easy: int
    normal: int
    hard: int
    harder: int
    insane: int
    daily: int
    gauntlet: int


@define
class PlatformerLevels(Breakdown):
    auto: int
    easy: int
    normal: int
    hard: int
    harder: int
    insane: int
    the_map: int


@define
class User(GDObject):
    object_type = "User"

    @classmethod
    def _clean(cls, raw_dict: dict) -> dict:

        if "friendRequestMessage" in raw_dict:
            raw_dict["friendRequestMessage"] = urlsafe_b64decode(
                raw_dict["friendRequestMessage"].encode()
            ).decode()

        if "special" in raw_dict:
            raw_dict["special"] = raw_dict["special"] == "2"

        # if "demons" in raw_dict:
        #     # then we have a DownloadLevel
        #     raw_dict["demons"] = Demons.from_string(raw_dict["demons"])
        #     raw_dict["classicLevels"] = ClassicLevels.from_string(raw_dict["classicLevels"])
        #     raw_dict["platformerLevels"] = PlatformerLevels.from_string(raw_dict["platformerLevels"])

        return super()._clean(raw_dict)


@define
class DownloadUser(User):
    ## BEGIN AUTO GENERATED FIELDS
    user_name: str
    user_id: int
    stars: int
    demon_count: int
    creator_points: int
    color: int
    color2: int
    secret_coins: int
    account_id: int
    user_coins: int
    message_state: int
    friend_requests_state: int = field(alias='friends_state')
    youtube: str = field(alias='you_tube')
    icon: int = field(alias='acc_icon')
    ship: int = field(alias='acc_ship')
    ball: int = field(alias='acc_ball')
    ufo: int = field(alias='acc_bird')
    wave: int = field(alias='acc_dart')
    robot: int = field(alias='acc_robot')
    glow: bool = field(alias='acc_glow')
    is_registered: bool
    global_rank: int
    friend_state: int
    spider: int = field(alias='acc_spider')
    twitter: str
    twitch: str
    diamonds: int
    explosion: int = field(alias='acc_explosion')
    mod: int
    comment_history_state: int
    color3: int
    moons: int
    swing: int = field(alias='acc_swing')
    jetpack: int = field(alias='acc_jetpack')
    demons: Demons
    classic_levels: ClassicLevels
    platformer_levels: PlatformerLevels
    discord: str
    instagram: str
    tiktok: str
    custom: str
    unknown62: str
    unknown63: str
    unknown67: str
    friend_request_id: int | None = None
    friend_request_message: str | None = None
    friend_request_age: int | None = None
    messages: int | None = None
    friend_requests: int | None = None
    new_friends: int | None = None
    ## END AUTO GENERATED FIELDS


@define
class SearchUser(User):
    ## BEGIN AUTO GENERATED FIELDS
    user_name: str
    user_id: int
    stars: int
    demon_count: int
    ranking: int
    creator_points: int
    icon_id: int
    color: int
    color2: int
    secret_coins: int
    icon_type: Gamemode
    glow: bool = field(alias='special')
    account_id: int
    user_coins: int
    diamonds: int
    color3: int
    moons: int
    ## END AUTO GENERATED FIELDS


@define
class LeaderboardUser(User):
    ## BEGIN AUTO GENERATED FIELDS
    user_name: str
    user_id: int
    stars: int
    demon_count: int
    ranking: int
    creator_points: int
    icon_id: int
    color: int
    color2: int
    secret_coins: int
    icon_type: Gamemode
    glow: bool = field(alias='special')
    account_id: int
    user_coins: int
    diamonds: int
    color3: int
    moons: int
    account_highlight: str | None = None
    ## END AUTO GENERATED FIELDS


@define
class LevelLeaderboardUser(User):
    ## BEGIN AUTO GENERATED FIELDS
    user_name: str
    user_id: int
    stars: int
    ranking: int
    icon_id: int
    color: int
    color2: int
    icon_type: Gamemode
    glow: bool = field(alias='special')
    account_id: int
    age: str
    color3: int
    secret_coins: int | None = None
    ## END AUTO GENERATED FIELDS

    @property
    def percentage(self) -> int:
        return self.stars

    @property
    def time(self) -> int:
        return self.stars


@define
class FriendRequestUser(User):
    ## BEGIN AUTO GENERATED FIELDS
    user_name: str
    user_id: int
    icon_id: int
    color: int
    color2: int
    icon_type: Gamemode
    glow: bool = field(alias='special')
    account_id: int
    friend_request_id: int
    friend_request_message: str
    friend_request_age: int
    new_friend_request: bool
    color3: int
    ## END AUTO GENERATED FIELDS


@define
class CommentUser(User):
    ## BEGIN AUTO GENERATED FIELDS
    user_name: str
    icon_id: int
    color: int
    color2: int
    icon_type: Gamemode
    glow: bool = field(alias='special')
    account_id: int
    color3: int
    ## END AUTO GENERATED FIELDS
