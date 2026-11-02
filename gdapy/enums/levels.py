from enum import IntEnum, StrEnum

from .gd_enum import GDEnum

# Endpoint Argument Enums
# Used by endpoint/levels.py

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
    LIST_OF_LEVELS = 26 # same as type 19 (unknown list of levels) but can return up to 100 levels
    # SENT_2 = 27 # TODO FIXME: GDDocs just calls this Sent
    GD_LITE_WEEKLY_LEVELS = 28
    GD_LITE_BONUS_LEVELS = 29


class DailyType(IntEnum):
    DAILY = 0
    WEEKLY = 1
    EVENT = 2


# Endpoint enums
# Used by endpoints/endpoint_objects/levels.py

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

# Used by SearchFilterss
class DemonDifficulty(IntEnum):
    """SearchFilters DemonDifficulty filter"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    INSANE = 4
    EXTREME = 5

# Field enums
# Used by endpoints/gd_objects/levels.py

# the world if level object used the same enums as everything else
# ✨✨✨✨✨✨✨
# alas, said world is unrealistic and impossible :(


class DifficultyNumerator(GDEnum):
    UNRATED = 0
    EASY = 10
    NORMAL = 20
    HARD = 30
    HARDER = 40
    INSANE = 50

class LevelDemonDifficulty(GDEnum):
    EASY_DEMON = 3
    MEDIUM_DEMON = 4
    HARD_DEMON = 0
    INSANE_DEMON = 5
    EXTREME_DEMON = 6


class LevelLength(GDEnum):
    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4
    PLATFORMER = 5

class EpicRating(GDEnum):
    NONE = 0
    EPIC = 1
    LEGENDARY = 2
    MYTHIC = 3


class OfficialSong(GDEnum):
    PRACTICE_STAY_INSIDE_ME = -1
    STEREO_MADNESS = 0
    BACK_ON_TRACK = 1
    POLARGEIST = 2
    DRY_OUT = 3
    BASE_AFTER_BASE = 4
    CANT_LET_GO = 5
    JUMPER = 6
    TIME_MACHINE = 7
    CYCLES = 8
    XSTEP = 9
    CLUTTERFUNK = 10
    THEORY_OF_EVERYTHING = 11
    ELECTROMAN_ADVENTURES = 12
    CLUBSTEP = 13
    ELECTRODYNAMIX = 14
    HEXAGON_FORCE = 15
    BLAST_PROCESSING = 16
    THEORY_OF_EVERYTHING_2 = 17
    GEOMETRICAL_DOMINATOR = 18
    DEADLOCKED = 19
    FINGERDASH = 20
    DASH = 21
    EXPLORERS = 22
    THE_SEVEN_SEAS = 23
    VIKING_ARENA = 24
    AIRBORNE_ROBOTS = 25
    SECRET = 26
    PAYLOAD = 27
    BEAST_MODE = 28
    MACHINA = 29
    YEARS = 30
    FRONTLINES = 31
    SPACE_PIRATES = 32
    STRIKER = 33
    EMBERS = 34
    ROUND_1 = 35
    MONSTER_DANCE_OFF = 36
    PRESS_START = 37
    NOCK_EM = 38
    POWER_TRIP = 39
