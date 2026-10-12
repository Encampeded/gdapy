# GDA.py

A simple yet powerful Python Geometry Dash API Wrapper built around attrs/cattrs.

> [!WARNING]
> This library is **unfinished**; many endpoints are missing, have an unfinished implementation, or are otherwise untested. PROCEED WITH CAUTION!

Huge thanks to the [gd-docs](boomlings.dev) project for providing the documentation that made this possible.

## Example Usage

```py
>>> from gdapy import GDClient
>>>
>>> client = GDClient()
>>>
>>> response = client.levels.get_levels(query = "ReTraY")
>>> for level in response.levels:
...     print(level.name, '-' level.rating)
...
ReTraY - Featured
ReTraY 2018 - Unrated
Retray 2019 - Featured
ReTrAy Bird - Unrated
ReTraY Clicks Chal - Unrated
ReTraY Full Ver - Unrated
ReTraY 2P - Unrated
ReTraY 2018 - Unrated
ReTraY  - Unrated
Retray V2 - Unrated
>>> retray_search_result = response.levels[0]
>>> # Many objects include property wrappers for otherwise obtuse values.
>>> retray_search_result.difficulty
'Easy'
>>> retray_search_result.game_version_semantic
2.1
>>> response = client.levels.download_level(response.levels[0].id)
>>> response
DownloadLevelResponse(
    level=DownloadLevel(
        id=6508283,
        name='ReTraY',
        description='Thanks for playing Geometry Dash',
        level_string='kS38,1_0_2_0_3_0_4_-1_6_1000_7_1_15_0_18_0_8_1|1_0_2_0_3_0_4_-1_...',
        version=3, user_id=4993756, difficulty_denominator=10, difficulty_numerator=10,
        downloads=137366401, official_song=0, game_version=21, likes=9191479, 
        length=3, demon=False, stars=2, feature_score=2619, auto=False, password=1532211,
        upload_date='11 years', update_date='7 years', copied_id=0, two_player=False,
        custom_song_id=557117, extra_string='0_733_0_0_0_0_574_716_0_0_352_78_729_0_42_0_833_68_0_347_0_38_240_205_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0',
        coins=3, verified_coins=True, stars_requested=2, low_detail_mode=False, epic=0,
        demon_difficulty=3, objects=20000, exact_upload_time=datetime.datetime(2015, 4, 15, 9, 47, 35),
        exact_update_time=datetime.datetime(2019, 7, 7, 12, 46, 52), editor_time=13773,
        editor_time_copies=None, song_ids=None,  sfx_ids=None, song_size=None, verification_time=0
    ),
    user=None,
    songs=[],
    extra_artist_names=[],
    extra_data='1000;3;#0;#'
)
>>> # Above manually wrapped for your viewing convenience.
>>> account_id = client.accounts.log_in("Encamped", "***********")
>>> comment_id = client.comments.upload_comment("I love ReTraY!", response.level.id)
>>> # Nevermind...
>>> client.comments.delete_comment(comment_id, retray.level.id)
>>> client.accounts.log_out()
```

For more examples, see the documentation.

> [!WARNING]
> The documentation does not presently exist!

Alternatively, look around using autocomplete, for basic api usage.

## Contributing

Wow, I'm flattered. The following sections specify general code-stuffs for the library, mostly for my own sanity when I inevitably return to this project after a months-long break and have no idea what I'm doing, but also, I suppose, for the contributer that may or may not exist!

### Program Flow
1. Endpoint method called
2. Method parses arguments and calls GDClient.gd_post()
3. If response is negative number, gd_post raises an GDServerError exception (will eventually be replaced with per-endpoint exceptions)
4. Endpoint method takes the raw_string response and parses it into a response, possibly from endpoint_objects
5. If it's a gd_object, GDObject.from_string(raw_object_str) turns it into a gd_object

### Project Structure
`gdapy/enums`
- Contains any enums used by the user; generally endpoint parameters; object attribute enums should be in endpoint_objects

`gdapy/endpoints`
- Contains endpoint classes used by client.py
- Should contain the implementation; the user shouldn't import anything from this folder.
- Endpoint methods should copy the actual php endpoint names, however with "GJ" and any numbers removed, and in snake_case.

`gdapy/endpoints/gd_objects`
- Contains `gd_object` implementations
  - Objects should inherit from a base Object class (ex Song, Level, etc) `gd_object` that defines the object_type ClassVar
    - If any attributes require cleanup (mainly just decoding a specially encoded string), implement a `_clean()` method (which should call `super()._clean()` at the end!)
    - 
  - Object fields are defined in `object_gen/objects.py`; **they should not be manually edited**.
  - If you want a convenience field (ex difficulty: str, instead of difficulty denominator/numerator), implement them as a property.

`gdapy/endpoints/endpoint_objects`
- Contains structured response objects returned by endpoint methods

`object_gen`
- Contains code for generating gd_objects from lists of int keys

### General Style
- I use ruff to format files. Would recommend.
- Use double quotes, save for where a string includes double quotes, in which case use single.
- Explicit is better than Implicit; please avoid writing deeply-nesting tiny functions. A good example of this (in my opinion) would be the former gd.py library. I would much prefer readable code that repeats a bit to... that.
- This is my first time taking on a project of this scale, so if something seems off or strange, it may not be intentional. Free free to let me know, or fix it yourself, or don't :shrug:
