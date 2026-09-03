# makes the convergence and parameter-study plots for assignments 1-3

import json
import os
import matplotlib.pyplot as plt

here = os.path.dirname(__file__)
outdir = os.path.join(here, "..", "outputs")

with open(os.path.join(outdir, "adaline_results.json")) as f:
    results = json.load(f)

with open(os.path.join(outdir, "param_study.json")) as f:
    pstudy = json.load(f)

GATES = ["AND", "OR", "NAND", "NOR"]


def plot_mode_convergence(mode, filename):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for gate in GATES:
        h = results[mode][gate]["history"]
        axes[0].plot(h["epoch"], h["sse"], label=gate)
        axes[1].plot(h["epoch"], h["max_dw"], label=gate)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Sum-squared error")
    axes[0].set_title(f"SSE convergence ({mode})")
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Max weight/bias change")
    axes[1].set_title(f"Weight-change convergence ({mode})")
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    axes[1].set_yscale("log")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, filename), dpi=150)
    plt.close(fig)


plot_mode_convergence("unipolar", "unipolar_convergence.png")
plot_mode_convergence("bipolar", "bipolar_convergence.png")


# Unipolar vs bipolar SSE comparison for AND specifically (Assignment 3 discussion)
fig, ax = plt.subplots(figsize=(6, 4))
for mode, style in [("unipolar", "-"), ("bipolar", "--")]:
    h = results[mode]["AND"]["history"]
    ax.plot(h["epoch"], h["sse"], style, label=f"AND ({mode})")
ax.set_xlabel("Epoch")
ax.set_ylabel("Sum-squared error")
ax.set_title("Unipolar vs bipolar Adaline convergence (AND)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(outdir, "unipolar_vs_bipolar_and.png"), dpi=150)
plt.close(fig)


# Parameter study: alpha vs epochs to first correct classification
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
alphas = [r["alpha"] for r in pstudy["alpha_study"]]
means = [r["mean_epochs_to_correct"] for r in pstudy["alpha_study"]]
stds = [r["std_epochs_to_correct"] for r in pstudy["alpha_study"]]
axes[0].errorbar(alphas, means, yerr=stds, marker="o", capsize=4)
axes[0].set_xlabel("Learning rate (alpha)")
axes[0].set_ylabel("Epochs to first correct classification")
axes[0].set_title("Effect of learning rate (AND, unipolar)")
axes[0].grid(alpha=0.3)

wscales = [r["w_init_scale"] for r in pstudy["w_scale_study"]]
wmeans = [r["mean_epochs_to_correct"] for r in pstudy["w_scale_study"]]
wstds = [r["std_epochs_to_correct"] for r in pstudy["w_scale_study"]]
axes[1].errorbar(wscales, wmeans, yerr=wstds, marker="s", color="tab:orange", capsize=4)
axes[1].set_xlabel("Initial weight scale")
axes[1].set_ylabel("Epochs to first correct classification")
axes[1].set_title("Effect of initial weight scale (AND, unipolar)")
axes[1].grid(alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(outdir, "param_study.png"), dpi=150)
plt.close(fig)

print("Saved plots to", outdir)
