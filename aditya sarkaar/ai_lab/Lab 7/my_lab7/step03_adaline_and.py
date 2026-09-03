"""Step 3: train one Adaline neuron to implement unipolar AND.

This version uses ordinary Python lists instead of NumPy so that the learning
algorithm remains visible.
"""


X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
]
TARGETS = [0, 0, 0, 1]


def net_input(x, weights, bias):
    """Calculate b + w1*x1 + w2*x2."""
    return bias + weights[0] * x[0] + weights[1] * x[1]


def classify(y_in):
    """Unipolar decision rule used by this lab."""
    return 1 if y_in > 0.5 else 0


def predict_all(weights, bias):
    return [classify(net_input(x, weights, bias)) for x in X]


def sum_squared_error(weights, bias):
    total = 0.0
    for x, target in zip(X, TARGETS):
        error = target - net_input(x, weights, bias)
        total += error * error
    return total


def train(alpha=0.1, max_epochs=100):
    # Fixed starting values make your result reproducible.
    weights = [0.2, -0.1]
    bias = 0.3

    for epoch in range(1, max_epochs + 1):
        largest_change = 0.0

        # Online learning: update immediately after every training pattern.
        for x, target in zip(X, TARGETS):
            y_in = net_input(x, weights, bias)
            error = target - y_in

            delta_w1 = alpha * error * x[0]
            delta_w2 = alpha * error * x[1]
            delta_bias = alpha * error

            weights[0] += delta_w1
            weights[1] += delta_w2
            bias += delta_bias

            largest_change = max(
                largest_change,
                abs(delta_w1),
                abs(delta_w2),
                abs(delta_bias),
            )

        predictions = predict_all(weights, bias)
        sse = sum_squared_error(weights, bias)

        print(
            f"epoch={epoch:2d}  "
            f"w1={weights[0]: .4f}  w2={weights[1]: .4f}  "
            f"bias={bias: .4f}  SSE={sse:.4f}  "
            f"max_change={largest_change:.4f}  predictions={predictions}"
        )

        if predictions == TARGETS:
            return weights, bias, epoch

    return weights, bias, max_epochs


if __name__ == "__main__":
    final_weights, final_bias, epochs = train(alpha=0.1)

    print("\nFinal result")
    print(f"weights = {final_weights}")
    print(f"bias    = {final_bias:.6f}")
    print(f"epochs  = {epochs}")
    print(f"outputs = {predict_all(final_weights, final_bias)}")
