ROWS = 20
COLS = 40

EMPTY = 0
OBSTACLE = 1
PAINTED = 2

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


def read_cell(room, row, col):
    # Outside the room is treated like an obstacle.
    if row < 0 or row >= ROWS:
        return OBSTACLE

    if col < 0 or col >= COLS:
        return OBSTACLE

    return room[row][col]


def get_observation(room, row, col, direction):
    current = read_cell(room, row, col)

    forward_direction = direction
    left_direction = (direction - 1) % 4
    right_direction = (direction + 1) % 4

    forward_row = row + DIRECTIONS[forward_direction][0]
    forward_col = col + DIRECTIONS[forward_direction][1]

    left_row = row + DIRECTIONS[left_direction][0]
    left_col = col + DIRECTIONS[left_direction][1]

    right_row = row + DIRECTIONS[right_direction][0]
    right_col = col + DIRECTIONS[right_direction][1]

    forward = read_cell(room, forward_row, forward_col)
    left = read_cell(room, left_row, left_col)
    right = read_cell(room, right_row, right_col)

    return [current, forward, left, right]


room = make_room()

# Place one obstacle directly in front of the robot.
room[10][21] = OBSTACLE

row = 10
col = 20
direction = 1  # east

print("Observation before painting:")
print(get_observation(room, row, col, direction))

room[row][col] = PAINTED

print("Observation after painting:")
print(get_observation(room, row, col, direction))