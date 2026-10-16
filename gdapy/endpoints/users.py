from typing import TYPE_CHECKING

from ..enums import LeaderboardStatistic, LeaderboardType
from .gd_objects import DownloadUser, LeaderboardUser, SearchUser

if TYPE_CHECKING:
    from ..client import GDClient


class UsersEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    def get_scores(
        self,
        statistic: LeaderboardStatistic = LeaderboardStatistic.STARS,
        type: LeaderboardType = LeaderboardType.TOP,
        count: int = 100,
    ) -> list[LeaderboardUser]:
        # TODO: What happens when you do relative when not logged in and no uuid?
        # as far as i remember, i tried and it just kinda works. so.

        response = self.client.gd_post(
            "getGJScores20",
            {"type": type.value, "stat": statistic.value, "count": count},
        )

        return [
            LeaderboardUser.from_string(user) for user in response.split("|") if user
        ]

    def get_user_info(self, account_id: int) -> DownloadUser:

        response = self.client.gd_post(
            "getGJUserInfo20", {"targetAccountID": account_id}
        )

        # We snip out page data (#999:0:10) because it is functionally meaningless
        return DownloadUser.from_string(response)

    def get_user(self, query: str) -> SearchUser:

        response = self.client.gd_post("getGJUsers20", {"str": query})

        return SearchUser.from_string(response.partition("#")[0])

    def update_user(self):
        """UNIMPLEMENTED"""
        raise NotImplementedError()

        # This would be extremely painful to implement.
        # Also, considering this would be an extremely easy way to cheat,
        # maybe I just shouldn't implement this.
        # I don't really see a good use for this other than that.
