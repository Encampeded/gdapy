from typing import TYPE_CHECKING

from .endpoint_objects.lists import GetListsResponse
from .endpoint_objects.page import PageInfo
from .gd_objects.list import SearchList
from .gd_objects.user import TinyUser

if TYPE_CHECKING:
    from ..client import GDClient


class ListsEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    def delete_list(self, list_id: int) -> None:
        """Deletes a list from the server.

        Arguments:
            list_id (int): The ID of the list to be deleted

        Returns:
            bool: True if deleted, False is delete failed
        """
        self.client.check_logged_in()

        self.client.gd_post("deleteGJLevelList", {"listID": list_id})

    def get_lists(
        self, search_type: int = 2, query: str = "", page: int = 0, search_filters=()
    ):
        # This is essentially get_levels but with some limitations.

        data: dict[str, str | int] = {"type": search_type, "str": query, "page": page}

        response = self.client.gd_post("getGJLevelLists", data)

        raw_data = response.split("#")

        lists: list[SearchList] = [
            SearchList.from_string(raw_list)
            for raw_list in raw_data[0].split("|")
            if raw_list
        ]

        creators: list[TinyUser] = [
            TinyUser.from_string(raw_user)
            for raw_user in raw_data[1].split("|")
            if raw_user
        ]

        return GetListsResponse(lists, creators, PageInfo(raw_data[2]))

    def upload_list(
        self,
        name: str,
        description: str,
        levels: list[int],
        difficulty: int,  # -1 = N/A, 0-10 = Auto-Extreme Demon
    ):
        self.client.check_logged_in()

        raise NotImplementedError()
