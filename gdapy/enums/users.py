from enum import StrEnum, IntEnum

class LeaderboardType(StrEnum):
    TOP = "top"
    RELATIVE = "relative"
    FRIENDS = "friends"
    CREATORS = "creators"

class LeaderboardStatistic(IntEnum):
    STARS = 0
    MOONS = 1
    DEMONS = 2
    USER_COINS = 3
