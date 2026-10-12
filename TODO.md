**Features to Impement:**
- Unify KEYs, and (maybe?) make dictionary keys ints instead of strings
  - Have generator also update KEY.py based on object_gen's key.py
- Logging:
  - warn on unknown keys (name UNKNOWNKEY_32) instead of raising an error
  - warn on extra fields
- Would be nice if properties could be included in gd_objects repr
- Could we add an OfficialSong enum?
- SearchType: aliases only on unstructure
- Use GDTuple for lists of set numbers of values (ex RGB values)


**General Chores:**
- GDObject.from_string() logic should probably be moved to gd_converter hooks
- Standardize imports and __init__.py
- List comprehensions for from_string: if input could be empty, add if object, 
  as "".split("|") returns [""] for... reasons.
- Add docstrings for methods missing them
- Support setting a timezone for datetime.fromtimestamp
- objects.py should use tuples instead of lists
- Parse artist_links for Song objects


**For the Future:**
- asyncio support
  - **__very important__**, but I really want it to be optional
  - unasync is an option, but seems wacky
  - What's painful is literally just gd_post needs to be awaited, but alas, async is like a virus
  - Honestly, generating async wouldn't be the most insane thing...?
    - It's just gd_post that needs to be async, which can be done manually
    - Then, the program can iterate over all the Endpoints classes, and make every method async and await gd_post using regex
- Tests!
  - Inherit from GDObject, overwriting gd_post to return cached responses based on endpoint
  - Also some script to generate and cache said responses
- Python 3.15:
  - sentinels for EMPTY vs None would be nice, for values that are present but empty
  - frozendict for dict function arguments instead of `if argument is None` boilerplate
  - Probably early to update though, and would limit the library's flexibility...

- Figure out a place for key.py; should probably replace the KEY.py in gdapy with the one with object_gen, but the tuple situation will cause issues
