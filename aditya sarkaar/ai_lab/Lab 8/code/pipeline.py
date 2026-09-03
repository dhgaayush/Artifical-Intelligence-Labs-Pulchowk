# AI Lab 8 - Iris dataset ML pipeline (Assignments 1-7)

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")  # so plots save fine when run from terminal, no popup window
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, log_loss

# ---------- Assignment 1: load data and build train/val/test split ----------

iris = load_iris()
X = iris.data
y = iris.target
class_names = iris.target_names

# first pull out 20% as the final test set
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
# then split what's left into train and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

print("train samples:", len(X_train))
print("val samples:", len(X_val))
print("test samples:", len(X_test))

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# ---------- Assignment 2: Gaussian Naive Bayes vs Logistic Regression ----------

gnb = GaussianNB()
gnb.fit(X_train, y_train)
gnb_acc = accuracy_score(y_val, gnb.predict(X_val))
print("GaussianNB val accuracy:", gnb_acc)

logreg = LogisticRegression(max_iter=1000, random_state=42)
logreg.fit(X_train, y_train)
logreg_acc = accuracy_score(y_val, logreg.predict(X_val))
print("Logistic Regression val accuracy:", logreg_acc)

plt.figure(figsize=(5, 4))
plt.bar(["Gaussian NB", "Logistic Regression"], [gnb_acc, logreg_acc], color=["#4C72B0", "#DD8452"])
plt.ylabel("validation accuracy")
plt.ylim(0, 1.05)
plt.title("Generative vs Discriminative model")
plt.savefig("../outputs/gen_vs_disc.png")
plt.close()

# ---------- Assignment 3: decision tree capacity ----------

depths = [1, 3, 5, None]
depth_labels = ["1", "3", "5", "None"]
train_accs = []
val_accs = []

for d in depths:
    tree = DecisionTreeClassifier(max_depth=d, random_state=42)
    tree.fit(X_train, y_train)
    tr_acc = accuracy_score(y_train, tree.predict(X_train))
    va_acc = accuracy_score(y_val, tree.predict(X_val))
    train_accs.append(tr_acc)
    val_accs.append(va_acc)
    print("depth =", d, " train acc =", round(tr_acc, 3), " val acc =", round(va_acc, 3))

plt.figure(figsize=(6, 4))
plt.plot(depth_labels, train_accs, marker="o", label="train accuracy")
plt.plot(depth_labels, val_accs, marker="s", label="val accuracy")
plt.xlabel("max_depth")
plt.ylabel("accuracy")
plt.ylim(0.5, 1.05)
plt.title("Decision tree accuracy vs depth")
plt.legend()
plt.savefig("../outputs/tree_capacity.png")
plt.close()

# ---------- Assignment 4: pick best depth using validation set ----------

best_i = val_accs.index(max(val_accs))
best_depth = depths[best_i]
print("best depth based on validation set:", best_depth)

final_tree = DecisionTreeClassifier(max_depth=best_depth, random_state=42)
final_tree.fit(X_train, y_train)
test_acc = accuracy_score(y_test, final_tree.predict(X_test))
print("final test accuracy:", test_acc)

# ---------- Assignment 5: bias/variance, just comparing shallow vs deep tree ----------

print("shallow tree (depth=1)  train:", train_accs[0], " val:", val_accs[0])
print("deep tree (depth=None)  train:", train_accs[3], " val:", val_accs[3])

# ---------- Assignment 6: cross entropy / log loss for logistic regression ----------

probs = logreg.predict_proba(X_val)
val_logloss = log_loss(y_val, probs)
print("validation log loss:", val_logloss)

preds = logreg.predict(X_val)
losses = []
for i in range(len(y_val)):
    p = probs[i][y_val[i]]
    losses.append(-np.log(p))

# find the most confident correct prediction and the worst wrong one
best_correct = None
worst_wrong = None
for i in range(len(y_val)):
    if preds[i] == y_val[i]:
        if best_correct is None or losses[i] < losses[best_correct]:
            best_correct = i
    else:
        if worst_wrong is None or losses[i] > losses[worst_wrong]:
            worst_wrong = i

print("most confident correct sample:", best_correct, class_names[y_val[best_correct]], "loss =", losses[best_correct])
print("most confident wrong sample:", worst_wrong, "true:", class_names[y_val[worst_wrong]],
      "predicted:", class_names[preds[worst_wrong]], "loss =", losses[worst_wrong])

order = sorted(range(len(losses)), key=lambda i: losses[i])
colors = ["#55A868" if preds[i] == y_val[i] else "#C44E52" for i in order]

plt.figure(figsize=(6.5, 4))
plt.bar(range(len(losses)), [losses[i] for i in order], color=colors)
plt.axhline(val_logloss, linestyle="--", color="black", label=f"mean loss = {val_logloss:.3f}")
plt.xlabel("validation samples (sorted by loss)")
plt.ylabel("cross entropy loss")
plt.title("Per-sample cross entropy (green = correct, red = wrong)")
plt.legend()
plt.savefig("../outputs/cross_entropy.png")
plt.close()

# ---------- Assignment 7: MLE vs MAP, effect of regularization strength C ----------

C_values = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
weight_norms = []
val_accs_C = []

for C in C_values:
    m = LogisticRegression(C=C, max_iter=2000, random_state=42)
    m.fit(X_train, y_train)
    weight_norms.append(np.linalg.norm(m.coef_))
    val_accs_C.append(accuracy_score(y_val, m.predict(X_val)))
    print("C =", C, " weight norm =", round(weight_norms[-1], 3), " val acc =", round(val_accs_C[-1], 3))

fig, ax1 = plt.subplots(figsize=(6.5, 4))
ax1.plot(C_values, weight_norms, marker="o", color="#4C72B0")
ax1.set_xscale("log")
ax1.set_xlabel("C (log scale)")
ax1.set_ylabel("weight norm ||w||", color="#4C72B0")

ax2 = ax1.twinx()
ax2.plot(C_values, val_accs_C, marker="s", color="#C44E52")
ax2.set_ylabel("validation accuracy", color="#C44E52")
ax2.set_ylim(0.5, 1.05)

plt.title("Effect of regularization strength on weights / accuracy")
fig.tight_layout()
fig.savefig("../outputs/mle_map.png")
plt.close()

# ---------- save everything needed for the report ----------

results = {
    "n_train": len(X_train),
    "n_val": len(X_val),
    "n_test": len(X_test),
    "gnb_val_acc": gnb_acc,
    "logreg_val_acc": logreg_acc,
    "tree_depths": depth_labels,
    "tree_train_acc": train_accs,
    "tree_val_acc": val_accs,
    "best_depth": str(best_depth),
    "final_test_acc": test_acc,
    "val_log_loss": val_logloss,
    "C_values": C_values,
    "weight_norms": weight_norms,
    "val_acc_vs_C": val_accs_C,
}

with open("../outputs/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("done, results saved to outputs/results.json")
