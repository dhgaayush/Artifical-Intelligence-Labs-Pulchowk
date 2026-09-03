"""Step 7: build XOR from fixed McCulloch-Pitts threshold units."""


X = [[0, 0], [0, 1], [1, 0], [1, 1]]
XOR_TARGETS = [0, 1, 1, 0]


def threshold_unit(inputs, weights, threshold):
    weighted_sum = sum(value * weight for value, weight in zip(inputs, weights))
    output = 1 if weighted_sum >= threshold else 0
    return weighted_sum, output


def xor_network(x1, x2):
    # Hidden unit 1: OR(x1, x2)
    z1_sum, z1 = threshold_unit([x1, x2], [1, 1], threshold=1)

    # Hidden unit 2: NAND(x1, x2)
    z2_sum, z2 = threshold_unit([x1, x2], [-1, -1], threshold=-1)

    # Output unit: AND(z1, z2)
    y_sum, y = threshold_unit([z1, z2], [1, 1], threshold=2)

    return z1_sum, z1, z2_sum, z2, y_sum, y


if __name__ == "__main__":
    all_correct = True

    for x, target in zip(X, XOR_TARGETS):
        z1_sum, z1, z2_sum, z2, y_sum, prediction = xor_network(x[0], x[1])
        correct = prediction == target
        all_correct = all_correct and correct

        print(
            f"x={tuple(x)}  "
            f"OR: sum={z1_sum: .1f}->z1={z1}  "
            f"NAND: sum={z2_sum: .1f}->z2={z2}  "
            f"AND: sum={y_sum: .1f}->y={prediction}  "
            f"target={target}  {'OK' if correct else 'WRONG'}"
        )

    print(f"\nAll XOR rows correct: {all_correct}")
