# parameter variation study for the AND gate (assignment 1)
# checks how learning rate and initial weight scale affect convergence speed

import json
import os
import numpy as np
from adaline import run_gate

outdir = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(outdir, exist_ok=True)

alphas = [0.01, 0.05, 0.1, 0.3, 0.5, 0.9]
seeds = [1, 2, 3, 4, 5]

alpha_rows = []
for a in alphas:
    epochs_list = []
    for s in seeds:
        res = run_gate("AND", "unipolar", alpha=a, seed=s, tol=1e-3, max_epochs=1000)
        fce = res["first_correct_epoch"] if res["first_correct_epoch"] is not None else 1000
        epochs_list.append(fce)
    alpha_rows.append({
        "alpha": a,
        "mean_epochs_to_correct": float(np.mean(epochs_list)),
        "std_epochs_to_correct": float(np.std(epochs_list)),
        "runs": epochs_list,
    })
    print(f"alpha={a}: mean epochs to correct = {np.mean(epochs_list):.2f}")

w_scales = [0.1, 0.5, 1.0, 2.0]
wscale_rows = []
for ws in w_scales:
    epochs_list = []
    for s in seeds:
        res = run_gate("AND", "unipolar", alpha=0.1, seed=s, tol=1e-3, max_epochs=1000, w_init_scale=ws)
        fce = res["first_correct_epoch"] if res["first_correct_epoch"] is not None else 1000
        epochs_list.append(fce)
    wscale_rows.append({
        "w_init_scale": ws,
        "mean_epochs_to_correct": float(np.mean(epochs_list)),
        "std_epochs_to_correct": float(np.std(epochs_list)),
        "runs": epochs_list,
    })
    print(f"w_init_scale={ws}: mean epochs to correct = {np.mean(epochs_list):.2f}")

with open(os.path.join(outdir, "param_study.json"), "w") as f:
    json.dump({"alpha_study": alpha_rows, "w_scale_study": wscale_rows}, f, indent=2)

print("saved outputs/param_study.json")
