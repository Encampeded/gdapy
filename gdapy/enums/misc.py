from enum import Enum, IntEnum, StrEnum

# TODO FIXME:
# Should we have an enum for salts?

# haha look at this old ass stupid comment
# there IS a salts enum now, get fucked


class Gamemode(Enum):
    CUBE = '0'
    SHIP = '1'
    BALL = '2'
    UFO = '3'
    WAVE = '4'
    ROBOT = '5'
    SPIDER = '6'
    SWING = '7'
    JETPACK = '8'

class Secrets(StrEnum):
    COMMON = "Wmfd2893gb7"
    ACCOUNT = "Wmfv3899gc9"
    LEVEL = "Wmfv2898gc9"
    MOD = "Wmfp3879gc3"
    # ADMIN = "Wmfx2878gb9"
    # "Currently, the Admin Secret no longer works as RobTop became aware of it." lol

class Salts(StrEnum):
    LEVEL = "xI25fpAapCQg"
    COMMENT = "xPT6iUrtws0J"
    LIKE_RATE = "ysg6pUrtjn0J"
    PROFILE = "xI35fsAapCRg"
    LEVEL_LEADERBOARD = "yPg6pUrtWn0J"
    VAULT = "yPg6pUrtWn0J"
    CHALLENGES = "oC36fpYaPtdg" # getGJChallenges
    REWARDS = "pC26fpYaQCtg" # getGJRewards
    GJP2 = "mI29fmAnxgTs"

class NongEnum(IntEnum):
    NONE = 0
    NCS = 1
    CHOMPO = 2
    LIBRARY = 10

class XORKeys(IntEnum):
    SAVE_DATA = 11 # Only singular xor
    MESSAGES = 14251
    VAULT_CODES = 19283
    DAILY_CHALLENGES = 19847
    LEVEL_PASSWORD = 26364
    COMMENT = 29481
    ACCOUNT_PASSWORD = 37526
    LEVEL_LEADERBOARD = 39673
    LEVEL = 41274
    LOAD_DATA = 48291
    # MULTIPLAYER = 52832
    MUSIC_SFX_LIBRARY = 57709
    RATING = 58281
    CHEST_REWARDS = 59182
    STAT_SUBMISSION = 85271

class Platform(Enum):
    """Corresponds to the Cocos2d CC_TARGET_PLATFORM macro"""
    UNKNOWN = 0
    IOS = 1
    ANDROID = 2
    WINDOWS = 3
    MACOS = 8
    # some day, perchance, gd-docs will explain udids for ios/macos?
