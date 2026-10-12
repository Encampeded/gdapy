from attrs import define

from ..gd_objects.list import SearchList
from ..gd_objects.user import TinyUser
from .page import PageInfo


@define
class GetListsResponse:
    """Represents a response from getGJLevels21.php

    Attributes:


    """

    lists: list[SearchList]
    creators: list[TinyUser]
    page_info: PageInfo
