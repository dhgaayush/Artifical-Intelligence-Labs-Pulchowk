"""
painter.py

Simulation engine for the Genetic Algorithm Painter Robot.

This module is responsible for:
    • Robot initialization
    • Robot movement
    • Direction handling
    • State sensing
    • Simulation

This is Part 1:
    - Constants
    - Direction utilities
    - Robot initialization
"""

import random
import numpy as np

from environment import copy_room


# ==========================================================
# CONSTANTS
# ==========================================================

# Cell values
EMPTY = 0
OBSTACLE = 1
PAINTED = 2

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

# Movement vectors
MOVE_VECTOR = {
    UP: (-1, 0),
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1)
}


# ==========================================================
# ROOM PREPARATION
# ==========================================================

def add_boundary_walls(room):
    """
    Surround the room with a one-cell thick wall.

    Original room:
        0 0 0
        0 0 0

    becomes

        1 1 1 1 1
        1 0 0 0 1
        1 0 0 0 1
        1 1 1 1 1
    """

    rows, cols = room.shape

    padded = np.ones((rows + 2, cols + 2), dtype=int)

    padded[1:rows + 1, 1:cols + 1] = room

    return padded


# ==========================================================
# ROBOT INITIALIZATION
# ==========================================================

def initialize_robot(room):
    """
    Spawn robot at a random empty square.

    Returns
    -------
    robot : dict
    """

    rows, cols = room.shape

    while True:

        row = random.randint(1, rows - 2)
        col = random.randint(1, cols - 2)

        if room[row, col] == EMPTY:
            break

    robot = {
        "row": row,
        "col": col,
        "direction": random.choice(DIRECTIONS)
    }

    return robot


# ==========================================================
# DIRECTION UTILITIES
# ==========================================================

def turn_left(direction):
    """
    Rotate robot 90° left.
    """

    return (direction - 1) % 4


def turn_right(direction):
    """
    Rotate robot 90° right.
    """

    return (direction + 1) % 4


def forward_position(robot):
    """
    Position directly in front of robot.
    """

    dr, dc = MOVE_VECTOR[robot["direction"]]

    return (
        robot["row"] + dr,
        robot["col"] + dc
    )


def left_position(robot):
    """
    Position directly left of robot.
    """

    direction = turn_left(robot["direction"])

    dr, dc = MOVE_VECTOR[direction]

    return (
        robot["row"] + dr,
        robot["col"] + dc
    )


def right_position(robot):
    """
    Position directly right of robot.
    """

    direction = turn_right(robot["direction"])

    dr, dc = MOVE_VECTOR[direction]

    return (
        robot["row"] + dr,
        robot["col"] + dc
    )


# ==========================================================
# MOVEMENT
# ==========================================================

def move_forward(robot, room):
    """
    Move one square forward.

    The robot remains in place if the square ahead
    is an obstacle.
    """

    new_row, new_col = forward_position(robot)

    if room[new_row, new_col] != OBSTACLE:

        robot["row"] = new_row
        robot["col"] = new_col

    return robot


# ==========================================================
# ROOM COPYING
# ==========================================================

def prepare_environment(room):
    """
    Create a fresh simulation environment.

    The original room is never modified.
    """

    room = copy_room(room)

    room = add_boundary_walls(room)

    return room

# ==========================================================
# STATE DETECTION
# ==========================================================

def get_cell_state(room, row, col):
    """
    Returns the state of a cell.

    Returns
    -------
    0 : Empty
    1 : Obstacle
    2 : Painted
    """

    return int(room[row, col])


def get_robot_state(robot, room):
    """
    Read the four values required by the chromosome.

    Returns
    -------
    tuple

    (current, forward, left, right)

    current ∈ {0,2}
    forward,left,right ∈ {0,1,2}
    """

    row = robot["row"]
    col = robot["col"]

    current = get_cell_state(room, row, col)

    forward_row, forward_col = forward_position(robot)
    left_row, left_col = left_position(robot)
    right_row, right_col = right_position(robot)

    forward = get_cell_state(room, forward_row, forward_col)
    left = get_cell_state(room, left_row, left_col)
    right = get_cell_state(room, right_row, right_col)

    return (
        current,
        forward,
        left,
        right
    )


# ==========================================================
# CHROMOSOME ENCODING
# ==========================================================

def encode_state_to_index(state):
    """
    Convert

        (current, forward, left, right)

    into chromosome index (0–53).

    Uses the exact encoding from the original lab code.

    Formula

        index = 2*(9*forward + 3*left + right)

        if current == PAINTED:
            index += 1
    """

    current, forward, left, right = state

    index = 2 * (
        9 * forward +
        3 * left +
        right
    )

    if current == PAINTED:
        index += 1

    return index


# ==========================================================
# ACTION SELECTION
# ==========================================================

def choose_action(chromosome, state):
    """
    Select action from chromosome.

    Returns

    0 -> Go Straight
    1 -> Turn Left
    2 -> Turn Right
    3 -> Random Left / Right
    """

    index = encode_state_to_index(state)

    action = chromosome[index]

    return int(action)


def apply_action(robot, action):
    """
    Apply turning action.

    Forward movement is NOT performed here.
    Only orientation changes.

    Returns
    -------
    robot
    """

    if action == 1:

        robot["direction"] = turn_left(
            robot["direction"]
        )

    elif action == 2:

        robot["direction"] = turn_right(
            robot["direction"]
        )

    elif action == 3:

        if random.random() < 0.5:
            robot["direction"] = turn_left(
                robot["direction"]
            )
        else:
            robot["direction"] = turn_right(
                robot["direction"]
            )

    return robot


