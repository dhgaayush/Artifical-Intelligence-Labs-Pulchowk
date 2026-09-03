ROWS = 20
COLS = 40

EMPTY = 0
OBSTACLE = 1
PAINTED = 2


def make_room():
    room = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    return room


def count_empty(room):
    return sum(cell == EMPTY for row in room for cell in row)


room = make_room()

print("Rows:", len(room))
print("Columns:", len(room[0]))
print("Paintable cells:", count_empty(room))