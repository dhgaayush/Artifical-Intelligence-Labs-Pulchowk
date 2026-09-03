"""Step 1: inspect the logic-gate datasets used by the neural-network lab."""


UNIPOLAR_X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
]

GATES = {
    "AND":  [0, 0, 0, 1],
    "OR":   [0, 1, 1, 1],
    "NAND": [1, 1, 1, 0],
    "NOR":  [1, 0, 0, 0],
    "XOR":  [0, 1, 1, 0],
}


def to_bipolar(values):
    """Convert unipolar values: 0 -> -1 and 1 -> 1."""
    return [-1 if value == 0 else 1 for value in values]


def print_gate(name, targets):
    print(f"\n{name}")
    print("x1  x2  target")
    print("--  --  ------")
    for x, target in zip(UNIPOLAR_X, targets):
        print(f"{x[0]}   {x[1]}   {target}")


if __name__ == "__main__":
    print("UNIPOLAR INPUTS")
    print(UNIPOLAR_X)

    print("\nBIPOLAR INPUTS")
    print([to_bipolar(x) for x in UNIPOLAR_X])

    for gate_name, targets in GATES.items():
        print_gate(gate_name, targets)

    print("\nYour checkpoint:")
    print("1. Identify the two rows where XOR outputs 1.")
    print("2. Explain why one straight line cannot separate those rows from the other two.")
    print("3. Write the formula y_in = b + w1*x1 + w2*x2 in your own notes.")
