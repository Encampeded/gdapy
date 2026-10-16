from attrs import define, field

from ..gd_objects import BeatenLevel, BeatenMapPack


@define
class SyncAccountResponse:
    """syncGJAccountNew.php response

    Attributes:
        save_CCGameManager (str)
        save_CCLocalLevels (str)
        game_version (int): game_version sent when saving
        binary_version (int): binary_version sent when saving
        levels (list[BeatenLevel]): list of rated beaten levels
        map_packs (list[BeatenMapPack]): list of beaten map packs
    """

    save_CCGameManager: str
    save_CCLocalLevels: str

    game_version: int
    binary_version: int
    levels: list[BeatenLevel]
    map_packs: list[BeatenMapPack]

    def __repr__(self):
        repr = "SyncAccountResponse("

        def truncate_str(string: str, maxlen: int = 64) -> str:
            return string[:maxlen] + "..." if len(string) > maxlen else string

        # FIXME: atp i should just write some nice repr helpers for objects that need them
        repr += "save_CCGameManager='" + truncate_str(self.save_CCGameManager) + "', "
        repr += "save_CCLocalLevels=" + truncate_str(self.save_CCLocalLevels) + "', "
        repr += "game_version=" + str(self.game_version) + ", "
        repr += "binary_version=" + str(self.binary_version) + ", "
        repr += "levels=" + self.levels[:16].__repr__() + ", "
        repr += "map_packs=" + self.map_packs[:16].__repr__() + ", "

        return repr


@define
class AccountSettings:
    """A user's account settings.

    Attributes:
        message (int, optional): Who the user allows messages from: 0: Anyone, 1: Friends, 2: No one.
        friend_request (int, optional): Who the user allows friend requests from: 0: Anyone, 1: No one.
        comment (int, optional): Who the user allows to view their comments: 0: Anyone, 1: Friends, 2: No one.
        youtube (str, optional): The user's YouTube channel ID (after youtube.com/channel/)
        twitter (str, optional): The user's Twitter handle.
        twitch (str, optional): The user's Twitch username.
        instagram (str, optional): The user's Instagram username.
        tiktok (str, optional): The user's TikTok handle.
        discord (str, optional): The user's Discord handle.
        custom (str, optional): The user's custom one-time authentication token.
    """

    messages: int | None = field(default=None, alias="mS")
    friend_requests: int | None = field(default=None, alias="frS")
    comments: int | None = field(default=None, alias="cS")

    youtube: str | None = field(default=None, alias="yt")
    twitter: str | None = None
    twitch: str | None = None
    instagram: str | None = None
    tiktok: str | None = None
    discord: str | None = None

    custom: str | None = None
