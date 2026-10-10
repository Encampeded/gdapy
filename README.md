# GDA.py

A simple yet powerful Python Geometry Dash API Wrapper.

> [!WARNING]
> This library is **extremely** unfinished; many endpoints are missing, have an unfinished implementation, or are otherwise untested. PROCEED WITH CAUTION!

## Basic Usage

```py
from gdapy import GDClient

client = GDClient()

results = client.levels.get_levels("retray")

retray = client.levels.download_level(results.levels[0].level_id)



```

## TODO

**CURRENT PRIORITY:**
- Refactor gd_objects; use attrs + object_gen, and for any additional parameters, move them to @property
  - Implement levels.get_level_scores when done with users endpoints

**Features to Impement:**
- Reimplement SearchFilters
- Unify KEYs, and (maybe?) make dictionary keys ints instead of strings
- Logging:
  - warn on unknown keys (name UNKNOWNKEY_32) instead of raising an error
  - warn on extra fields
- Would be nice if properties could be included in gd_objects repr

**General Chores:**
- Standardize imports and __init__.py
- List comprehensions for from_string: if input could be empty, add if object, 
  as "".split("|") returns [""] for... reasons.
- Add docstrings for methods missing them
- Use GDTuple for lists of set numbers of values (ex RGB values)
- Support setting a timezone for datetime.fromtimestamp
- Should objects.py use tuples instead of lists?

**For the Future:**
- asyncio support; pretty important, but i really want to make it optional in some way...
- TESTING:
  - Inherit from GDObject, overwriting gd_post to return cached responses based on endpoint



- Merge enums and endpoint_objects
  - User-used enums should be in enums (function parameters/object fields)
  - Any others should be in endpoint objects
- Replace const lists with tuples

- Figure out a place for key.py; should probably replace the KEY.py in gdapy with the one with object_gen, but the tuple situation will cause issues

- Standardize response objects in endpoint_objects being the PascalCase of their corresponding endpoint + Response (ex GetUserResponse)



## Contributing

### Program Flow
1. Call endpoint method
2. Endpoint method parses arguments and calls gd_post
3. If response is negative number, gd_post raises an GDServerError exception (will eventually be replaced with per-endpoint exceptions)
4. Endpoint method takes the raw_string response and parses it into a response
5. If it's a gd_object, utils.parse_object turns it into a gd_object

### Project Structure
`gdapy/enums`
- Contains any enums used by the user; function parameters and object attributes

`gdapy/endpoints`<br>
- Contains endpoint classes used by client.py
- Should contain the implementation; the user shouldn't import anything from this folder.
- Endpoint methods should copy the actual php endpoint names, however with "GJ" and any numbers removed, and in snake_case.

`gdapy/endpoints/gd_objects`<br>
Contains `gd_object` implementations<br>
Objects should inherit from base `gd_object`, and if any attributes require cleanup (decoding an encoded string, second example), implement a `_clean()` method (which should call `super()._clean()` at the end!)<br>

`gdapy/endpoints/endpoint_objects`<br>
Contains structured objects/enums returned by endpoint methods


### General Style
- Use double quotes for longer strings, and single quotes for character-like strings
- Explicit is better than Implicit; please avoid writing deeply-nesting tiny functions. A good example of this (in my opinion) would be the former gd.py library. I would much prefer readable code that repeats a bit to... that.
- This is my first time taking on a project of this scale, so if something seems off or strange, it may not be intentional. Free free to let me know, or fix it yourself, or don't :shrug:
