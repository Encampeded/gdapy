from attrs import define, field

from ...enums.levels import DemonDifficulty, Difficulty, Length, Rating
from ...KEY import KEY
from ..gd_objects.level import DownloadLevel, SearchLevel
from ..gd_objects.song import LevelSong
from ..gd_objects.user import TinyUser
from .page import PageInfo


@define
class DownloadLevelResponse:
    """Represents a response from downloadGJLevel22.php

    Attributes:
        level (DownloadLevel): The downloaded level
        user (TinyUser | None):
            The user who uploaded the level. Only returned by daily,
            weekly, or event level downloads
        songs (list[Song]): A list of songs the level uses
        extra_artist_names (list[tuple[int, str]]):
            A list of extra artists' names from songs, deduplicated,
            in the format (artist_id, artist_name)
        extra_data (str):
            Presently undocumented data returned at the end of the response
    """

    level: DownloadLevel
    user: TinyUser | None
    songs: list[LevelSong]
    extra_artist_names: list[tuple[int, str]]
    extra_data: str


@define
class GetLevelsResponse:
    """Represents a response from getGJLevels21.php

    Attributes:


    """

    levels: list[SearchLevel]
    creators: list[TinyUser]
    songs: list[LevelSong]
    page_info: PageInfo


@define
class SearchFilters:
    pass
    # # difficulty: GDList[Difficulty] | None = field(default=None, name="diff")
    # demon_difficulty: DemonDifficulty | None = field(default=None, name="demonFilter")
    # # length: GDList[Length] | None = field(default=None, name="len")

    # only_uncompleted: bool | None = field(default=None, name="uncompleted")
    # only_completed: bool | None = field(default=None, name="onlycompleted")
    # # completed_levels: GDList[int] | None = field(default=None, name="completedLevels")

    # is_original: bool | None = field(default=None, name="original")
    # is_two_player: bool | None = field(default=None, name="twoPlayer")
    # has_coins: bool | None = field(default=None, name="coins")

    # # So I was trying this, and found it doesn't work
    # # is_rated will return mythic levels, not just star rated levels.
    # # EXCEPT that's just how to server works. The in-game filters
    # # do the same thing. I'm glad it's the servers that are broken
    # # and not my code lol.
    # rating: Rating | None = None
    # # is_unrated: bool | None = field(default=None, name="noStar")
    # # is_rated: bool | None = field(default=None, name="star")
    # # is_featured: bool | None = field(default=None, name="featured")
    # # is_epic: bool | None = field(default=None, name="epic")
    # # is_legendary: bool | None = field(default=None, name="mythic")
    # # is_mythic: bool | None = field(default=None, name="legendary")

    # song_id: int | None = field(default=None, name="song")
    # uses_custom_song: bool | None = field(default=None, name="customSong")

    # validate_filters: bool = True

    # def to_dict(self):
    #     return {f: getattr(self, f) for f in self.__struct_fields__}

    # def validate(self) -> dict:

    #     # if self.demon_difficulty:
    #     #     self.difficulty = GDList()
    #     #     self.difficulty.append(Difficulty.DEMON)

    #     # It seems like the gd servers just rolls with stuff like this but eh
    #     if self.validate_filters:

    #         # if self.completed_levels is not None and not (self.only_completed or self.only_uncompleted):
    #         #     raise msgspec.ValidationError("Completed levels present when not searching for completed/completed!")

    #         if self.only_completed and self.only_uncompleted:
    #             raise msgspec.ValidationError("TODO FIXME WRITEME")

    #         # If we're using an official song, that actually isn't a valid official song ID.
    #         if (not self.uses_custom_song and
    #             self.song_id is not None and
    #             self.song_id not in KEY["officialSong"]):
    #             raise msgspec.ValidationError(f"Invalid officialSong ID: {self.song_id}")

    #         # If we say we're using a custom song, but we don't have a song_id
    #         if self.uses_custom_song and self.song_id is None:
    #             raise msgspec.ValidationError("TODO FIXME WRITEME")

    #     # Encode w/ msgspec
    #     encoded_filters = msgspec.to_builtins(
    #         self,
    #         enc_hook=enc_hook
    #     )

    #     # Now we fix what msgspec did lol.
    #     # This kinda sucks ngl.
    #     encoded_filters.pop("validate_filters", None)

    #     if "rating" in encoded_filters:
    #         encoded_filters[encoded_filters["rating"]] = 1
    #         encoded_filters.pop("rating")

    #     for key, value in encoded_filters.copy().items():
    #         if isinstance(value, bool):
    #             encoded_filters[key] = int(value)

    #     return encoded_filters
