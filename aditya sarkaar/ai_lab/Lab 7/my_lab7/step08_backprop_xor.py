"""Step 8: train a 2-2-1 sigmoid MLP to learn XOR."""

import math
import random


X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
TARGETS = [0.0, 1.0, 1.0, 0.0]


def sigmoid(value):
    return 1.0 / (1.0 + math.exp(-value))


def train(alpha=0.5, seed=1, max_epochs=20000, tolerance=0.0001):
    rng = random.Random(seed)

    # V: input -> hidden weights; W: hidden -> output weights.
    V = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(2)]
    hidden_bias = [rng.uniform(-1, 1) for _ in range(2)]
    W = [rng.uniform(-1, 1) for _ in range(2)]
    output_bias = rng.uniform(-1, 1)

    def forward(x):
        hidden_input = [
            hidden_bias[j] + x[0] * V[0][j] + x[1] * V[1][j]
            for j in range(2)
        ]
        hidden_output = [sigmoid(value) for value in hidden_input]
        output_input = output_bias + sum(
            hidden_output[j] * W[j] for j in range(2)
        )
        output = sigmoid(output_input)
        return hidden_output, output

    for epoch in range(1, max_epochs + 1):
        squared_error = 0.0

        # Online backpropagation: update after every XOR pattern.
        for x, target in zip(X, TARGETS):
            hidden_output, output = forward(x)
            error = target - output
            squared_error += error * error

            # Output delta: error multiplied by sigmoid derivative.
            output_delta = error * output * (1.0 - output)

            # Hidden deltas use the output weights before they are changed.
            hidden_deltas = [
                output_delta * W[j] * hidden_output[j] * (1.0 - hidden_output[j])
                for j in range(2)
            ]

            # Output-layer updates.
            for j in range(2):
                W[j] += alpha * output_delta * hidden_output[j]
            output_bias += alpha * output_delta

            # Input-to-hidden updates.
            for i in range(2):
                for j in range(2):
                    V[i][j] += alpha * hidden_deltas[j] * x[i]
            for j in range(2):
                hidden_bias[j] += alpha * hidden_deltas[j]

        mse = squared_error / len(X)

        if epoch <= 5 or epoch % 1000 == 0:
            print(f"epoch={epoch:5d}  MSE={mse:.6f}")

        if mse < tolerance:
            break

    predictions = []
    raw_outputs = []
    for x in X:
        hidden_output, output = forward(x)
        raw_outputs.append(output)
        predictions.append(1 if output > 0.5 else 0)

    return epoch, mse, raw_outputs, predictions


if __name__ == "__main__":
    epochs, mse, raw_outputs, predictions = train()

    print("\nFinal result")
    print(f"epochs      = {epochs}")
    print(f"final MSE   = {mse:.6f}")
    for x, output, prediction, target in zip(X, raw_outputs, predictions, TARGETS):
        print(
            f"x={tuple(int(value) for value in x)}  "
            f"raw={output:.4f}  prediction={prediction}  target={int(target)}"
        )
