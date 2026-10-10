from typing import ClassVar, Self

from attrs import define, field
from pyheck import snake

from ...utils import to_dictionary
from .gd_converter import gd_converter


def to_snake(name: str) -> str:
    snake_case: str = snake(name)

    if snake_case.endswith("_i_ds"):
        snake_case = snake_case.removesuffix("_i_ds") + "_ids"

    return snake_case


@define
class GDObject:
    raw_dict: dict = field(repr=False)
    object_type: ClassVar[str]

    @classmethod
    def from_string(cls, raw_data: str, delimiter: str = ":") -> Self:
        try:
            raw_dict = to_dictionary(cls.object_type, raw_data, delimiter)
        except ValueError as e:
            print(f'"{raw_data}"')
            raise ValueError(f"{raw_data}\nGot ValueError parsing above data:\n{e}")

        raw_dict["rawDict"] = raw_dict.copy()  # type: ignore

        cleaned_dict = cls._clean(raw_dict)

        object = gd_converter.structure(cleaned_dict, cls)

        return object

    @classmethod
    def _clean(cls, raw_dict: dict) -> dict:
        return {to_snake(k): v for k, v in raw_dict.items()}
