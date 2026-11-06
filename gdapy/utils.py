import random
import string
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

def generate_rewards_chk(user_id: int, xor_key: XORKeys):
    m_chk = int((user_id / 10000.0) + random.randint(0, 1000000))

    chk_string: str = gd_xor_cipher(str(m_chk), xor_key)
    encoded_chk: str = urlsafe_b64encode(chk_string.encode()).decode()

    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    return random_string + encoded_chk
    # this->m_chk = static_cast<int>(this->m_playerUserID/10000.0f + rand()/RAND_MAX * 1000000.0f);
    # auto chkString = std::format("{}", GameManager::sharedState()->m_chk);
    # auto encodedChk = cocos2d::ZipUtils::base64EncodeEnc(chkString, "19847");
    # // gen_random(n) returns a random string of length n using the alphabet [a-zA-Z0-9]
    # auto chkParam = std::format("chk={}{}", gen_random(5), encodedChk);


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
