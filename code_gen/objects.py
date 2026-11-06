"""
!!HOW TO USE THIS FILE!!

Got a validation error?
- Extra Fields (in constructor for {Object}):
    - Find the new/unimplemented field's corresponding int key on gd-docs (or key.py) and add to the object
    - You might want to check if the field is optional (if it's only sometimes returned by the endpoint); if optional, make it negative

- Too many Fields:
    - Is the field still returned sometimes?
        - Find it's corresponding int key on gd-docs (or key.py), and set it to negative to make it optional
    - Is the field never returned by said endpoint anymore?
        - Delete the field from its list

"""

OBJECTS: dict[str, dict[str, list[int]]] = {

    "User": {
        "DownloadUser":      [1, 2, 3, 4, 8, 10, 11, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, -32, -35, -37, -38, -39, -40, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 67],
        "LevelLeaderboardUser": [1, 2, 3, 6,        9, 10, 11,-13, 14, 15, 16,             42, 51],
        "SearchUser":        [1, 2, 3, 4, 6,     8, 9, 10, 11, 13, 14, 15, 16, 17, 46,         51, 52],
        "LeaderboardUser":   [1, 2, 3, 4, 6, -7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 46,         51, 52],
        "FriendRequestUser": [1, 2,                 9, 10, 11,     14, 15, 16, 32, 35, 37, 41, 51],
        "CommentUser":       [1,                    9, 10, 11,     14, 15, 16, 51],
    },

    "Song": {
        "LevelSong":    [1, 2, 3, 4, 5, 6, 7, 8, 10, -11, -12, -13, 16,      -18],
        "DownloadSong": [1, 2, 3, 4, 5, 6, 7, 8, 10, -11, -12, -13, 16, -17, -18],
        "TopArtist":    [      3, 4,      -7,                                -18]
    },

    "Level": {
        "SearchLevel":   [1, 2, 3,    5, 6, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19, 25,             30, 31, 35,     37, 38, 39,          42, 43, 45,  46, -47],
        "DownloadLevel": [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19, 25, 27, 28, 29, 30, 31, 35, 36, 37, 38, 39, 40, -41, 42, 43, 45, -46, -47, -52, -53, -54, -57, 62, 63],
        "SearchList":    [1, 2, 3,    5, 7,       10,         14,            -19,         28, 29, 49, 50, 51, 55, 56]
    },

    "Comment": {
        "AccountComment":      [   2,    4, 6,    9,               15],
        "LevelComment":        [   2, 3, 4, 6, 7, 9, 10, -11, -12, 15],
        "LevelHistoryComment": [1, 2, 3, 4, 6,    9, 10, -11, -12, 15],
    },
}
