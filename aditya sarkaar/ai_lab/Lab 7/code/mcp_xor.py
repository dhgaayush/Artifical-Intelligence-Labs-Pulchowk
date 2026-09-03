# hand-designed McCulloch-Pitts net for XOR (assignment 4)
# single perceptron can't do XOR since it's not linearly separable, so we
# build it from two gates in a hidden layer: XOR = AND(OR(x1,x2), NAND(x1,x2))

import json
import os
import numpy as np

outdir = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(outdir, exist_ok=True)


def mp_unit(x, w, theta):
    y_in = float(np.dot(w, x))
    return (1 if y_in >= theta else 0), y_in


Z1_W, Z1_T = np.array([1, 1]), 1      # OR
Z2_W, Z2_T = np.array([-1, -1]), -1   # NAND
Y_W, Y_T = np.array([1, 1]), 2        # AND


def xor_mcp(x1, x2):
    x = np.array([x1, x2])
    z1, z1_in = mp_unit(x, Z1_W, Z1_T)
    z2, z2_in = mp_unit(x, Z2_W, Z2_T)
    y, y_in = mp_unit(np.array([z1, z2]), Y_W, Y_T)
    return {"x1": x1, "x2": x2, "z1_in": z1_in, "z1": z1,
            "z2_in": z2_in, "z2": z2, "y_in": y_in, "y": y}


if __name__ == "__main__":
    expected = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}
    rows = [xor_mcp(a, b) for a in (0, 1) for b in (0, 1)]

    all_correct = True
    for r in rows:
        exp = expected[(r["x1"], r["x2"])]
        ok = r["y"] == exp
        all_correct &= ok
        print(f"x1={r['x1']} x2={r['x2']} -> z1(OR)={r['z1']} z2(NAND)={r['z2']} "
              f"-> y={r['y']} expected={exp} {'ok' if ok else 'WRONG'}")

    print("all correct:", all_correct)

    with open(os.path.join(outdir, "mcp_xor_results.json"), "w") as f:
        json.dump({
            "weights": {
                "z1_OR": {"w": Z1_W.tolist(), "theta": Z1_T},
                "z2_NAND": {"w": Z2_W.tolist(), "theta": Z2_T},
                "y_AND": {"w": Y_W.tolist(), "theta": Y_T},
            },
            "truth_table": rows,
            "all_correct": bool(all_correct),
        }, f, indent=2)

    print("saved outputs/mcp_xor_results.json")
