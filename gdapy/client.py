from random import randint
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import uuid4

from .endpoints import (
    AccountsEndpoints,
    CommentsEndpoints,
    LevelsEndpoints,
    ListsEndpoints,
    SongsEndpoints,
    UsersEndpoints,
)
from .enums.misc import Platform, Secrets
from .errors import GDServerError, NotLoggedInError
from .utils import is_integer

# msgspec.convert(dict, type=Level)
# userID and accountID
# NOT playerID. playerID is FAKE PROPAGANDA made up by GDDocs!!!!1!1 (and colon ngl i think)
# userName, not username, as "In 2.2, the userName and password fields were replaced with accountID and gjp2."
# Robtop himself uses userName
# downloadGJLevel:


class GDClient:
    def __init__(self):
        self.levels = LevelsEndpoints(self)
        self.accounts = AccountsEndpoints(self)
        self.comments = CommentsEndpoints(self)
        self.users = UsersEndpoints(self)
        self.songs = SongsEndpoints(self)
        self.lists = ListsEndpoints(self)

        self.logged_in: bool = False

        self.saved_data: dict = {}

        self.common_data: dict = {
            # Some endpoints check for a minimum binaryVersion,
            # but we can just set ours really high and it works lol
            "gameVersion": 128,
            "binaryVersion": 128,
            # If logged in:
            # "accountID": 1234,
            # "gjp2": "********",
            # "uuid": userID
            # "udid": f"NoUDID_{random.randint(0, 1000000000)}"
        }

    def set_new_udid(self, platform: Platform = Platform.WINDOWS) -> None:
        """Generates and sets a new UDID for API requests."""
        udid: str

        match platform:
            case Platform.WINDOWS:
                udid = f"NoUDID_{randint(0, 1000000000)}"

            case Platform.ANDROID:
                udid = str(uuid4())

            case _:
                raise NotImplementedError(
                    "Only Android and Windows UDIDs are supported presently!"
                )

        self.common_data["udid"] = udid

    def gd_post(
        self, endpoint: str, data: dict | None = None, secret: Secrets = Secrets.COMMON
    ) -> str:
        """Makes a properly formatted post request to the gd servers using provided endpoint and data"""
        if data is None:
            data = {}

        data["secret"] = secret.value
        data |= self.common_data

        url = (
            endpoint
            if endpoint.startswith("https://")
            else f"http://www.boomlings.com/database/{endpoint}.php"
        )

        request = Request(
            url=url,
            method="POST",
            data=urlencode(data).encode("utf-8"),
            headers={"User-Agent": ""},
        )

        # Should raise an exception in case of a non-200 code
        response = urlopen(request)

        response_text: str = response.read().decode("utf-8")

        if is_integer(response_text) and response_text.startswith("-"):
            raise GDServerError(int(response_text))

        return response_text

    def check_logged_in(self):
        if not self.logged_in:
            raise NotLoggedInError()
