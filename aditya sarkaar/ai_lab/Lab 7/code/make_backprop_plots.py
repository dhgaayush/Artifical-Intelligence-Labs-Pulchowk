# loss curve + decision boundary plot for the backprop XOR run (assignment 5)

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from backprop_xor import MLP_XOR, X, T, sigmoid

here = os.path.dirname(__file__)
outdir = os.path.join(here, "..", "outputs")

with open(os.path.join(outdir, "backprop_xor_results.json")) as f:
    res = json.load(f)

# Loss curve
fig, ax = plt.subplots(figsize=(6, 4))
h = res["history"]
ax.plot(h["epoch"], h["mse"])
ax.set_xlabel("Epoch")
ax.set_ylabel("Mean squared error")
ax.set_title(f"Backpropagation MLP training loss (XOR), seed={res['seed']}")
ax.set_yscale("log")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(outdir, "xor_backprop_loss.png"), dpi=150)
plt.close(fig)

# Rebuild the best model to plot its decision boundary
model = MLP_XOR(n_hidden=2, alpha=res["alpha"], seed=res["seed"])
model.V = np.array(res["V_input_hidden"])
model.vb = np.array(res["vb_hidden_bias"])
model.W = np.array(res["W_hidden_output"])
model.wb = res["wb_output_bias"]

xx, yy = np.meshgrid(np.linspace(-0.5, 1.5, 200), np.linspace(-0.5, 1.5, 200))
grid = np.c_[xx.ravel(), yy.ravel()]
zz = np.array([model.forward(g)[3] for g in grid]).reshape(xx.shape)

fig, ax = plt.subplots(figsize=(5.5, 5))
cs = ax.contourf(xx, yy, zz, levels=20, cmap="RdBu_r", vmin=0, vmax=1, alpha=0.85)
ax.contour(xx, yy, zz, levels=[0.5], colors="k", linewidths=2)
for x, t in zip(X, T):
    ax.scatter(*x, c="black" if t == 0 else "white", edgecolors="black", s=140, zorder=5,
               marker="o" if t == 0 else "s")
    ax.annotate(f"({int(x[0])},{int(x[1])})->{int(t)}", (x[0], x[1]), textcoords="offset points",
                xytext=(10, 8), fontsize=9)
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_title("XOR decision boundary learned by backpropagation")
fig.colorbar(cs, ax=ax, label="network output")
fig.tight_layout()
fig.savefig(os.path.join(outdir, "xor_backprop_boundary.png"), dpi=150)
plt.close(fig)

print("Saved outputs/xor_backprop_loss.png and outputs/xor_backprop_boundary.png")
