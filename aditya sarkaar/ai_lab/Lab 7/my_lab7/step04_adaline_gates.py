"""Step 4: reuse one Adaline trainer for four logic gates."""


X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
]

GATES = {
    "AND": [0, 0, 0, 1],
    "OR": [0, 1, 1, 1],
    "NAND": [1, 1, 1, 0],
    "NOR": [1, 0, 0, 0],
    "XOR": [0, 1, 1, 0]

}


def net_input(x, weights, bias):
    return bias + weights[0] * x[0] + weights[1] * x[1]


def classify(y_in):
    return 1 if y_in > 0.5 else 0


def predict_all(weights, bias):
    return [classify(net_input(x, weights, bias)) for x in X]


def train_gate(targets, alpha=0.1, max_epochs=100):
    weights = [0.2, -0.1]
    bias = 0.3

    for epoch in range(1, max_epochs + 1):
        for x, target in zip(X, targets):
            y_in = net_input(x, weights, bias)
            error = target - y_in

            weights[0] += alpha * error * x[0]
            weights[1] += alpha * error * x[1]
            bias += alpha * error

        predictions = predict_all(weights, bias)
        if predictions == targets:
            return weights, bias, epoch, predictions

    return weights, bias, max_epochs, predict_all(weights, bias)


if __name__ == "__main__":
    for gate_name, targets in GATES.items():
        weights, bias, epochs, predictions = train_gate(targets)
        print(
            f"{gate_name:4s}  "
            f"w1={weights[0]: .4f}  w2={weights[1]: .4f}  "
            f"bias={bias: .4f}  epochs={epochs:2d}  "
            f"predictions={predictions}  targets={targets}"
        )
