"""Step 2: follow two Adaline updates numerically.

We use simple fixed values so the arithmetic can be checked by hand.
This is intentionally not the complete trainer yet.
"""


def adaline_update(x1, x2, target, w1, w2, bias, alpha):
    """Perform one online Adaline update and return all intermediate values."""
    y_in = bias + w1 * x1 + w2 * x2
    error = target - y_in

    delta_w1 = alpha * error * x1
    delta_w2 = alpha * error * x2
    delta_bias = alpha * error

    new_w1 = w1 + delta_w1
    new_w2 = w2 + delta_w2
    new_bias = bias + delta_bias

    return {
        "y_in": y_in,
        "error": error,
        "delta_w1": delta_w1,
        "delta_w2": delta_w2,
        "delta_bias": delta_bias,
        "w1": new_w1,
        "w2": new_w2,
        "bias": new_bias,
    }


if __name__ == "__main__":
    alpha = 0.1
    w1, w2, bias = 0.2, -0.1, 0.3

    # First two rows of the unipolar AND truth table.
    examples = [
        ((0, 0), 0),
        ((0, 1), 0),
    ]

    print(f"Initial: w1={w1:.3f}, w2={w2:.3f}, bias={bias:.3f}, alpha={alpha:.3f}")

    for number, (inputs, target) in enumerate(examples, start=1):
        result = adaline_update(
            inputs[0], inputs[1], target, w1, w2, bias, alpha
        )

        print(f"\nPattern {number}: x={inputs}, target={target}")
        print(f"y_in       = {result['y_in']:.3f}")
        print(f"error      = {result['error']:.3f}")
        print(
            "changes    = "
            f"dw1={result['delta_w1']:.3f}, "
            f"dw2={result['delta_w2']:.3f}, "
            f"db={result['delta_bias']:.3f}"
        )
        print(
            "new values = "
            f"w1={result['w1']:.3f}, "
            f"w2={result['w2']:.3f}, "
            f"bias={result['bias']:.3f}"
        )

        # Online learning: use this pattern's new values for the next pattern.
        w1, w2, bias = result["w1"], result["w2"], result["bias"]

    print("\nCheckpoint: explain why dw1 and dw2 are both zero for pattern 1.")
