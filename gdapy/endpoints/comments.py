from base64 import urlsafe_b64encode
from typing import TYPE_CHECKING, Annotated

from .. import utils
from ..enums import XORKeys
from .endpoint_objects import Page, PageInfo
from .gd_objects import AccountComment, CommentUser, LevelComment, LevelHistoryComment

if TYPE_CHECKING:
    from ..client import GDClient


class CommentsEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    def _parse_level_comment(
        self, comment_type: type[LevelComment | LevelHistoryComment], raw_data: str
    ) -> LevelComment | LevelHistoryComment:
        raw_comment, _, raw_user = raw_data.partition(":")

        comment: LevelComment | LevelHistoryComment = comment_type.from_string(
            raw_comment, "~"
        )
        comment.user = CommentUser.from_string(raw_user, "~")

        return comment

    # target_account_id exists because
    # above is how i found this comment... but im guessing it exists for mods
    def delete_account_comment(
        self, comment_id: int, target_account_id: int = -1
    ) -> None:
        """Deletes an account comment.

        Arguments:
            comment_id (int): ID of the comment to be deleted
            target_account_id (int): Account ID of the comment author. Defaults to own account ID
        """
        self.client.check_logged_in()

        if target_account_id == -1:
            target_account_id = self.client.common_data["accountID"]

        if target_account_id != self.client.common_data["accountID"]:
            print(
                "You seem to be attempting to delete someone else's account comment. Are you a moderator? If so, please contact the maintainer!"
            )
            # self.client.check_modded() implement at some point...?

        response = self.client.gd_post(
            "deleteGJAccComment20",
            data={"commentID": comment_id, "targetAccountID": target_account_id},
        )

        # if it doesn't, something has gone wrong...
        # gd_post should check if
        assert response == "1"

    def delete_comment(self, comment_id: int, level_id: int) -> bool:
        """Deletes a level comment.

        Arguments:
            comment_id (int): ID of the comment to be deleted
            level_id (int): ID of the level the comment is on

        Returns:
            bool: Whether the delete succeeded
        """
        self.client.check_logged_in()

        response = self.client.gd_post(
            "deleteGJComment20", data={"commentID": comment_id, "levelID": level_id}
        )

        return response == "1"

    def get_account_comments(
        self, account_id: int, page: int = 0, count: int = 10
    ) -> Page[AccountComment]:
        """Gets a user's account comments.

        Arguments:
            account_id (int): The account ID of the user
            page (int)

        Returns:
            CommentPage

        """

        data = {"accountID": account_id, "page": page}
        if page != 10:
            data["page"] = page

        response = self.client.gd_post("getGJAccountComments20", data)

        raw_data = response.split("#")

        comments = [
            AccountComment.from_string(comment, "~")
            for comment in raw_data[0].split("|")
        ]

        page_info = PageInfo(raw_data[1])

        return Page(comments, page_info)

    def get_comment_history(
        self, user_id: int, page: int = 0, mode: int = 0, count: int = 20
    ) -> Page[LevelHistoryComment]:
        """Gets a user's comment history.

        Arguments:
            user_id (int): The userID of the user whose history to fetch
            page (int)
            mode (int): 0 = Most recent, 1 = Most liked. Defaults to 0
            count (int): The number of comments to get. Capped at 100

        Returns:
            CommentPage
        """
        # TODO FIXME: What does this return when the user has comments disabled?
        # Probably -1

        response = self.client.gd_post(
            "getGJCommentHistory",
            data={"userID": user_id, "page": page, "mode": mode, "count": count},
        )

        raw_data = response.split("#")

        comments: list[LevelHistoryComment] = [
            self._parse_level_comment(LevelHistoryComment, comment)  # type: ignore
            for comment in raw_data[0].split("|")
        ]

        page_info = PageInfo(raw_data[1])

        return Page(comments, page_info)  # type: ignore

    def get_comments(
        self, level_id: int, page: int = 0, mode: int = 0, count: int = 10
    ) -> Page[LevelComment]:
        """Gets a level or list's comments.

        Arguments:
            level_id (int): The ID of the level or list. Negative if it's a list ID
            page (int)
            mode (int): 0 = Most recent, 1 = Most liked. Defaults to 0
            count (int): Number of comments to fetch. Defaults to 10

        Returns:
            CommentPage
        """
        response = self.client.gd_post(
            "getGJComments21",
            data={"levelID": level_id, "page": page, "mode": mode, "count": count},
        )

        raw_data = response.split("#")

        comments: list[LevelComment] = [
            self._parse_level_comment(LevelComment, comment)  # type: ignore
            for comment in raw_data[0].split("|")
        ]

        page_info = PageInfo(raw_data[1])

        return Page(comments, page_info)  # type: ignore

    def upload_account_comment(self, comment: str) -> Annotated[int, "commentID"]:
        """Posts an account comment

        Arguments:
            comment: str

        Returns:
            int: comment ID if the comment was successfully posted
        """
        self.client.check_logged_in()

        # TODO: Generate chk, save userName to extra_data, test cType
        # TODO: Does the server or client enforce max/min comment length?

        comment_b64 = urlsafe_b64encode(comment.encode()).decode()

        data = {
            "comment": comment_b64,
            "cType": 1,
            "chk": utils.generate_chk(
                (
                    self.client.saved_data["userName"],
                    comment_b64,
                    0,  # LevelID, or 0 in case of account comments
                    0,  # Percentage, or 0 in case of account comments
                    1,  # cType
                ),
                XORKeys.COMMENT,
            ),
        }

        print(data)
        response = self.client.gd_post("uploadGJAccComment20", data)

        return int(response)

    def upload_comment(
        self, comment: str, level_id: int, percent: int = 0
    ) -> Annotated[int, "commentID"]:
        """Uploads a comment to a user level.

        Arguments:
            comment (str): The comment's message
            level_id (int): The ID of the level to comment on. If commenting on a list, the ID should be negative
            percent (int, optional): Percentage progress on the level
        """
        self.client.check_logged_in()

        data: dict = {
            "levelID": level_id,
            "comment": urlsafe_b64encode(comment.encode()).decode(),
            "userName": self.client.saved_data["userName"],
        }

        if percent != 0:
            data["percent"] = percent

        data["chk"] = utils.generate_chk(
            (
                data["userName"],
                data["comment"],
                level_id,
                percent,
                0,  # 0 for level comment
            ),
            XORKeys.COMMENT,
        )

        response = self.client.gd_post("uploadGJComment21", data)

        return int(response)
