# Neural Network Lab Quick Notes

## Evolution
- **McCulloch-Pitts (MCP):** Fixed weights, threshold neuron, **no learning**.
- **Perceptron:** MCP + learns weights.
- **ADALINE:** Learns using the **linear output** before thresholding (Delta/LMS rule).
- **MLP:** Multiple perceptrons trained using **backpropagation**.

## 1. McCulloch-Pitts (MCP)
- Computes weighted sum: `Σ(wᵢxᵢ)`
- Output:
  - 1 if sum ≥ threshold
  - 0 otherwise
- Weights are chosen manually.
- Solves simple logic gates (AND, OR, etc.).

## 2. Perceptron
- Same neuron as MCP but **learns** weights.
- Update rule:
  `w_new = w_old + α(t − y)x`
- Error is computed **after thresholding**.

## 3. ADALINE
- **Adaptive Linear Neuron**
- Uses the **linear neuron output (`y_in`)** during training.
- Delta/LMS (Widrow–Hoff) update:
  `w_new = w_old + α(t − y_in)x`
- Continues improving even if classification is already correct.

## 4. Delta Rule (LMS / Widrow–Hoff)
All three names refer to the same learning rule.
- Error = `target − y_in`
- Used by ADALINE.

## 5. Learning Rate (α)
- Small α → slow, stable learning.
- Large α → faster but may oscillate.

## 6. Bias
- Shifts the decision boundary.
- Equivalent to a threshold.

## 7. Transfer Functions
- **Linear:** Output = weighted sum.
- **Threshold:** Binary (0/1).
- **Sigmoid:** Smooth S-shaped function.

## 8. Backpropagation
- Training algorithm for MLPs.
- Propagates errors backward using the chain rule.

## 9. MLP (Multi-Layer Perceptron)
Input → Hidden Layer(s) → Output
- Can solve nonlinear problems.
- Trained with backpropagation.

## 10. XOR
Single-layer MCP/Perceptron **cannot** solve XOR because it is **not linearly separable**.
An MLP with at least one hidden layer can.

## Lab Assignment Mapping
- AND/OR/NAND/NOR: MCP neuron + ADALINE learning.
- XOR: Implement using an MLP + backpropagation.

## Key Differences

| Model | Learns? | Error Computed On | Multi-layer? |
|-------|---------|-------------------|--------------|
| MCP | ❌ | N/A | ❌ |
| Perceptron | ✅ | Thresholded output | ❌ |
| ADALINE | ✅ | Linear output (`y_in`) | ❌ |
| MLP | ✅ | Backpropagation | ✅ |
