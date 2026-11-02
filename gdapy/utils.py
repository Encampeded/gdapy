from base64 import urlsafe_b64decode, urlsafe_b64encode
from collections.abc import Iterable
from hashlib import sha1
from itertools import batched

from .enums import Salts, XORKeys
from .key import KEY


def gdb64_decode(encoded_string: str) -> str:
    return urlsafe_b64decode(encoded_string.encode()).decode()


def to_dictionary(type: str, raw_data: str, delimiter: str = ":") -> dict[str, str]:
    """Converts a geometry dash `key:value` object to a dictionary.

    Arguments:
        type (str): The object type, as appears in KEY
        raw_data (str): The raw `key:value` object
        delimiter (str): The delimeter between key/values

    Returns:
        dict[str, str]
    """
    try:
        return {  # TODO: When we unify key, make KEY[type][int(key)].name
            KEY[type][key]: value
            for key, value in batched(raw_data.split(delimiter), 2)
        }  # this is so clean i love python

    except KeyError as e:
        raise KeyError(
            f"{raw_data}\nGot following KeyError (likely undocumented key) parsing above data:\n{e}"
        )


def gd_xor_cipher(input: str, key: XORKeys) -> str:

    if key == XORKeys.SAVE_DATA:
        return "".join(chr(ord(char) ^ key) for char in input)

    key_str = str(key.value)

    return "".join(
        chr(ord(char) ^ ord(key_str[i % len(key_str)])) for i, char in enumerate(input)
    )


def gd_sha1(hash_string: str, salt: str = ""):
    return sha1((hash_string + salt).encode()).hexdigest()


def generate_chk(values: Iterable, key: XORKeys, salt: str = "") -> str:

    # FIXME: This is so ugly lmao
    # I'll fix it when implementing more chks though
    if not salt:
        match key:
            case XORKeys.COMMENT:
                salt = Salts.COMMENT

    hash_string: str = "".join(map(str, values))

    hashed: str = gd_sha1(hash_string, salt)

    xored: str = gd_xor_cipher(hashed, key)

    final = urlsafe_b64encode(xored.encode()).decode()

    return final


def check_hash(hash_string: str, server_hash: str, salt: str = "xI25fpAapCQg"):
    """Adds salt to provided plaintext, SHA1 hashes it, and checks against provided server hash."""

    local_hash = gd_sha1(hash_string, salt)

    if local_hash != server_hash:
        print(
            f"{local_hash} (Locally Generated Hash)\n{server_hash} (Server Provided Hash)"
        )
        raise ValueError(
            "Hash doesn't match. Either try again or check your connection."
        )


def is_integer(response: str) -> bool:
    try:
        int(response)
        return True
    except ValueError:
        return False


def present_keys(raw_object, delimiter: str = ":") -> list[int]:
    """Returns keys present in string object. Helpful for debugging object variants returned from the servers."""
    return sorted(map(int, raw_object.split(delimiter)[::2]))


def print_keys(keys: set[int]):
    for key in range(1, max(keys) + 1):
        if key in keys:
            print(f"{key:02d} ", end="")
        else:
            print("   ", end="")
    print()
