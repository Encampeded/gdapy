# gdapy

A simple yet powerful Geometry Dash API Wrapper written in Python.

> [!WARNING]
> This library is **unfinished**. Many endpoints are missing, have incomplete implementation, or are otherwise untested. PROCEED WITH CAUTION!

Huge thanks to the [gd-docs](boomlings.dev) project for providing the documentation that made this possible.

## Example Usage

```py
>>> from gdapy import GDClient
>>> import rich # for pretty printing
>>>
>>> client = GDClient()
>>>
>>> search_results = client.levels.get_levels(query="loco motive")
>>> search_results.page_info
PageInfo(1 to 10 of 9999)
>>>
>>> for level in search_results.levels:
...     print(level.name, '-', level.id)
...
Loco Motive - 97598449
Loco Motive meme - 97846910
loco motive - 93798744
Loco Motive auto - 97803866
Loco Motive Practice - 98444782
Loco Motive bad - 98084107
Loco Motive 2 - 97990163
Loco Motive Easy - 97647550
Loco Motive 2 - 98292665
Loco Motive but - 97638201
>>>
>>> downloaded_response = client.levels.download_level(search_results.levels[0].id)
>>> rich.print(downloaded_response)
DownloadLevelResponse(
    level=DownloadLevel(
        difficulty='Harder',
        rating='Epic',
        game_version_semantic=2.2,
        id=97598449,
        name='Loco Motive',
        description='Yee                                                                      Haw',
        level_string='kS38,1_255_2_195_3_26_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_...',
        version=2,
        user_id=8599996,
        difficulty_denominator=10,
        difficulty_numerator=<DifficultyNumerator.HARDER: 40>,
        downloads=4498275,
        official_song=<OfficialSong.STEREO_MADNESS: 0>,
        game_version=22,
        likes=190744,
        length=<LevelLength.PLATFORMER: 5>,
        demon=False,
        stars=6,
        feature_score=33391,
        auto=False,
        password=1,
        upload_date='2 years',
        update_date='2 years',
        copied_id=0,
        two_player=False,
        custom_song_id=1204676,
        extra_string='25,328,58,230,76,373,82,980',
        coins=0,
        verified_coins=False,
        stars_requested=6,
        low_detail_mode=False,
        epic=<EpicRating.EPIC: 1>,
        demon_difficulty=<LevelDemonDifficulty.INSANE_DEMON: 5>,
        objects=18374,
        exact_upload_time=datetime.datetime(2023, 12, 21, 14, 19, 6),
        exact_update_time=datetime.datetime(2023, 12, 21, 16, 17),
        daily_number=None,
        editor_time=87320,
        editor_time_copies=0,
        song_ids=[1204676],
        sfx_ids=[386, 463, 477, 1202, 1224, 1565, 1750, 2051, 2385, 2559, 2629, 2981, 3081, 3308, 3309, 3310, 3313, 3581, 4083, 4112, 4117, 4118, 4397, 6010, 6044, 6045, 6398, 6405, 6543, 6780, 7379, 9553, 9680, 9681, 13154, 13727, 14059],
        song_size=8167092,
        verification_time=19959
    ),
    user=None,
    songs=[
        LevelSong(
            id=1204676,
            name='Hide n Seek Ranch',
            artist_id=15747,
            artist_name='PuffballsUnited',
            size=6.34,
            video_id='',
            youtube_url='',
            is_verified=False,
            link='https%3A%2F%2Faudio.ngfiles.com%2F1204000%2F1204676_Hide-n-Seek-Ranch.mp3%3Ff1680307735',
            download_soundtrack_override='',
            nong_enum=None,
            extra_artist_ids=None,
            new=None,
            artist_links=None
        )
    ],
    extra_artist_names=[],
    extra_data='0;2;H4sIAAAAAAAAA91ZWbLlNgjdkD-EAA2VrWXxYZB1LcTbQKor3XWPEWI4DHbq...'
)
>>>
>>> account_id = client.accounts.log_in("Encamped", "***********")
>>> comment_id = client.comments.upload_comment("I love this level!", downloaded_response.level.id)
>>> # Nevermind...
>>> client.comments.delete_comment(comment_id, retray.level.id)
>>> client.accounts.log_out()
```

For more examples, see the documentation.

> [!WARNING]
> The documentation does not presently exist!

## Contributing

Wow, I'm flattered. The following sections specify general code-stuffs for the library, mostly for my own sanity when I inevitably return to this project after a months-long break and have no idea what I'm doing, but also, I suppose, for the contributer that may or may not exist!

### Program Flow
1. Endpoint method called
2. Method parses arguments and calls `GDClient.gd_post()`
3. If response is negative number, `gd_post()` raises a `GDServerError` (will eventually be replaced with per-endpoint exceptions)
4. Endpoint method takes the raw string `response` and parses it; possibly (likely) structuring it into `gd_object`s (using `GDObject.from_string(raw_string)`) and an `endpoint_object`

### Project Structure
`gdapy/enums`
- Contains all and any gd enums
  - Endpoint parameters
  - Object attributes

`gdapy/endpoints`
- Contains endpoint classes used by client.py
- Should generally contain the implementation; the user shouldn't import anything from this folder*
  - *Save for complex endpoint parameters. See SearchFilters.
- Endpoint methods should copy the actual php endpoint names, however with "GJ" and any numbers removed, and in snake_case.

`gdapy/endpoints/gd_objects`
- Contains gd_objects (Level, User, etc.)
- Most object fields are defined in `object_gen/objects.py`
  - If you see `## BEGIN AUTO GENERATED FIELDS`, **do not edit the fields manually**.
  - Smaller classes, like MapPack, can be implemented manually
- Objects should inherit from a base Object class (ex Song, Level, etc) `gd_object` that defines the object_type ClassVar
  - If any attributes require cleanup (mainly just decoding a specially encoded string), implement a `_clean()` method (which should call `super()._clean()` at the end!)
- If you want a convenience field (ex difficulty: str, instead of difficulty denominator/numerator), set them as `field(init=False)` and set them in `__post_init__`

`gdapy/endpoints/endpoint_objects`
- Contains structured response objects returned by endpoint methods

`code_gen`
- Contains code for generating gd_objects and `gdapy/key.py` from `key.py` and `objects.py`

### General Style
- I use ruff to format files. Would recommend.
- Use double quotes, save for where a string includes double quotes, in which case use single.
- Explicit is better than Implicit; please avoid writing deeply-nesting tiny functions. A good example of this (in my opinion) would be the former gd.py library. I would much prefer readable code that repeats a bit to... that.
- This is my first time taking on a project of this scale, so if something seems off or strange, it may not be intentional. Free free to let me know, or fix it yourself, or don't :shrug:
