from typing import TYPE_CHECKING

from .endpoint_objects import Page, PageInfo
from .gd_objects import DownloadSong, TopArtist

if TYPE_CHECKING:
    from ..client import GDClient


class SongsEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    def get_custom_content_url(self) -> str:
        """Gets the URL for the music & SFX library server."""
        response = self.client.gd_post("getCustomContentURL")

        return response

    def get_song_info(self, song_id: int) -> DownloadSong:

        response = self.client.gd_post("getGJSongInfo", {"songID": song_id})

        song = DownloadSong.from_string(response, "~|~")

        return song

    def get_top_artists(self, page: int = 1) -> Page[TopArtist]:

        response = self.client.gd_post("getGJTopArtists", {"page": page})

        raw_songs, _, raw_page_info = response.partition("#")

        songs = [
            TopArtist.from_string(raw_song)
            for raw_song in raw_songs.split("|")
            if raw_song
        ]

        return Page(songs, PageInfo(raw_page_info))
