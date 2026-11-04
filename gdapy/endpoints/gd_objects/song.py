from attrs import define

from .gd_object import GDObject


class Song(GDObject):
    object_type = "Song"

    @classmethod
    def _clean(cls, raw_dict: dict) -> dict:
        if raw_dict.get("extraArtistIDs", False):
            raw_dict["extraArtistIDs"] = raw_dict["extraArtistIDs"].replace(".", ",")

        return super()._clean(raw_dict)


@define
class TopArtist(Song):
    ## BEGIN AUTO GENERATED FIELDS
    artist_id: int
    artist_name: str
    youtube_url: str | None = None
    artist_links: str | None = None
    ## END AUTO GENERATED FIELDS


@define
class LevelSong(Song):
    ## BEGIN AUTO GENERATED FIELDS
    id: int
    name: str
    artist_id: int
    artist_name: str
    size: float
    video_id: str
    youtube_url: str
    is_verified: bool
    link: str
    download_soundtrack_override: str
    nong_enum: int | None = None
    extra_artist_ids: list[int] | None = None
    new: bool | None = None
    artist_links: str | None = None
    ## END AUTO GENERATED FIELDS


@define
class DownloadSong(Song):
    ## BEGIN AUTO GENERATED FIELDS
    id: int
    name: str
    artist_id: int
    artist_name: str
    size: float
    video_id: str
    youtube_url: str
    is_verified: bool
    link: str
    download_soundtrack_override: str
    nong_enum: int | None = None
    extra_artist_ids: list[int] | None = None
    new: bool | None = None
    song_link: str | None = None
    artist_links: str | None = None
    ## END AUTO GENERATED FIELDS


# class Song(GDObject):
#     song_id: int = field(alias="ID")
#     song_name: str = field(alias="name")
#     artist_id: int
#     artist_name: str
#     size: float #TODO int or float?, Size of the song in MB, rounded to two decimal places

#     is_verified: bool

#     video_id: str | None
#     youtube_url: str | None
#     link: str | None
#     nong: NongEnum | None = field(default = NongEnum.NONE, alias="nongEnum")
#     # TODO FIXME: does this work?

#     # TODO:
#     download_soundtrack_override: str | None = None

#     extra_artists: list[dict] = []

#     # The following attributes, while listed on GDDocs, seem to literally never be returned...
#     # is_verified: bool | None = None
#     # song_priority: int | None = None # "priority over the song list" what the fuck does that mean
#     # new: bool | None = None
#     # new_type: bool | None = None

#     object_type = "Song"

#     @classmethod
#     def _clean(cls, raw_dict: dict) -> dict:

#         if raw_dict["link"] != '-':
#             raw_dict["link"] = unquote(raw_dict["link"])

#         if "extraArtistNames" in raw_dict:
#             raw_dict["extraArtists"] = [
#                 {"artist_id": int(artist[0]), "artist_name": artist[1]}
#                 for artist in batched(raw_dict["extraArtistNames"].split(','), 2)
#             ]
#             # artists: list[str] = raw_dict["extraArtistNames"].split(',')
#             # for artist in batched(artists, 2):
#             #     raw_dict["extraArtists"].append({
#             #         "artist_id": int(artist[0]),
#             #         "artist_name": artist[1]
#             #     })
#         # else:
#         #     raw_dict["extraArtists"] = []


#         return super()._clean(raw_dict)
