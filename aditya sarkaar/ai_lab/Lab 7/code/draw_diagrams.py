# draws the neuron diagrams for the gates and the MLP diagram for XOR
# just plain matplotlib shapes, nothing fancy

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

here = os.path.dirname(__file__)
outdir = os.path.join(here, "..", "outputs")


def draw_single_neuron(gate, w, b, mode, filename):
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    x1_pos = (1, 6)
    x2_pos = (1, 2)
    bias_pos = (5, 7.3)
    neuron_pos = (5.5, 4)

    for pos, label in [(x1_pos, "x1"), (x2_pos, "x2")]:
        ax.add_patch(Circle(pos, 0.5, fill=False, lw=1.6))
        ax.text(*pos, label, ha="center", va="center", fontsize=11)

    ax.add_patch(Circle(bias_pos, 0.4, fill=False, lw=1.6))
    ax.text(*bias_pos, "1", ha="center", va="center", fontsize=10)

    ax.add_patch(Circle(neuron_pos, 0.9, fill=False, lw=1.8))
    ax.text(neuron_pos[0], neuron_pos[1] + 0.15, r"$\Sigma\,f$", ha="center", va="center", fontsize=12)

    for pos, label, val in [(x1_pos, "w1", w[0]), (x2_pos, "w2", w[1])]:
        ax.annotate("", xy=(neuron_pos[0]-0.75, neuron_pos[1] + (0.5 if pos==x1_pos else -0.5)),
                     xytext=(pos[0]+0.5, pos[1]),
                     arrowprops=dict(arrowstyle="->", lw=1.4))
        mx, my = (pos[0]+neuron_pos[0])/2, (pos[1]+neuron_pos[1])/2
        ax.text(mx, my + 0.3, f"{label}={val:.2f}", fontsize=9, ha="center", color="tab:blue")

    ax.annotate("", xy=(neuron_pos[0], neuron_pos[1]+0.9), xytext=(bias_pos[0], bias_pos[1]-0.4),
                arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(bias_pos[0]+0.35, (bias_pos[1]+neuron_pos[1])/2 + 0.3, f"b={b:.2f}", fontsize=9, color="tab:red")

    ax.annotate("", xy=(9.3, 4), xytext=(neuron_pos[0]+0.9, 4), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.text(9.5, 4, "y", fontsize=11, va="center")

    thresh = "y=1 if y_in>0.5 else 0" if mode == "unipolar" else "y=1 if y_in>=0 else -1"
    ax.text(5, 0.6, f"{gate} gate ({mode})\nActivation: {thresh}", ha="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, filename), dpi=150)
    plt.close(fig)


def draw_xor_mlp(filename, weights=None):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis("off")

    x_pos = {"x1": (1, 6.5), "x2": (1, 2.5), "bias_in": (1, 8.5)}
    h_pos = {"h1": (5.5, 6.5), "h2": (5.5, 2.5), "bias_h": (5.5, 8.5)}
    o_pos = {"y": (10, 4.5)}

    for pos, label in [(x_pos["x1"], "x1"), (x_pos["x2"], "x2")]:
        ax.add_patch(Circle(pos, 0.5, fill=False, lw=1.6))
        ax.text(*pos, label, ha="center", va="center", fontsize=11)
    ax.add_patch(Circle(x_pos["bias_in"], 0.35, fill=False, lw=1.4))
    ax.text(*x_pos["bias_in"], "1", ha="center", va="center", fontsize=9)

    for pos, label in [(h_pos["h1"], "z1"), (h_pos["h2"], "z2")]:
        ax.add_patch(Circle(pos, 0.55, fill=False, lw=1.8))
        ax.text(pos[0], pos[1]+0.1, r"$\Sigma f$", ha="center", va="center", fontsize=10)
        ax.text(pos[0], pos[1]-0.9, label, ha="center", fontsize=9)
    ax.add_patch(Circle(h_pos["bias_h"], 0.35, fill=False, lw=1.4))
    ax.text(*h_pos["bias_h"], "1", ha="center", va="center", fontsize=9)

    ax.add_patch(Circle(o_pos["y"], 0.6, fill=False, lw=2))
    ax.text(o_pos["y"][0], o_pos["y"][1]+0.1, r"$\Sigma f$", ha="center", va="center", fontsize=11)
    ax.text(o_pos["y"][0], o_pos["y"][1]-1.0, "y", ha="center", fontsize=10)

    for xp in [x_pos["x1"], x_pos["x2"]]:
        for hp in [h_pos["h1"], h_pos["h2"]]:
            ax.annotate("", xy=(hp[0]-0.6, hp[1]), xytext=(xp[0]+0.5, xp[1]),
                        arrowprops=dict(arrowstyle="->", lw=1.0, color="gray"))
    for hp in [h_pos["h1"], h_pos["h2"]]:
        ax.annotate("", xy=(o_pos["y"][0]-0.65, o_pos["y"][1]), xytext=(hp[0]+0.6, hp[1]),
                    arrowprops=dict(arrowstyle="->", lw=1.2, color="black"))
    ax.annotate("", xy=(h_pos["h1"][0], h_pos["h1"][1]+0.55), xytext=(x_pos["bias_in"][0], x_pos["bias_in"][1]-0.3),
                arrowprops=dict(arrowstyle="->", lw=0.8, color="gray"))
    ax.annotate("", xy=(h_pos["h2"][0], h_pos["h2"][1]+0.55), xytext=(x_pos["bias_in"][0], x_pos["bias_in"][1]-0.3),
                arrowprops=dict(arrowstyle="->", lw=0.8, color="gray"))
    ax.annotate("", xy=(o_pos["y"][0], o_pos["y"][1]+0.6), xytext=(h_pos["bias_h"][0], h_pos["bias_h"][1]-0.3),
                arrowprops=dict(arrowstyle="->", lw=0.8, color="gray"))

    ax.text(1, 0.3, "Input\nlayer", ha="center", fontsize=10)
    ax.text(5.5, 0.3, "Hidden\nlayer", ha="center", fontsize=10)
    ax.text(10, 0.3, "Output\nlayer", ha="center", fontsize=10)

    if weights is not None:
        v = weights["v"]  # 2x2 input->hidden, vb: hidden bias (2,)
        w = weights["w"]  # 2 hidden->output, wb: scalar
        txt = (f"v11={v[0][0]:.2f} v21={v[1][0]:.2f} vb1={weights['vb'][0]:.2f}\n"
               f"v12={v[0][1]:.2f} v22={v[1][1]:.2f} vb2={weights['vb'][1]:.2f}\n"
               f"w1={w[0]:.2f} w2={w[1]:.2f} wb={weights['wb']:.2f}")
        ax.text(6, 8.7, txt, fontsize=8, ha="center", family="monospace")

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, filename), dpi=150)
    plt.close(fig)


def draw_mcp_xor(filename):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    x1, x2 = (1, 5.5), (1, 1.5)
    z1, z2 = (5.5, 5.5), (5.5, 1.5)
    y = (10, 3.5)

    for pos, label in [(x1, "x1"), (x2, "x2")]:
        ax.add_patch(Circle(pos, 0.5, fill=False, lw=1.6))
        ax.text(*pos, label, ha="center", va="center", fontsize=11)

    for pos, label in [(z1, "z1\n(OR)"), (z2, "z2\n(NAND)")]:
        ax.add_patch(Circle(pos, 0.55, fill=False, lw=1.8))
        ax.text(pos[0], pos[1], label, ha="center", va="center", fontsize=9)

    ax.add_patch(Circle(y, 0.6, fill=False, lw=2))
    ax.text(y[0], y[1], "y\n(AND)", ha="center", va="center", fontsize=10)

    for xp in [x1, x2]:
        for zp, w in zip([z1, z2], ["+1", "-1"]):
            ax.annotate("", xy=(zp[0]-0.6, zp[1]), xytext=(xp[0]+0.5, xp[1]),
                        arrowprops=dict(arrowstyle="->", lw=1.2))
            mx, my = (xp[0]+zp[0])/2, (xp[1]+zp[1])/2 + (0.25 if xp==x1 else -0.25)
            ax.text(mx, my, w, fontsize=8, color="tab:blue")

    for zp in [z1, z2]:
        ax.annotate("", xy=(y[0]-0.65, y[1]), xytext=(zp[0]+0.6, zp[1]),
                    arrowprops=dict(arrowstyle="->", lw=1.4))
        mx, my = (zp[0]+y[0])/2, (zp[1]+y[1])/2
        ax.text(mx, my+0.2, "+1", fontsize=8, color="tab:blue")

    ax.text(1, 7, "Input\nlayer", ha="center", fontsize=10)
    ax.text(5.5, 7, "Hidden layer\n(theta1=1, theta2=-1)", ha="center", fontsize=10)
    ax.text(10, 6, "Output layer\n(theta=2)", ha="center", fontsize=10)
    ax.text(6, 0.2,
            "z1 = OR(x1,x2): w=(1,1), theta=1\n"
            "z2 = NAND(x1,x2): w=(-1,-1), theta=-1\n"
            "y = AND(z1,z2): w=(1,1), theta=2\n"
            "y = 1 if y_in >= theta else 0",
            ha="center", fontsize=8.5, family="monospace")

    fig.tight_layout()
    fig.savefig(os.path.join(outdir, filename), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    with open(os.path.join(outdir, "adaline_results.json")) as f:
        results = json.load(f)

    for mode in ["unipolar", "bipolar"]:
        for gate in ["AND", "OR", "NAND", "NOR"]:
            r = results[mode][gate]
            draw_single_neuron(gate, r["final_weights"], r["final_bias"], mode,
                                f"neuron_{gate.lower()}_{mode}.png")

    draw_xor_mlp("xor_mlp_blank.png")
    draw_mcp_xor("mcp_xor_diagram.png")
    print("Saved neuron and MLP diagrams to", outdir)
