"""Step 5: study how the Adaline learning rate affects AND training."""

import random


X = [[0, 0], [0, 1], [1, 0], [1, 1]]
TARGETS = [0, 0, 0, 1]
ALPHAS = [0.01, 0.05, 0.1, 0.3, 0.5, 0.9]
SEEDS = [1, 2, 3, 4, 5]
MAX_EPOCHS = 1000


def net_input(x, weights, bias):
    return bias + weights[0] * x[0] + weights[1] * x[1]


def predict_all(weights, bias):
    return [1 if net_input(x, weights, bias) > 0.5 else 0 for x in X]


def epochs_to_correct(alpha, seed):
    rng = random.Random(seed)
    weights = [rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]
    bias = rng.uniform(-0.5, 0.5)

    for epoch in range(1, MAX_EPOCHS + 1):
        for x, target in zip(X, TARGETS):
            y_in = net_input(x, weights, bias)
            error = target - y_in
            weights[0] += alpha * error * x[0]
            weights[1] += alpha * error * x[1]
            bias += alpha * error

        if predict_all(weights, bias) == TARGETS:
            return epoch

    return MAX_EPOCHS


if __name__ == "__main__":
    print("alpha   epochs for seeds 1..5        mean")
    print("-----   --------------------        ----")

    for alpha in ALPHAS:
        results = [epochs_to_correct(alpha, seed) for seed in SEEDS]
        mean = sum(results) / len(results)
        print(f"{alpha:0.2f}    {results!s:24s}  {mean:0.2f}")

    print("\nInterpretation: a result of 1000 means 'not correct within the limit'.")
