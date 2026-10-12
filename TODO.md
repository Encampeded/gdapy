**Features to Impement:**
- Unify KEYs, and (maybe?) make dictionary keys ints instead of strings
  - Have generator also update KEY.py based on object_gen's key.py
- Logging:
  - warn on unknown keys (name UNKNOWNKEY_32) instead of raising an error
  - warn on extra fields
- Would be nice if properties could be included in gd_objects repr
- Could we add an OfficialSong enum?
- SearchType: aliases only on unstructure

**General Chores:**
- Standardize imports and __init__.py
- List comprehensions for from_string: if input could be empty, add if object, 
  as "".split("|") returns [""] for... reasons.
- Add docstrings for methods missing them
- Use GDTuple for lists of set numbers of values (ex RGB values)
- Support setting a timezone for datetime.fromtimestamp
- Should objects.py use tuples instead of lists?
- Parse artist_links for Song objects

**For the Future:**
- asyncio support; pretty important, but i really want to make it optional in some way...
- Tests!
  - Inherit from GDObject, overwriting gd_post to return cached responses based on endpoint
  - Also some script to generate and cache said responses


- Figure out a place for key.py; should probably replace the KEY.py in gdapy with the one with object_gen, but the tuple situation will cause issues
