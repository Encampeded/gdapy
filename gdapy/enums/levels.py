from enum import Enum, IntEnum, StrEnum


class SearchType(IntEnum):
    SEARCH = 0
    MOST_DOWNLOADED = 1
    MOST_LIKED = 2
    TRENDING = 3
    RECENT = 4
    USERS_LEVELS = 5  # Query is userID
    FEATURED = 6
    MAGIC = 7
    SENT = 8
    # LIST_OF_LEVELS = 10 # Get multiple levels. Query is CommaSeperatedIDList of IDs
    AWARDED = 11
    FOLLOWED = 12  # See `followed` parameter
    FRIENDS = 13  # Login Required
    GD_WORLD_MOST_LIKED = 15
    HALL_OF_FAME = 16
    GD_WORLD_FEATURED = 17
    # UNKNOWN = 18 # "always empty, perhaps robtop only?"
    # LIST_OF_LEVELS_2 = 19 # same as type 10 (list of levels) but this type has pagination and no star rate filter
    DAILY_HISTORY = 21
    WEEKLY_HISTORY = 22
    EVENT_HISTORY = 23
    # REPORTED_LEVELS = 24 # Elder mods only
    LIST = 25  # str is listID
    # LIST_OF_LEVELS_3 = 26 # same as type 19 (unknown list of levels) but can return up to 100 levels
    # SENT_2 = 27 # TODO FIXME: GDDocs just calls this Sent
    GD_LITE_WEEKLY_LEVELS = 28
    GD_LITE_BONUS_LEVELS = 29


class DailyType(IntEnum):
    DAILY = 0
    WEEKLY = 1
    EVENT = 2


# Parameter enums
# Used by endpoints/endpoint_objects/levels.py


class Unlisted(Enum):
    PUBLIC = 0
    FRIENDS_ONLY = 1
    UNLISTED = 2


class Rating(StrEnum):
    UNRATED = "noStar"
    STAR_RATED = "star"
    FEATURED = "featured"
    EPIC = "epic"
    LEGENDARY = "mythic"
    MYTHIC = "legendary"


class Difficulty(IntEnum):
    # NONE = '-'
    NA = -1
    DEMON = -2
    AUTO = 0

    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDER = 4
    INSANE = 5

    EASY_DEMON = 6
    MEDIUM_DEMON = 7
    HARD_DEMON = 8
    INSANE_DEMON = 9
    EXTREME_DEMON = 10


class DemonDifficulty(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    INSANE = 4
    EXTREME = 5


class Length(IntEnum):
    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4
    PLATFORMER = 5


# Object enums
# Used by endpoints/gd_objects/levels.py
