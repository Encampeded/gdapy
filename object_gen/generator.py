import re
import os
from objects import OBJECTS
from key import KEY
from pyheck import snake

DIRECTORY = "/".join(__file__.split("/")[:-2]) + "/gdapy/endpoints/gd_objects"

## BEGIN AUTO GENERATED FIELDS
## END AUTO GENERATED FIELDS

# ------------------------------------- #

RE_OBJECT_TYPE = r"object_type = \"(.*?)\""

FIELDS_BEGIN = "    ## BEGIN AUTO GENERATED FIELDS"
FIELDS_END   = "    ## END AUTO GENERATED FIELDS"
RE_CLASS = rf"(?s)class ([a-zA-Z]+)\(([a-zA-Z,=_\s]*)\):\n+{FIELDS_BEGIN}\n(.*?){FIELDS_END}"

def generate_fields(object_type: str, keys: list[int]) -> str:
    fields: str = ""

    keys = [k for k in keys if k > 0] + [k for k in keys if k < 0]
    # print(keys)

    for int_key in keys:

        field = KEY[object_type][str(abs(int_key))]

        if int_key < 0:
            field = field._replace(
                type = field.type_to_str() + " | None",
                default = "None"
            )

        fields += field.to_line()

    return fields


# TODO: Clean up variable names here
for object_filename in os.listdir(DIRECTORY):
    if not object_filename.endswith(".py"):
        continue

    print("\nFound", object_filename)

    object_path = os.path.join(DIRECTORY, object_filename)

    with open(object_path, 'r') as f:
        file = f.read()

    # classes: Iterator[re.Match] = re.finditer(RE_CLASS, file)

    # if not classes:
    #     print("    Skipping", object_filename)
    #     continue

    object_type_match = re.search(RE_OBJECT_TYPE, file)

    if object_type_match is None:
        print("    Failed to find object_type in", object_filename)
        continue

    object_type: str = object_type_match.group(1)

    def rewrite_fields(match: re.Match) -> str:
        full_match: str = match.group(0)

        object_name: str = match.group(1)
        print("        Found", object_name)

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
        return full_match[:start - match_start] + new_fields + full_match[end - match_start:]

    file = re.sub(RE_CLASS, rewrite_fields, file)

    print("    Writing", object_filename)
    with open(object_path, 'w') as f:
        f.write(file)
    print("    Done!")

"""
open file
get object_type with RE_OBJECT_TYPE
match to RE_CLASS
for every match:

    keys = key[object_type][match[0]]
    for obj in key[object_type]:
        if obj in match[1]:
            keys -= key[object_type][obj]

    fields: str = gen_fields(object_type, keys)
    file.replace(match[2], fields)

---

matches = re.match(RE_CLASS_NAME)

if re.match(RE_CLASS_NAME):
    current_object = matched_name

if not FIELDS_BEGIN in current_line:
    continue

fields_end_index: int = next (FIELDS_END in line)
current_file[fields_begin_index:fields_end_index] = []

fields = [
    KEY[current_object][present_key]
    for present_key in objects[current_object]:
]

current_file.insert(fields_begin_index, fields)
i = fields_end_index
"""
# Groups:
#   1. ClassName
#   2. Inherits From
#   3. Fields (to replace)
