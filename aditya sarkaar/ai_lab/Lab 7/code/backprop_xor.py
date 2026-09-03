# 2-2-1 MLP trained on XOR using backpropagation (assignment 5)
# sigmoid activation on hidden and output layer

import json
import os
import numpy as np

outdir = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(outdir, exist_ok=True)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
T = np.array([0, 1, 1, 0], dtype=float)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class MLP_XOR:
    def __init__(self, n_hidden=2, alpha=0.5, seed=0):
        rng = np.random.default_rng(seed)
        self.V = rng.uniform(-1, 1, size=(2, n_hidden))   # input -> hidden weights
        self.vb = rng.uniform(-1, 1, size=n_hidden)         # hidden bias
        self.W = rng.uniform(-1, 1, size=n_hidden)          # hidden -> output weights
        self.wb = float(rng.uniform(-1, 1))                 # output bias
        self.alpha = alpha

    def forward(self, x):
        z_in = self.vb + x @ self.V
        z = sigmoid(z_in)
        y_in = self.wb + z @ self.W
        y = sigmoid(y_in)
        return z_in, z, y_in, y

    def train(self, X, T, max_epochs=20000, tol=1e-4):
        history = {"epoch": [], "mse": []}
        for epoch in range(1, max_epochs + 1):
            mse = 0
            for x, t in zip(X, T):
                z_in, z, y_in, y = self.forward(x)
                mse += (t - y) ** 2

                # error term at output, then propagate back to hidden layer
                d_k = (t - y) * y * (1 - y)
                d_j = d_k * self.W * z * (1 - z)

                # weight updates
                self.W += self.alpha * d_k * z
                self.wb += self.alpha * d_k
                self.V += self.alpha * np.outer(x, d_j)
                self.vb += self.alpha * d_j

            mse /= len(X)
            history["epoch"].append(epoch)
            history["mse"].append(float(mse))
            if mse < tol:
                break
        return history

    def predict(self, X):
        outs = np.array([self.forward(x)[3] for x in X])
        return outs, (outs > 0.5).astype(int)


if __name__ == "__main__":
    best = None
    for seed in range(20):
        model = MLP_XOR(n_hidden=2, alpha=0.5, seed=seed)
        history = model.train(X, T)
        outs, preds = model.predict(X)
        converged = np.array_equal(preds, T.astype(int))
        if converged and (best is None or history["epoch"][-1] < best["history"]["epoch"][-1]):
            best = {"seed": seed, "model": model, "history": history, "outs": outs, "preds": preds}
        print(f"seed={seed}: epochs={history['epoch'][-1]}, mse={history['mse'][-1]:.6f}, "
              f"preds={preds.tolist()}, converged={converged}")

    model, history = best["model"], best["history"]
    outs, preds = best["outs"], best["preds"]
    print("\nbest run: seed =", best["seed"])
    for x, t, o, p in zip(X, T, outs, preds):
        print(f"x={x.tolist()} target={t} output={o:.4f} predicted={p}")

    result = {
        "seed": best["seed"],
        "alpha": model.alpha,
        "epochs_run": history["epoch"][-1],
        "final_mse": history["mse"][-1],
        "V_input_hidden": model.V.tolist(),
        "vb_hidden_bias": model.vb.tolist(),
        "W_hidden_output": model.W.tolist(),
        "wb_output_bias": model.wb,
        "truth_table": [
            {"x1": int(x[0]), "x2": int(x[1]), "target": int(t), "raw_output": float(o), "predicted": int(p)}
            for x, t, o, p in zip(X, T, outs, preds)
        ],
        "history": history,
    }
    with open(os.path.join(outdir, "backprop_xor_results.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("saved outputs/backprop_xor_results.json")
