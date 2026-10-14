from base64 import urlsafe_b64decode
from collections.abc import Callable
from datetime import datetime
from types import NoneType, UnionType
from typing import Any, get_args, get_origin

from cattrs import Converter

from ...enums.gd_enum import GDEnum
from .gd_types import B64String

gd_converter = Converter(forbid_extra_keys=True, use_alias=True)


@gd_converter.register_structure_hook
def bool_structure_hook(value: Any, t: Any) -> bool:
    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise TypeError(
            f"Got neither bool nor str for bool structure hook? {value} of type {type(value)}"
        )

    if value.isnumeric():
        return bool(int(value))

    if not value:
        return False

    raise TypeError(f'Got unknown boolean value! "{value}"')


@gd_converter.register_unstructure_hook
def bool_unstructure_hook(value: bool) -> int:
    return int(value)


def gd_list_structure_hook(value: str, t: type) -> list:
    args = get_args(t)
    list_type = args[0] if args else str

    return [list_type(e) for e in value.split(",")]


gd_converter.register_structure_hook_func(
    check_func=lambda t: get_origin(t) is list, func=gd_list_structure_hook
)


@gd_converter.register_unstructure_hook
def gd_list_unstructure_hook(value: list) -> str:
    return ",".join(map(str, value))


@gd_converter.register_structure_hook
def b64_string_structure_decode_hook(value: str, _) -> B64String:
    return B64String(urlsafe_b64decode(value.encode()).decode())


@gd_converter.register_structure_hook
def datetime_structure_hook(value: str, _) -> datetime:
    return datetime.fromtimestamp(int(value))


@gd_converter.register_structure_hook
def gd_enum_structure_hook(value: str, t) -> GDEnum:
    return t(int(value))


# Hook factory for: T | None types, where empty string evaluates to None.
@gd_converter.register_structure_hook_factory(
    lambda convert_to: (
        (get_origin(convert_to) is UnionType) and (NoneType in get_args(convert_to))
    )
)
def optional_hook_factory(optional: Any | None, converter: Converter) -> Callable:

    def optional_hook(value: str, _) -> Any | None:
        if value == "":
            return None

        return converter.structure(value, get_args(optional)[0])

    return optional_hook
