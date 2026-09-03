# Adaline (delta rule) for AND/OR/NAND/NOR gates
# works for both unipolar (0/1) and bipolar (-1/1) encoding

import json
import os
import numpy as np

GATES_UNIPOLAR = {
    "AND":  {"X": np.array([[0,0],[0,1],[1,0],[1,1]]), "t": np.array([0,0,0,1])},
    "OR":   {"X": np.array([[0,0],[0,1],[1,0],[1,1]]), "t": np.array([0,1,1,1])},
    "NAND": {"X": np.array([[0,0],[0,1],[1,0],[1,1]]), "t": np.array([1,1,1,0])},
    "NOR":  {"X": np.array([[0,0],[0,1],[1,0],[1,1]]), "t": np.array([1,0,0,0])},
}

GATES_BIPOLAR = {
    "AND":  {"X": np.array([[-1,-1],[-1,1],[1,-1],[1,1]]), "t": np.array([-1,-1,-1,1])},
    "OR":   {"X": np.array([[-1,-1],[-1,1],[1,-1],[1,1]]), "t": np.array([-1,1,1,1])},
    "NAND": {"X": np.array([[-1,-1],[-1,1],[1,-1],[1,1]]), "t": np.array([1,1,1,-1])},
    "NOR":  {"X": np.array([[-1,-1],[-1,1],[1,-1],[1,1]]), "t": np.array([1,-1,-1,-1])},
}


class Adaline:
    def __init__(self, n_inputs, alpha=0.1, mode="unipolar", seed=0, w_init_scale=0.5):
        rng = np.random.default_rng(seed)
        self.w = rng.uniform(-w_init_scale, w_init_scale, size=n_inputs)
        self.b = rng.uniform(-w_init_scale, w_init_scale)
        self.alpha = alpha
        self.mode = mode

    def net_input(self, x):
        return self.b + np.dot(self.w, x)

    def activate(self, y_in):
        if self.mode == "unipolar":
            return 1 if y_in > 0.5 else 0
        else:
            return 1 if y_in >= 0 else -1

    def train(self, X, t, tol=1e-3, max_epochs=500):
        history = {"epoch": [], "sse": [], "max_dw": [], "weights": [], "bias": []}
        first_correct_epoch = None

        for epoch in range(1, max_epochs + 1):
            max_dw = 0
            sse = 0
            for xi, ti in zip(X, t):
                y_in = self.net_input(xi)
                error = ti - y_in
                sse += error ** 2

                # delta rule (Widrow-Hoff) update
                dw = self.alpha * error * xi
                db = self.alpha * error
                self.w += dw
                self.b += db

                max_dw = max(max_dw, np.max(np.abs(dw)), abs(db))

            history["epoch"].append(epoch)
            history["sse"].append(float(sse))
            history["max_dw"].append(float(max_dw))
            history["weights"].append(self.w.tolist())
            history["bias"].append(float(self.b))

            if first_correct_epoch is None and np.array_equal(self.predict(X), t):
                first_correct_epoch = epoch

            if max_dw < tol:
                break

        history["first_correct_epoch"] = first_correct_epoch
        return history

    def predict(self, X):
        return np.array([self.activate(self.net_input(xi)) for xi in X])


def run_gate(gate_name, mode, alpha=0.1, seed=0, tol=1e-3, max_epochs=500, w_init_scale=0.5):
    table = GATES_UNIPOLAR if mode == "unipolar" else GATES_BIPOLAR
    X, t = table[gate_name]["X"], table[gate_name]["t"]

    model = Adaline(2, alpha=alpha, mode=mode, seed=seed, w_init_scale=w_init_scale)
    history = model.train(X, t, tol=tol, max_epochs=max_epochs)
    preds = model.predict(X)

    return {
        "gate": gate_name,
        "mode": mode,
        "alpha": alpha,
        "seed": seed,
        "tol": tol,
        "epochs_run": history["epoch"][-1],
        "final_weights": model.w.tolist(),
        "final_bias": model.b,
        "predictions": preds.tolist(),
        "targets": t.tolist(),
        "converged_to_target": bool(np.array_equal(preds, t)),
        "first_correct_epoch": history["first_correct_epoch"],
        "history": history,
    }


if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(outdir, exist_ok=True)

    all_results = {"unipolar": {}, "bipolar": {}}

    for gate in ["AND", "OR", "NAND", "NOR"]:
        res = run_gate(gate, "unipolar", alpha=0.1, seed=1)
        all_results["unipolar"][gate] = res
        print(f"[unipolar] {gate}: epochs={res['epochs_run']}, w={np.round(res['final_weights'],4)}, "
              f"b={round(res['final_bias'],4)}, preds={res['predictions']}, converged={res['converged_to_target']}")

    for gate in ["AND", "OR", "NAND", "NOR"]:
        res = run_gate(gate, "bipolar", alpha=0.1, seed=1)
        all_results["bipolar"][gate] = res
        print(f"[bipolar] {gate}: epochs={res['epochs_run']}, w={np.round(res['final_weights'],4)}, "
              f"b={round(res['final_bias'],4)}, preds={res['predictions']}, converged={res['converged_to_target']}")

    with open(os.path.join(outdir, "adaline_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)

    print("saved outputs/adaline_results.json")
