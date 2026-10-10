from typing import TYPE_CHECKING, Literal

from .. import utils
from ..enums.levels import DailyType, SearchType
from ..errors import NotImplementedModEndpointError
from .endpoint_objects.levels import (
    DownloadLevelResponse,
    GetLevelsResponse,
    SearchFilters,
)
from .endpoint_objects.page import Page, PageInfo
from .gd_objects import DownloadLevel, Gauntlet, MapPack, SearchLevel
from .gd_objects.song import LevelSong
from .gd_objects.user import LevelLeaderboardUser, TinyUser

if TYPE_CHECKING:
    from ..client import GDClient


class LevelsEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    def delete_level(self, level_id: int) -> None:
        """Deletes a level from the servers. Must be logged in to use this endpoint."""
        self.client.check_logged_in()

        self.client.gd_post("deleteGJLevelUser20.php", {"levelID": level_id})

    def download_level(self, level_id: int | DailyType) -> DownloadLevelResponse:
        """Downloads a level from the servers.

        Arguments:
            level_id (int | DailyType):
                ID of the level to download.
                Pass DailyType to download the current daily, weekly, or event level.
        """

        # Convert DailyType enum to daily/weekly/event ID
        if isinstance(level_id, DailyType):
            level_id = (level_id.value * -1) - 1

        response: str = self.client.gd_post("downloadGJLevel22", {"levelID": level_id})

        # level#hash1#hash2#user#songs#extraArtistNames#{progressSave?}#{0;?}
        # level, hash1, hash2 are all returned by default
        raw_data: list[str] = response.split("#")

        level = DownloadLevel.from_string(raw_data[0])

        # Generate and check has the first hash.
        # See GDDocs for an explanation of... whatever this does...
        hash_string_1 = ""
        level_string = level.raw_dict["levelString"]
        if len(level_string) < 41:
            hash_string_1 = level_string
        else:
            shift = len(level_string) // 40
            for i in range(40):
                hash_string_1 += level_string[i * shift]
        utils.check_hash(hash_string_1, raw_data[1])

        # # Generate and check the second hash.
        # # Except I never got this hash to work...
        #
        # raw_level = level.raw_dict
        # # print(raw_level["player_id"])
        # hash_segments = [
        #     raw_level["userID"],
        #     raw_level["stars"],
        #     ('1' if raw_level["demon"] else '0'),
        #     raw_level["levelID"],
        #     raw_level["verifiedCoins"],
        #     raw_level["featureScore"],
        #     (str(level.password) if level.password in (0, 1) else
        #      str(level.password + (1000000 if level.password < 1000000 else 0))),
        #     ('0' if not "dailyNumber" in raw_level else raw_level["dailyNumber"])
        # ]
        # hash_string_2 = "".join(hash_segments)
        # utils.check_hash(hash_string_2, raw_data[2])

        # user is only present with daily/weekly/event levels
        # songs are only present either with DailyType or if the level has multiple songs
        # extra_artist_names are only present if they exist
        user: TinyUser | None = None
        songs: list[LevelSong] = []
        extra_artist_names: list[tuple[int, str]] = []

        if raw_data[4]:
            # Songs' use "~|~" as their delimeter, and can end with `~|` or start with `|~`
            # So we just remove the tildes for simplicity, though: TODO: does this break song names with tildes?
            songs = [
                LevelSong.from_string(song, "|")
                for song in raw_data[4].replace("~", "").split(":")
            ]

        # user is only returned if the level is daily/weekly/event
        if level_id < 0:
            raw_user = raw_data[3]
            user = TinyUser.from_string(raw_user)

        if raw_data[5]:
            input(raw_data[1:])

        return DownloadLevelResponse(
            level=level,
            user=user,
            songs=songs,
            extra_artist_names=extra_artist_names,
            extra_data="#".join(raw_data[6:]),
        )

    def get_daily_level(self, type: int | DailyType = 0) -> tuple[int, int]:
        """Gets the current daily, weekly, or event level's index, and the time left in seconds.

        Arguments:
            type (int | DailyType): 0 for daily, 1 for weekly, 2 for event level.

        Returns:
            Tuple in the following format (index, time_left)
        """
        response = self.client.gd_post("getGJDailyLevel", {"type": type})

        index, time_left = map(int, response.split("|"))

        return (index, time_left)

    def get_gauntlets(self) -> list[Gauntlet]:
        response = self.client.gd_post("getGJGauntlets21", {"special": 1})
        raw_data = response.split("#")

        gauntlets = [
            Gauntlet.from_string(gauntlet) for gauntlet in raw_data[0].split("|")
        ]

        # TODO FIXME: Implement hashes for raw_data[1]

        return gauntlets

    # type = 0: Search type, see values. Defaults to most liked
    # str: query (userID or GDList depending on type)
    # page = 0: Which page to request, defaults to 0
    # accountID = None: only sent w/ types 5 (user lvls), 8 (sent), 13 (friends)
    # gdw: int/bool = 0/1: If the request is from GD World
    # gauntlet: int (id): gauntlet id being requested, TODO FIXME: What mode does this use?
    # local: intbool, fetch "My Levels," current user's levels
    def get_levels(
        self,
        search_type: SearchType = SearchType.SEARCH,
        query: str | int = "",
        page: int = 0,
        filters: SearchFilters | None = None,
        gdw: bool = False,
        raw_params: dict | None = None,
    ) -> GetLevelsResponse:

        parameters: dict[str, str | int] = {}

        parameters["type"] = search_type.value
        parameters["str"] = query
        parameters["page"] = page

        parameters |= filters.to_dict() if filters is not None else {}

        if gdw:
            parameters["gdw"] = 1
        if raw_params is not None:
            parameters.update(raw_params)

        response = self.client.gd_post("getGJLevels21", parameters)

        raw_data = response.split("#")

        levels: list[SearchLevel] = [
            SearchLevel.from_string(raw_level) for raw_level in raw_data[0].split("|")
        ]

        creators: list[TinyUser] = [
            TinyUser.from_string(raw_user) for raw_user in raw_data[1].split("|")
        ]

        # so. TIL (5/12/2026) the reason rob has the tildes
        # is because songs can have pipes/colons in their names. thanks lchavasse
        # https://cdn.discordapp.com/attachments/1007310139172331681/1503936058868498446/Screenshot_20260512_214321.png
        songs: list[LevelSong] = [
            LevelSong.from_string(raw_song, "~|~")
            for raw_song in raw_data[2].split("~:~")
            if raw_song
        ]

        page_info: PageInfo = PageInfo(raw_data[3])

        hash_string = "".join(
            [
                str(level.level_id)[0]
                + str(level.level_id)[-1]
                + str(level.stars)
                + str(int(level.verified_coins))
                for level in levels
            ]
        )
        utils.check_hash(hash_string, raw_data[4])

        return GetLevelsResponse(
            levels=levels, creators=creators, songs=songs, page_info=page_info
        )

    # TODO: Write wrapper methods for the following SearchTypes:
    # SearchType.SEARCH
    # SearchType.USER (query = user_id, local: bool)
    # SearchType.LIST_OF_LEVELS (query = GDList[int])
    # SearchType.FOLLOWED (filters.followed = GDList[Annotated[int, "accountID"]])

    def get_level_scores(
        self, level_id: int, type: Literal[0, 1, 2] = 0
    ) -> list[LevelLeaderboardUser]:
        """Fetches the leaderboard for a level. Submitting your level stats to the server is presently unimplemented.

        Arguments:
            level_id (int): The ID of the level
            type (Literal[0, 1, 2]): 0 for Friends, 1 for Top, 2 for Week. Defaults to 0
        """
        self.client.check_logged_in()

        response = self.client.gd_post(
            "getGJLevelScores211", {"levelID": level_id, "type": type}
        )

        users = [
            LevelLeaderboardUser.from_string(raw_user)
            for raw_user in response.split("|")
            if raw_user
        ]

        return users

    def get_level_scores_platformer(
        self, level_id: int, type: Literal[0, 1, 2] = 0, mode: Literal[0, 1] = 0
    ):
        """Fetches the leaderboard for a platformer level. Submitting your level stats to the server is presently unimplemented.

        Arguments:
            level_id (int): The ID of the level
            type (Literal[0, 1, 2]): 0 for Friends, 1 for Top, 2 for Week. Defaults to 0
            mode (Literal[0, 1]: 0 for Time, 1 for Points. Defaults to 0)
        """

        response = self.client.gd_post(
            "getGJLevelScoresPlat", {"levelID": level_id, "type": type, "mode": mode}
        )

        users = [
            LevelLeaderboardUser.from_string(raw_user)
            for raw_user in response.split("|")
            if raw_user
        ]

        return users


    def get_map_packs(self, page: int = 0) -> Page[MapPack]:
        response = self.client.gd_post("getGJMapPacks21", {"page": page})

        raw_data = response.split("#")

        map_packs: list[MapPack] = [
            MapPack.from_string(map_pack_string)
            for map_pack_string in raw_data[0].split("|")
        ]

        hash_string = ""
        for pack in map_packs:
            pack_id: str = str(pack.pack_id)
            hash_string += pack_id[0] + pack_id[-1] + str(pack.stars) + str(pack.coins)
        utils.check_hash(hash_string, raw_data[2])

        return Page(content=map_packs, page_info=PageInfo(raw_data[1]))

    def rate_demon(self):
        """UNIMPLMENTED"""
        raise NotImplementedModEndpointError()

    def rate_stars(self):
        """UNIMPLIMENTED"""
        raise NotImplementedError()

    def report_level(self) -> None:
        """UNIMPLEMENTED"""
        raise NotImplementedError()

    def suggest_stars(self):
        """UNIMPLEMENTED"""
        raise NotImplementedModEndpointError()

    def update_description(self, level_id: int, description: str) -> bool:
        """UNIMPLEMENTED"""
        raise NotImplementedError()

    def upload_level(self):
        """UNIMPLEMENTED"""
        raise NotImplementedError()
