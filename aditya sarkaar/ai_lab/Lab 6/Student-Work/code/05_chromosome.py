import random


EMPTY = 0
OBSTACLE = 1
PAINTED = 2

# Direction numbers:
# 0 = north, 1 = east, 2 = south, 3 = west
DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

# Actions stored in a chromosome gene:
# 0 = do not turn, 1 = turn left, 2 = turn right,
# 3 = randomly turn left or right.
NO_TURN = 0
TURN_LEFT = 1
TURN_RIGHT = 2
RANDOM_TURN = 3

STATE_COUNT = 54


def current_to_code(current):
    # The robot can only stand on an empty or painted square.
    if current == EMPTY:
        return 0

    return 1


def state_to_index(current, forward, left, right):
    """Convert [current, forward, left, right] into a gene index."""
    index = current_to_code(current)
    index = index * 3 + forward
    index = index * 3 + left
    index = index * 3 + right
    return index


def make_random_chromosome(seed=7):
    """Create 54 random actions, one for every possible sensor state."""
    generator = random.Random(seed)
    return [generator.randrange(4) for _ in range(STATE_COUNT)]


def apply_action(direction, action, generator):
    """Return the new direction after applying one chromosome action."""
    if action == NO_TURN:
        return direction

    if action == TURN_LEFT:
        return (direction - 1) % 4

    if action == TURN_RIGHT:
        return (direction + 1) % 4

    if action == RANDOM_TURN:
        if generator.choice([True, False]):
            return (direction - 1) % 4

        return (direction + 1) % 4

    raise ValueError("Action must be an integer from 0 to 3")


chromosome = make_random_chromosome()

# Example: look up the action for an empty current square with an obstacle ahead.
state_index = state_to_index(EMPTY, OBSTACLE, EMPTY, EMPTY)
action = chromosome[state_index]

direction = 1  # east
new_direction = apply_action(direction, action, random.Random(10))

print("Chromosome length:", len(chromosome))
print("State index:", state_index)
print("Action at that state:", action)
print("Direction before action:", direction)
print("Direction after action:", new_direction)
