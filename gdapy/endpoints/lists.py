from base64 import urlsafe_b64encode
from typing import TYPE_CHECKING

from ..enums.levels import DemonDifficulty, Difficulty, SearchType, Unlisted

if TYPE_CHECKING:
    from ..client import GDClient


class ListsEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    def delete_list(self, list_id: int) -> bool:
        """Deletes a list from the server.

        Arguments:
            list_id (int): The ID of the list to be deleted

        Returns:
            bool: True if deleted, False is delete failed
        """
        self.client.check_logged_in()

        response = self.client.gd_post("deleteGJLevelList", {"listID": list_id})

        # TODO: This doesn't really work because gd_post raises an error if '-1'
        return response == "1"

    def get_lists(self):
        # This is essentially get_levels but with some limitations.

        raise NotImplementedError()

    def upload_list(
        self,
        name: str,
        description: str,
        levels: list[int],
        difficulty: int,  # -1 = N/A, 0-10 = Auto-Extreme Demon
    ):
        self.client.check_logged_in()

        raise NotImplementedError()
