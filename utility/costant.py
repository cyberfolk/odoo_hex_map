BORDERS_MAP = {
    1: [2, 3, 4, 5, 6, 7],
    2: [8, 9, 3, 1, 7, 19],
    3: [9, 10, 11, 4, 1, 2],
    4: [3, 11, 12, 13, 5, 1],
    5: [1, 4, 13, 14, 15, 6],
    6: [7, 1, 5, 15, 16, 17],
    7: [19, 2, 1, 6, 17, 18],
    8: [0, 0, 9, 2, 19, 0],
    9: [0, 0, 10, 3, 2, 8],
    10: [0, 0, 0, 11, 3, 9],
    11: [10, 0, 0, 12, 4, 3],
    12: [11, 0, 0, 0, 13, 4],
    13: [4, 12, 0, 0, 14, 5],
    14: [1, 2, 3, 4, 5, 6],
    15: [6, 5, 14, 0, 0, 16],
    16: [17, 6, 15, 0, 0, 0],
    17: [18, 7, 6, 16, 0, 0],
    18: [0, 19, 7, 17, 0, 0],
    19: [0, 8, 2, 7, 18, 0],
}

EXTERNAL_BORDERS_MAP = {
    2: {
        "border_N": ("border_N", 14)},
    3: {
        "border_NE": ("border_NE", 16)},
    4: {
        "border_SE": ("border_SE", 18)},
    5: {
        "border_S": ("border_S", 8)},
    6: {
        "border_SW": ("border_SW", 10)},
    7: {
        "border_NW": ("border_NW", 12)},
    8: {
        "border_N": ("border_N", 5),
        "border_NE": ("border_N", 13),
        "border_NW": ("border_N", 15)},
    9: {
        "border_N": ("border_N", 13),
        "border_NE": ("border_NE", 17)},
    10: {
        "border_N": ("border_NE", 17),
        "border_NE": ("border_NE", 6),
        "border_SE": ("border_NE", 15)},
    11: {
        "border_NE": ("border_NE", 15),
        "border_SE": ("border_SE", 19)},
    12: {
        "border_NE": ("border_SE", 19),
        "border_SE": ("border_SE", 7),
        "border_S": ("border_SE", 17)},
    13: {
        "border_SE": ("border_SE", 17),
        "border_S": ("border_S", 9)},
    14: {
        "border_SE": ("border_S", 9),
        "border_S": ("border_S", 2),
        "border_SW": ("border_S", 19)},
    15: {
        "border_S": ("border_S", 19),
        "border_SW": ("border_SW", 11)},
    16: {
        "border_S": ("border_SW", 11),
        "border_SW": ("border_SW", 3),
        "border_NW": ("border_SW", 9)},
    17: {
        "border_SW": ("border_SW", 9),
        "border_NW": ("border_NW", 13)},
    18: {
        "border_N": ("border_NW", 11),
        "border_SW": ("border_NW", 13),
        "border_NW": ("border_NW", 4)},
    19: {
        "border_N": ("border_N", 15),
        "border_NW": ("border_NW", 11)},
}
