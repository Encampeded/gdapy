import os
import re
from pathlib import Path

from attrs import evolve
from key import KEY
from objects import OBJECTS

# FIXME: Pretty sure this only works on linux...
PATH_LIBRARY = Path(__file__).resolve().parent.parent / "gdapy"
PATH_OBJECTS = PATH_LIBRARY / "endpoints" / "gd_objects"
PATH_KEY     = PATH_LIBRARY / "key.py"

## BEGIN AUTO GENERATED FIELDS
## END AUTO GENERATED FIELDS

# ------------------------------------- #

RE_OBJECT_TYPE = r"object_type = \"(.*?)\""

FIELDS_BEGIN = "    ## BEGIN AUTO GENERATED FIELDS"
FIELDS_END = "    ## END AUTO GENERATED FIELDS"
RE_CLASS = (
    rf"(?s)class ([a-zA-Z]+)\(([a-zA-Z,=_\s]*)\):\n+{FIELDS_BEGIN}\n(.*?){FIELDS_END}"
)


def generate_fields(object_type: str, keys: list[int]) -> str:
    fields: str = ""

    keys = [k for k in keys if k > 0] + [k for k in keys if k < 0]
    # print(keys)

    for int_key in keys:
        field = KEY[object_type][str(abs(int_key))]

        if int_key < 0:
            field = evolve(
                field,
                type=field.type_to_str() + " | None",
                field_values={**field.field_values, "default": None},
            )

        fields += field.to_line()

    return fields


# TODO: Clean up variable names here
for object_filename in os.listdir(PATH_OBJECTS):
    if not object_filename.endswith(".py"):
        continue

    object_path = PATH_OBJECTS / object_filename

    with open(object_path, "r") as f:
        file = f.read()

    # classes: Iterator[re.Match] = re.finditer(RE_CLASS, file)

    # if not classes:
    #     print("    Skipping", object_filename)
    #     continue

    object_type_match = re.search(RE_OBJECT_TYPE, file)

    if object_type_match is None:
        continue

    print("\nFound", object_filename)

    object_type: str = object_type_match.group(1)

    def rewrite_fields(match: re.Match) -> str:
        full_match: str = match.group(0)

        object_name: str = match.group(1)
        print("    Writing", object_name)

        if object_name not in OBJECTS[object_type]:
            print(OBJECTS[object_type])
            print(f"            Missing fields for {object_name}! Skipping...")
            return full_match

        new_fields = generate_fields(object_type, OBJECTS[object_type][object_name])

        # Remove fields that would be inherited from parent class. Doesn't seem entirely necessary
        # for variant in OBJECTS[object_type]:
        #     if variant in match.group(2):
        #         keys = list(set(keys) - set(OBJECTS[object_type][variant]))
        # file = file.replace(fields, generate_fields(object_type, keys))

        # Modified AI code, because im in pain im sorry

        start, end = match.span(3)
        match_start, _ = match.span(0)

        # Reconstruct the match with the specific group replaced
        # print(full_match[:start - match_start] + new_fields + full_match[end - match_start:])
        return (
            full_match[: start - match_start]
            + new_fields
            + full_match[end - match_start :]
        )

    file = re.sub(RE_CLASS, rewrite_fields, file)

    # print(file)
    # continue

    print("        Writing file...")
    with open(object_path, "w") as f:
        f.write(file)
    print("    Done!")

print("\nUpdating key...")

new_key: dict[str, dict[str, str]] = {
    object_type: {k: v.get_key_name() for k, v in mappings.items()}
    for object_type, mappings in KEY.items()
}

new_key_file: str = f"""# Auto generated from object_gen/generator.py using object_gen/key.py

KEY = {new_key}"""

with open(PATH_KEY, "w") as f:
    f.write(new_key_file)

print("    Done!")
