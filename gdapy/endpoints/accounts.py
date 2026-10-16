from base64 import urlsafe_b64decode
from itertools import batched
from random import randint
from typing import TYPE_CHECKING, Annotated
from zlib import decompress

from .. import utils
from ..enums import Salts, Secrets
from .endpoint_objects import AccountSettings, SyncAccountResponse
from .gd_objects import BeatenLevel, BeatenMapPack

"""
UNIMPLEMENTED: update_acount_settings
"""

if TYPE_CHECKING:
    from ..client import GDClient


class AccountsEndpoints:
    def __init__(self, client: "GDClient"):
        self.client: GDClient = client

    # TODO: Find some way to test this works
    def backup_account_new(self, save_data: str) -> None:
        """Saves account data. BEWARNED: UNTESTED METHOD!

        Args:
            save_data (str): The save data for CCGameManager.dat and CCLocalLevels.dat, both compressed with gzip and separated by a semicolon `;`
        """
        print(
            "WARNING: This endpoint (update_account_settings) is untested! It may work, but it also may not! Bewarned..."
        )

        self.client.check_logged_in()

        response = self.client.gd_post(
            "https://robtopgames.org/database/accounts/backupGJAccountNew.php",
            {"saveData": save_data},
            Secrets.ACCOUNT,
        )

        # There should be no possible way that response isn't '1'
        assert response == "1"

    def login_account(
        self, udid: str, user_name: str, gjp2: str, steam_id: str = ""
    ) -> tuple[Annotated[int, "account_id"], Annotated[int, "user_id"]]:
        """Endpoint used to log in to a player's Geometry Dash account. You might want to use log_in() instead.

        Returns:
            tuple[int, int]: If request is successful, returns a tuple of the following format: (accountID, userID)
        """

        data = {"udid": udid, "userName": user_name, "gjp2": gjp2}

        if steam_id:
            data["sID"] = steam_id

        response = self.client.gd_post("accounts/loginGJAccount", data, Secrets.ACCOUNT)

        account_id, user_id = map(int, response.split(","))
        return (account_id, user_id)

    def log_in(
        self, username: str, password: str, udid: str = ""
    ) -> Annotated[int, "user_id"]:
        """Logs in using a given username and password, and saves credentials for further use.

        Returns:
            Annotated[int, "user_id"]
            If log in successful, returns user_id of account.
        """

        if not udid:  # truly amazing udid implementation rob
            udid = "NoUDID_" + str(randint(0, 1000000000))

        gjp2 = utils.gd_sha1(password, Salts.GJP2)

        response = self.login_account(udid, username, gjp2)

        account_id, user_id = response

        self.client.saved_data.update(
            {"userName": username.lower(), "uuid": account_id, "udid": udid}
        )

        self.client.common_data.update(
            {
                "accountID": account_id,
                "gjp2": gjp2,
            }
        )

        self.client.logged_in = True

        return user_id

    def log_out(self) -> None:
        """Logs out. Deletes all login information from extra_data and saved_data."""
        self.client.check_logged_in()

        for parameter in ("accountID", "gjp2"):
            self.client.common_data.pop(parameter)

        for parameter in ("userName", "uuid", "udid"):
            self.client.saved_data.pop(parameter)

        self.client.logged_in = False

    def register_account(self, username: str, password: str, email: str):
        """NOT IMPLEMENTED; replaced in 2.2 with register.php according to gddocs. Does this still work, or is it obsolete?"""
        raise NotImplementedError()

    def sync_account_new(self) -> SyncAccountResponse:
        """Loads account data if logged in

        Returns:
            SyncAccountResponse
        """
        self.client.check_logged_in()

        response = self.client.gd_post(
            "https://www.robtopgames.org/database/accounts/syncGJAccountNew.php",
            {},
            Secrets.ACCOUNT,
        )

        raw_data = response.split(";")

        # TODO: Decompress these for the user?
        save_CCGameManager = raw_data[0]
        save_CCLocalLevels = raw_data[1]

        game_version = int(raw_data[2])
        binary_version = int(raw_data[3])

        def decode(raw_data: str) -> str:
            return decompress(urlsafe_b64decode(raw_data[20:-20].encode())).decode()

        raw_levels = decode(raw_data[4])
        raw_map_packs = decode(raw_data[5])

        levels: list[BeatenLevel] = [
            BeatenLevel(int(level_id), int(stars))
            for level_id, stars in batched(raw_levels.split(","), 2)
        ]

        map_packs: list[BeatenMapPack] = [
            BeatenMapPack.from_string(raw_map_pack)
            for raw_map_pack in raw_map_packs.split("|")
        ]

        return SyncAccountResponse(
            save_CCGameManager=save_CCGameManager,
            save_CCLocalLevels=save_CCLocalLevels,
            game_version=game_version,
            binary_version=binary_version,
            levels=levels,
            map_packs=map_packs,
        )

    def update_account_settings(
        self, account_id: int, gjp2: str, settings: AccountSettings
    ):
        """NOT IMPLEMENTED"""
        raise NotImplementedError()
