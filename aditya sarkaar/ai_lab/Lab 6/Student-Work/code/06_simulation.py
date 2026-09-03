import random


ROWS = 20
COLS = 40

EMPTY = 0
OBSTACLE = 1
PAINTED = 2

# Direction numbers: north, east, south, west.
DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

# Actions stored in a chromosome gene.
NO_TURN = 0
TURN_LEFT = 1
TURN_RIGHT = 2
RANDOM_TURN = 3

STATE_COUNT = 54
MAX_STEPS = 3 * ROWS * COLS


def make_room():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def read_cell(room, row, col):
    """Read a cell; outside the room behaves like an obstacle."""
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return OBSTACLE

    return room[row][col]


def get_observation(room, row, col, direction):
    """Return [current, forward, left, right] for the robot."""
    current = read_cell(room, row, col)
    forward = direction
    left = (direction - 1) % 4
    right = (direction + 1) % 4

    forward_row = row + DIRECTIONS[forward][0]
    forward_col = col + DIRECTIONS[forward][1]
    left_row = row + DIRECTIONS[left][0]
    left_col = col + DIRECTIONS[left][1]
    right_row = row + DIRECTIONS[right][0]
    right_col = col + DIRECTIONS[right][1]

    return [
        current,
        read_cell(room, forward_row, forward_col),
        read_cell(room, left_row, left_col),
        read_cell(room, right_row, right_col),
    ]


def state_to_index(state):
    """Encode a sensor state into a chromosome index from 0 to 53."""
    current, forward, left, right = state
    current_code = 0 if current == EMPTY else 1

    index = current_code
    index = index * 3 + forward
    index = index * 3 + left
    index = index * 3 + right
    return index


def make_random_chromosome(seed=7):
    generator = random.Random(seed)
    return [generator.randrange(4) for _ in range(STATE_COUNT)]


def apply_action(direction, action, generator):
    if action == TURN_LEFT:
        return (direction - 1) % 4

    if action == TURN_RIGHT:
        return (direction + 1) % 4

    if action == RANDOM_TURN:
        turn = TURN_LEFT if generator.choice([True, False]) else TURN_RIGHT
        return apply_action(direction, turn, generator)

    return direction


def count_empty(room):
    return sum(cell == EMPTY for row in room for cell in row)


def simulate(
    chromosome,
    start_row,
    start_col,
    start_direction,
    seed=11,
    room_template=None,
):
    """Run one chromosome and return its coverage and trajectory."""
    if room_template is None:
        room = make_room()
    else:
        room = [row[:] for row in room_template]

    generator = random.Random(seed)
    paintable_cells = count_empty(room)
    remaining_cells = paintable_cells
    trajectory = []
    row = start_row
    col = start_col
    direction = start_direction

    if read_cell(room, row, col) != EMPTY:
        raise ValueError("The robot must start on an empty cell")

    for step in range(MAX_STEPS):
        trajectory.append((row, col))

        state = get_observation(room, row, col, direction)
        action = chromosome[state_to_index(state)]
        direction = apply_action(direction, action, generator)

        if room[row][col] == EMPTY:
            room[row][col] = PAINTED
            remaining_cells -= 1

        if remaining_cells == 0:
            break

        row_change, col_change = DIRECTIONS[direction]
        next_row = row + row_change
        next_col = col + col_change

        if read_cell(room, next_row, next_col) != OBSTACLE:
            row = next_row
            col = next_col

    painted_cells = paintable_cells - remaining_cells
    efficiency = painted_cells / paintable_cells

    return {
        "painted_cells": painted_cells,
        "paintable_cells": paintable_cells,
        "efficiency": efficiency,
        "steps": len(trajectory),
        "trajectory": trajectory,
        "final_position": (row, col),
    }


if __name__ == "__main__":
    chromosome = make_random_chromosome()
    result = simulate(chromosome, 10, 20, 1)

    print("Painted cells:", result["painted_cells"])
    print("Paintable cells:", result["paintable_cells"])
    print("Efficiency:", f'{result["efficiency"]:.2%}')
    print("Steps:", result["steps"])
    print("Final position:", result["final_position"])
