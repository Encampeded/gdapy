from datetime import datetime
from typing import Any, NamedTuple, get_args

from pyheck import snake


def type_to_str_rec(t: Any) -> str:
    field_type = t if isinstance(t, str) else t.__name__

    if type_args := get_args(t):
        field_type += f"[{', '.join(map(type_to_str_rec, type_args))}]"

    return field_type


class Field(NamedTuple):
    name: str
    type: type | str
    default: str = ""

    def type_to_str(self) -> str:
        return type_to_str_rec(self.type)

    def to_line(self) -> str:  # TODO: snake_case name

        name = snake(self.name)
        if "_i_ds" in name:
            name = name.replace("_i_ds", "_ids")

        field_type = self.type_to_str()

        default = " = " + self.default if self.default else ""

        return f"    {name}: {field_type}{default}\n"


F = Field

KEY: dict[str, dict[str, Field]] = {
    "Song": {
        "1": F("ID", int, ""),
        "2": F("name", str, ""),
        "3": F("artistID", int),
        "4": F("artistName", str),
        "5": F("size", float),
        "6": F("videoID", str),
        "7": F("youtubeURL", str),
        "8": F("isVerified", bool),
        "9": F("songPriority", int),
        "10": F("link", str),
        "11": F("nongEnum", int),
        "12": F("extraArtistIDs", list[int]),
        "13": F("new", bool),
        "14": F("newType", int),
        "15": F("extraArtistNames", list[int]),
        "16": F("downloadSoundtrackOverride", str),
        "18": F(
            "artistLinks", str
        ),  # {artistID},{platformID},,{url}; | 1 = YouTube, 5 = Bandcamp, 7 = Personal Website, 8 = Instagram
    },
    "Comment": {
        "1": F("levelID", int),
        "2": F("comment", "B64String"),
        "3": F("userID", int),
        "4": F("likes", int),
        "5": F("dislikes", int),
        "6": F("messageID", int),
        "7": F("spam", bool),
        "8": F("authorAccountID", int),
        "9": F("age", str),
        "10": F("percent", int),
        "11": F("modBadge", "ModLevel"),
        "12": F("moderatorChatColor", list[int]),
        "15": F("timestamp", datetime),
    },
    "Level": {
        "1": F("levelID", int),
        "2": F("levelName", str),
        "3": F("description", "B64String"),
        "4": F(
            "levelString",
            str,
            "field(repr=lambda s: s[:64] + '...' if len(s) > 64 else s)",
        ),
        "5": F("version", int),
        "6": F("userID", int),
        "8": F("difficultyDenominator", int),
        "9": F("difficultyNumerator", int),
        "10": F("downloads", int),
        "11": F("setCompletes", int),
        "12": F("officialSong", int),
        "13": F("gameVersion", int),
        "14": F("likes", int),
        "15": F("length", int),
        "16": F("dislikes", int),
        "17": F("demon", bool),
        "18": F("stars", int),
        "19": F("featureScore", int),
        "20": F("starRatings", int),
        "21": F("starRatingsSum", int),
        "22": F("minStarRatings", int),
        "23": F("maxStarRatings", int),
        "24": F("demonVotes", int),
        "25": F("auto", bool),
        "26": F("recordString", str),
        "27": F("password", int),
        "28": F("uploadDate", str),
        "29": F("updateDate", str),
        "30": F("copiedID", int),
        "31": F("twoPlayer", bool),
        "32": F("rateStars", int),
        "33": F("rateFeature", bool),
        "34": F("rateUser", str),
        "35": F("customSongID", int),
        "36": F("extraString", str),
        "37": F("coins", int),
        "38": F("verifiedCoins", bool),
        "39": F("starsRequested", int),
        "40": F("lowDetailMode", bool),
        "41": F("dailyNumber", int),
        "42": F("epic", int),
        "43": F("demonDifficulty", int),
        "44": F("isGauntlet", bool),
        "45": F("objects", int),
        "46": F("editorTime", int),
        "47": F("editorTimeCopies", int),
        "48": F("settingsString", str),
        "52": F("songIDs", list[int]),
        "53": F("sfxIDs", list[int]),
        "54": F("songSize", int),
        "57": F("verificationTime", int),
        "62": F("exactUploadTime", datetime),
        "63": F("exactUpdateTime", datetime),
    },
    "User": {
        "1": F("userName", str),
        "2": F("userID", int),
        "3": F("stars", int),
        "4": F("demonCount", int),
        "6": F("ranking", int),
        "7": F("accountHighlight", str),
        "8": F("creatorPoints", int),
        "9": F("iconID", int),
        "10": F("color", int),
        "11": F("color2", int),
        "12": F("shipID", int),
        "13": F("secretCoins", int),
        "14": F("iconType", "Gamemode"),
        "15": F("glow", bool, 'field(alias="special")'),
        "16": F("accountID", int),
        "17": F("userCoins", int),
        "18": F("messageState", int),
        "19": F("friendRequestsState", int, 'field(alias="friends_state")'),
        "20": F("youtube", str, 'field(alias="you_tube")'),
        "21": F("icon", int, 'field(alias="acc_icon")'),
        "22": F("ship", int, 'field(alias="acc_ship")'),
        "23": F("ball", int, 'field(alias="acc_ball")'),
        "24": F("ufo", int, 'field(alias="acc_bird")'),
        "25": F("wave", int, 'field(alias="acc_dart")'),
        "26": F("robot", int, 'field(alias="acc_robot")'),
        "27": F("streak", int, 'field(alias="acc_streak")'),
        "28": F("glow", bool, 'field(alias="acc_glow")'),
        "29": F("isRegistered", bool),
        "30": F("globalRank", int),
        "31": F("friendState", int),
        "32": F("friendRequestID", int),
        "35": F("friendRequestMessage", str),
        "37": F("friendRequestAge", int),
        "38": F("messages", int),
        "39": F("friendRequests", int),
        "40": F("newFriends", int),
        "41": F("newFriendRequest", bool),
        "42": F("age", str),
        "43": F("spider", int, 'field(alias="acc_spider")'),
        "44": F("twitter", str),
        "45": F("twitch", str),
        "46": F("diamonds", int),
        "48": F("explosion", int, 'field(alias="acc_explosion")'),
        "49": F("mod", int),
        "50": F("commentHistoryState", int),
        "51": F("color3", int),
        "52": F("moons", int),
        "53": F("swing", int, 'field(alias="acc_swing")'),
        "54": F("jetpack", int, 'field(alias="acc_jetpack")'),
        "55": F("demons", "Demons"),
        "56": F("classicLevels", "ClassicLevels"),
        "57": F("platformerLevels", "PlatformerLevels"),
        "58": F("discord", str),
        "59": F("instagram", str),
        "60": F("tiktok", str),
        "61": F("custom", str),
        "62": F("unknown62", str),
        "63": F("unknown63", str),
        "67": F("unknown67", str),
    },
}