# ==========================================================
# PAINTING
# ==========================================================

def paint_current_cell(robot, room):
    """
    Paint current location if it has not already
    been painted.

    Returns
    -------
    bool

    True  -> newly painted

    False -> already painted / obstacle
    """

    row = robot["row"]
    col = robot["col"]

    if room[row, col] == EMPTY:

        room[row, col] = PAINTED

        return True

    return False

# ==========================================================
# SIMULATION
# ==========================================================

def simulate_step(robot, room, chromosome):
    """
    Execute one complete simulation step.

    Order of operations (matches original implementation):

        1. Sense environment
        2. Choose action
        3. Turn
        4. Paint current square
        5. Move forward

    Returns
    -------
    painted : bool
        True if a new square was painted.
    """

    # Sense surroundings
    state = get_robot_state(robot, room)

    # Decide action
    action = choose_action(chromosome, state)

    # Turn
    apply_action(robot, action)

    # Paint current location
    painted = paint_current_cell(robot, room)

    # Move forward
    move_forward(robot, room)

    return painted


# ==========================================================
# EFFICIENCY
# ==========================================================

def calculate_efficiency(room):
    """
    Calculate painting efficiency.

    Efficiency =
        Painted Cells / Paintable Cells

    Boundary walls are ignored.
    """

    # Remove artificial boundary walls
    inner_room = room[1:-1, 1:-1]

    painted = np.sum(inner_room == PAINTED)

    total = painted + np.sum(inner_room == EMPTY)

    if total == 0:
        return 0.0

    return painted / total


# ==========================================================
# MAIN SIMULATION
# ==========================================================

def simulate_painter(chromosome, room):
    """
    Simulate the painter robot.

    Parameters
    ----------
    chromosome : ndarray (54,)
    room : ndarray

    Returns
    -------
    dict

        {
            "efficiency": float,
            "trajectory": [(r,c), ...],
            "painted_room": ndarray,
            "robot": dict
        }
    """

    # Create independent simulation environment
    room = prepare_environment(room)

    # Random initial position
    robot = initialize_robot(room)

    # Number of time steps
    # (same as original implementation)

    steps = np.sum(room == EMPTY)

    trajectory = []

    for _ in range(steps):

        trajectory.append(
            (robot["row"] - 1,
             robot["col"] - 1)
        )

        simulate_step(
            robot,
            room,
            chromosome
        )

    efficiency = calculate_efficiency(room)

    return {

        "efficiency": efficiency,

        "trajectory": trajectory,

        "painted_room": room[1:-1, 1:-1].copy(),

        "robot": robot.copy()

    }


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    from environment import create_empty_room

    room = create_empty_room()

    chromosome = np.random.randint(
        0,
        4,
        size=54
    )

    result = simulate_painter(
        chromosome,
        room
    )

    print("=" * 40)
    print("Simulation Complete")
    print("=" * 40)

    print("Efficiency :",
          round(result["efficiency"], 3))

    print("Trajectory Length :",
          len(result["trajectory"]))

    print("Final Robot State :")
    print(result["robot"])


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def generate_random_chromosome():
    """
    Generate a random chromosome.

    Returns
    -------
    ndarray (54,)
    """

    return np.random.randint(0, 4, size=54)


def simulate_multiple_runs(chromosome, room, runs=5):
    """
    Run the same chromosome multiple times.

    Since the robot starts at a random location and
    orientation, averaging several runs gives a much
    more reliable estimate of its performance.

    Returns
    -------
    dict

        {
            "average_efficiency": float,
            "best_efficiency": float,
            "worst_efficiency": float,
            "results": [...]
        }
    """

    results = []

    efficiencies = []

    for _ in range(runs):

        result = simulate_painter(chromosome, room)

        results.append(result)

        efficiencies.append(result["efficiency"])

    return {

        "average_efficiency": float(np.mean(efficiencies)),

        "best_efficiency": float(np.max(efficiencies)),

        "worst_efficiency": float(np.min(efficiencies)),

        "results": results

    }


# ==========================================================
# DEBUGGING HELPERS
# ==========================================================

def print_simulation_summary(result):
    """
    Print a nicely formatted simulation summary.
    """

    print("=" * 45)
    print("Painter Simulation Summary")
    print("=" * 45)

    print(f"Efficiency        : {result['efficiency']:.3f}")

    print(f"Trajectory Length : {len(result['trajectory'])}")

    print(f"Final Position    : "
          f"({result['robot']['row']-1}, "
          f"{result['robot']['col']-1})")

    direction_names = {
        UP: "UP",
        RIGHT: "RIGHT",
        DOWN: "DOWN",
        LEFT: "LEFT"
    }

    print(f"Final Direction   : "
          f"{direction_names[result['robot']['direction']]}")

    print("=" * 45)


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    from environment import create_empty_room

    room = create_empty_room()

    chromosome = generate_random_chromosome()

    result = simulate_painter(chromosome, room)

    print_simulation_summary(result)

    multi = simulate_multiple_runs(
        chromosome,
        room,
        runs=5
    )

    print("\nAverage over 5 runs")
    print("-------------------")
    print(f"Average : {multi['average_efficiency']:.3f}")
    print(f"Best    : {multi['best_efficiency']:.3f}")
    print(f"Worst   : {multi['worst_efficiency']:.3f}")