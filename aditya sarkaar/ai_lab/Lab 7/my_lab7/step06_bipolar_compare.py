"""Step 6: compare unipolar and bipolar Adaline representations."""

import random


X_UNIPOLAR = [[0, 0], [0, 1], [1, 0], [1, 1]]
X_BIPOLAR = [[-1, -1], [-1, 1], [1, -1], [1, 1]]

GATES_UNIPOLAR = {
    "AND": [0, 0, 0, 1],
    "OR": [0, 1, 1, 1],
    "NAND": [1, 1, 1, 0],
    "NOR": [1, 0, 0, 0],
}


def to_bipolar(targets):
    return [-1 if target == 0 else 1 for target in targets]


def net_input(x, weights, bias):
    return bias + weights[0] * x[0] + weights[1] * x[1]


def train(X, targets, mode, alpha=0.1, seed=1, max_epochs=1000):
    rng = random.Random(seed)
    weights = [rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]
    bias = rng.uniform(-0.5, 0.5)

    for epoch in range(1, max_epochs + 1):
        for x, target in zip(X, targets):
            y_in = net_input(x, weights, bias)
            error = target - y_in
            weights[0] += alpha * error * x[0]
            weights[1] += alpha * error * x[1]
            bias += alpha * error

        if mode == "unipolar":
            predictions = [1 if net_input(x, weights, bias) > 0.5 else 0 for x in X]
        else:
            predictions = [1 if net_input(x, weights, bias) >= 0 else -1 for x in X]

        if predictions == targets:
            return epoch, weights, bias, predictions

    return max_epochs, weights, bias, predictions


if __name__ == "__main__":
    print("gate  unipolar epochs  bipolar epochs")
    print("----  ----------------  --------------")

    for gate_name, unipolar_targets in GATES_UNIPOLAR.items():
        bipolar_targets = to_bipolar(unipolar_targets)

        u_epochs, _, _, _ = train(
            X_UNIPOLAR, unipolar_targets, mode="unipolar"
        )
        b_epochs, _, _, _ = train(
            X_BIPOLAR, bipolar_targets, mode="bipolar"
        )

        print(f"{gate_name:4s}  {u_epochs:16d}  {b_epochs:14d}")

    print("\nUnipolar zero = inactive input; bipolar -1 = active negative contribution.")
