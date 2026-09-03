ROWS = 20
COLS = 40

EMPTY = 0
PAINTED = 2

# Direction numbers:
# 0 = north, 1 = east, 2 = south, 3 = west
DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]


def make_room():
    room = []

    for i in range(ROWS):
        row = []

        for j in range(COLS):
            row.append(EMPTY)

        room.append(row)

    return room


def paint_current(room, row, col):
    room[row][col] = PAINTED


def move_forward(row, col, direction):
    row_change = DIRECTIONS[direction][0]
    col_change = DIRECTIONS[direction][1]

    new_row = row + row_change
    new_col = col + col_change

    if new_row >= 0 and new_row < ROWS:
        if new_col >= 0 and new_col < COLS:
            return new_row, new_col

    return row, col


def count_painted(room):
    count = 0

    for i in range(ROWS):
        for j in range(COLS):
            if room[i][j] == PAINTED:
                count = count + 1

    return count


room = make_room()

row = 10
col = 20
direction = 1

paint_current(room, row, col)

for step in range(5):
    row, col = move_forward(row, col, direction)
    paint_current(room, row, col)

print("Final position:", row, col)
print("Painted cells:", count_painted(room))