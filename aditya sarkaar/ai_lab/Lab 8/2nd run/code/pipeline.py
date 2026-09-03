"""
Lab 8 - Iris ML pipeline, second attempt.
Same assignment, just organized a bit differently this time - grouped the
repeated "train + score" bit into a tiny helper, and used pandas for the
cross-entropy part instead of looping by hand.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, log_loss

# rough color scheme for all the plots in this run
TEAL = "#118AB2"
CORAL = "#EF476F"
GOLD = "#FFD166"
GREEN = "#06D6A0"
NAVY = "#073B4C"

plt.rcParams["axes.grid"] = True
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.4
plt.rcParams["axes.facecolor"] = "#F5FBFC"
plt.rcParams["figure.dpi"] = 130

OUT_DIR = "../outputs/"


def acc(model, X, y):
    """just saves typing accuracy_score(y, model.predict(X)) everywhere"""
    return accuracy_score(y, model.predict(X))


# --------------------------------------------------
# Part 1 - get the data ready
# --------------------------------------------------

iris = load_iris()
X, y = iris.data, iris.target
classes = iris.target_names

X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_val = sc.transform(X_val)
X_test = sc.transform(X_test)

split_sizes = {"train": len(X_train), "val": len(X_val), "test": len(X_test)}
print("split sizes ->", split_sizes)

# --------------------------------------------------
# Part 2 - generative (Naive Bayes) vs discriminative (Logistic Regression)
# --------------------------------------------------

nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
nb_val_acc = acc(nb_model, X_val, y_val)

logit_model = LogisticRegression(max_iter=1000, random_state=42)
logit_model.fit(X_train, y_train)
logit_val_acc = acc(logit_model, X_val, y_val)

print(f"NaiveBayes val acc = {nb_val_acc:.3f}, LogisticRegression val acc = {logit_val_acc:.3f}")

# horizontal bar this time just for a different look than a plain vertical bar
plt.figure(figsize=(5.5, 3))
plt.barh(["Logistic Regression\n(discriminative)", "Gaussian Naive Bayes\n(generative)"],
         [logit_val_acc, nb_val_acc], color=[TEAL, CORAL])
plt.xlim(0, 1)
plt.xlabel("validation accuracy")
plt.title("Model comparison on validation set")
for i, v in enumerate([logit_val_acc, nb_val_acc]):
    plt.text(v + 0.02, i, f"{v:.3f}", va="center")
plt.tight_layout()
plt.savefig(OUT_DIR + "gen_vs_disc.png")
plt.close()

# --------------------------------------------------
# Part 3 - decision tree capacity (underfit / overfit)
# --------------------------------------------------

depth_options = [1, 3, 5, None]
depth_labels = [str(d) for d in depth_options]
train_scores = []
val_scores = []

for depth in depth_options:
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    clf.fit(X_train, y_train)
    train_scores.append(acc(clf, X_train, y_train))
    val_scores.append(acc(clf, X_val, y_val))

for d, tr, va in zip(depth_labels, train_scores, val_scores):
    print(f"depth={d:<4} train={tr:.3f}  val={va:.3f}")

# grouped bar chart instead of a line plot
x_pos = np.arange(len(depth_options))
width = 0.35
plt.figure(figsize=(6.5, 4))
plt.bar(x_pos - width / 2, train_scores, width, label="train", color=NAVY)
plt.bar(x_pos + width / 2, val_scores, width, label="validation", color=GOLD)
plt.xticks(x_pos, depth_labels)
plt.xlabel("max_depth")
plt.ylabel("accuracy")
plt.ylim(0, 1.1)
plt.title("Decision tree: train vs validation accuracy by depth")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR + "tree_capacity.png")
plt.close()

# --------------------------------------------------
# Part 4 - pick max_depth using the validation set, then touch the test set once
# --------------------------------------------------

best_pos = val_scores.index(max(val_scores))
chosen_depth = depth_options[best_pos]

best_tree = DecisionTreeClassifier(max_depth=chosen_depth, random_state=42)
best_tree.fit(X_train, y_train)
test_accuracy = acc(best_tree, X_test, y_test)

print("chosen depth:", chosen_depth, "-> test accuracy:", round(test_accuracy, 3))

# --------------------------------------------------
# Part 5 - bias / variance talk (reusing numbers from part 3, nothing new to compute)
# --------------------------------------------------

print("shallow tree (depth=1):", train_scores[0], val_scores[0])
print("unrestricted tree (depth=None):", train_scores[-1], val_scores[-1])

# --------------------------------------------------
# Part 6 - cross entropy for the logistic regression model
# --------------------------------------------------

proba = logit_model.predict_proba(X_val)
val_loss = log_loss(y_val, proba)
print("val log loss:", val_loss)

# build a little table with pandas, easier to slice/sort than doing it by hand
val_df = pd.DataFrame({
    "true_label": y_val,
    "pred_label": logit_model.predict(X_val),
})
val_df["true_class_name"] = val_df["true_label"].apply(lambda i: classes[i])
val_df["prob_of_true_class"] = [proba[i, y_val[i]] for i in range(len(y_val))]
val_df["loss"] = -np.log(val_df["prob_of_true_class"])
val_df["correct"] = val_df["true_label"] == val_df["pred_label"]

most_confident_right = val_df[val_df["correct"]].sort_values("loss").iloc[0]
most_confident_wrong = val_df[~val_df["correct"]].sort_values("loss", ascending=False).iloc[0]

print("best correct prediction:\n", most_confident_right)
print("worst wrong prediction:\n", most_confident_wrong)

sorted_df = val_df.sort_values("loss").reset_index(drop=True)
bar_colors = [GREEN if c else CORAL for c in sorted_df["correct"]]

plt.figure(figsize=(6.5, 4))
plt.scatter(sorted_df.index, sorted_df["loss"], c=bar_colors, s=60, edgecolor="black", linewidth=0.4)
plt.axhline(val_loss, color=NAVY, linestyle=":", label=f"mean = {val_loss:.3f}")
plt.xlabel("validation sample (sorted by loss)")
plt.ylabel("cross entropy loss")
plt.title("Per-sample loss (green=correct, coral=wrong)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR + "cross_entropy.png")
plt.close()

# --------------------------------------------------
# Part 7 - MLE vs MAP, using regularization strength C as the knob
# --------------------------------------------------

C_grid = np.logspace(-3, 3, 7)  # 0.001 ... 1000
norms = []
accs_for_C = []

for c in C_grid:
    m = LogisticRegression(C=c, max_iter=2000, random_state=42)
    m.fit(X_train, y_train)
    norms.append(np.linalg.norm(m.coef_))
    accs_for_C.append(acc(m, X_val, y_val))

fig, (top, bottom) = plt.subplots(2, 1, figsize=(6.5, 5.5), sharex=True)
top.plot(C_grid, norms, marker="o", color=TEAL)
top.set_xscale("log")
top.set_ylabel("||w||")
top.set_title("Weight norm vs regularization strength C")

bottom.plot(C_grid, accs_for_C, marker="s", color=CORAL)
bottom.set_xscale("log")
bottom.set_ylabel("val accuracy")
bottom.set_xlabel("C (log scale)")
bottom.set_ylim(0.5, 1.05)

fig.tight_layout()
fig.savefig(OUT_DIR + "mle_map.png")
plt.close(fig)

# --------------------------------------------------
# dump everything used in the report so numbers don't get typed twice
# --------------------------------------------------

summary = {
    "split_sizes": split_sizes,
    "nb_val_acc": nb_val_acc,
    "logit_val_acc": logit_val_acc,
    "depths": depth_labels,
    "train_scores": train_scores,
    "val_scores": val_scores,
    "chosen_depth": str(chosen_depth),
    "test_accuracy": test_accuracy,
    "val_log_loss": val_loss,
    "best_correct_sample": most_confident_right.to_dict(),
    "worst_wrong_sample": most_confident_wrong.to_dict(),
    "C_grid": C_grid.tolist(),
    "weight_norms": norms,
    "acc_vs_C": accs_for_C,
}

with open(OUT_DIR + "results.json", "w") as f:
    json.dump(summary, f, indent=2, default=str)

print("all done, check outputs/ folder")
