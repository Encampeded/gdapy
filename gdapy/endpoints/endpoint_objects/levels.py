from attrs import define, field
from cattrs.gen import make_dict_unstructure_fn

from ...enums.levels import DemonDifficulty, Difficulty, Length, Rating
from ...KEY import KEY
from ..gd_objects.gd_converter import gd_converter
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
    difficulties: list[Difficulty] = field(factory=list, alias="diff")
    demon_difficulty: DemonDifficulty | None = field(default=None, alias="demonFilter")

    lengths: list[Length] = field(factory=list, alias="len")
    is_rated: bool = field(default=False, alias="star")

    # Following are in the "Advanced Options" menu in the client

    only_uncompleted: bool = field(default=False, alias="uncompleted")
    only_completed: bool = field(default=False, alias="onlycompleted")
    completed_levels: list[int] = field(factory=list, alias="completedLevels")
    # completed_levels is a comma seperated list of your completed levels for the above filters
    # I wonder if we could auto generate them if logged in...

    is_original: bool = field(default=False, alias="original")
    has_coins: bool = field(default=False, alias="coins")
    is_two_player: bool = field(default=False, alias="twoPlayer")

    song_id: int | None = field(default=None, alias="song")
    uses_custom_song: bool = field(default=False, alias="customSong")

    # is_rated isn't for only star_rated levels; that filter just doesn't exist lmao
    is_unrated: bool = field(default=False, alias="noStar")
    is_featured: bool = field(default=False, alias="featured")
    is_epic: bool = field(default=False, alias="epic")
    is_legendary: bool = field(default=False, alias="mythic")
    is_mythic: bool = field(default=False, alias="legendary")

    validate_filters: bool = True

    def to_dict(self):
        if self.validate_filters:
            self.validate()

        return gd_converter.unstructure(self)

    def validate(self):

        exclusive_difficulties = [d for d in self.difficulties if d < 0]

        if not len(exclusive_difficulties) < 2:
            raise ValueError(
                "Difficulties contain more than one exclusive value (N/A, Demon, and Auto)"
            )

        if self.uses_custom_song and not self.song_id:
            raise ValueError()


gd_converter.register_unstructure_hook(
    SearchFilters,
    make_dict_unstructure_fn(SearchFilters, gd_converter, _cattrs_omit_if_default=True),
)
