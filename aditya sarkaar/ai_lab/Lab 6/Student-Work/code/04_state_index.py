EMPTY = 0
OBSTACLE = 1
PAINTED = 2


def current_to_code(current):
    # The current square has only two possible states:
    # empty = 0, painted = 1
    if current == EMPTY:
        return 0

    return 1


def state_to_index(current, forward, left, right):
    current_code = current_to_code(current)

    index = current_code
    index = index * 3 + forward
    index = index * 3 + left
    index = index * 3 + right

    return index


state_one = state_to_index(EMPTY, EMPTY, EMPTY, EMPTY)
state_two = state_to_index(EMPTY, OBSTACLE, EMPTY, EMPTY)
state_three = state_to_index(PAINTED, PAINTED, PAINTED, PAINTED)

print("State [0, 0, 0, 0] has index:", state_one)
print("State [0, 1, 0, 0] has index:", state_two)
print("State [2, 2, 2, 2] has index:", state_three)


# Check that all possible states produce unique indexes.
all_indexes = []

for current in [EMPTY, PAINTED]:
    for forward in range(3):
        for left in range(3):
            for right in range(3):
                index = state_to_index(current, forward, left, right)

                if index not in all_indexes:
                    all_indexes.append(index)

print("Number of unique states:", len(all_indexes))
print("Smallest index:", min(all_indexes))
print("Largest index:", max(all_indexes))