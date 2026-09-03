# My Neural Network Lab 7

This folder is for rebuilding the experiment yourself. The original Claude files are outside this folder and will not be changed.

## Learning sequence

1. Build and inspect the truth tables.
2. Compute one Adaline update by hand.
3. Implement a single Adaline neuron for AND.
4. Extend it to OR, NAND, and NOR.
5. Compare unipolar and bipolar encodings.
6. Study learning rate and initial-weight scale.
7. Build XOR from fixed McCulloch-Pitts units.
8. Train a 2-2-1 XOR network using backpropagation.

## Step 1

Run:

```powershell
cd "G:\downloads\Lab 7\my_lab7"
python step01_truth_tables.py
```

Before moving on, be able to explain every row printed by the program and answer:

- What is the difference between unipolar and bipolar input values?
- Why is XOR different from AND, OR, NAND, and NOR?
- For a neuron with weights `w1`, `w2`, and bias `b`, what value is calculated before thresholding?

Do not copy the original implementation yet. The goal is to understand the data first.

## Step 2

Open `step02_manual_update.py` and calculate the first two updates on paper before running it:

```powershell
python step02_manual_update.py
```

The update is online: the weights changed by pattern 1 are immediately used for pattern 2.
Compare your calculations with the program output. Focus on why an input value of zero produces
no direct update to that input's weight.

## Step 3

Run the complete single-neuron AND experiment:

```powershell
python step03_adaline_and.py
```

This is the first real training program. Read the `train` function line by line and identify where
it performs the forward calculation, error calculation, weight update, bias update, and stopping
test. The program stops once all four AND patterns are classified correctly.

## Step 4

Run:

```powershell
python step04_adaline_gates.py
```

Compare the four target vectors. The input patterns and learning algorithm are unchanged. Only
the desired outputs differ. Because the starting values are fixed in this exercise, your results
will be reproducible.

## Step 5

Study the learning rate:

```powershell
python step05_learning_rate.py
```

The program repeats AND training with five starting seeds. `1000` means that the run did not
classify every AND row correctly within the allowed limit. Look for the middle learning rates
that work quickly and the large learning rate that becomes unstable.

## Step 6

Compare unipolar and bipolar training:

```powershell
python step06_bipolar_compare.py
```

Pay attention to the input row `(0, 0)` in the unipolar version versus `(-1, -1)` in the bipolar
version. In the bipolar version, both weights receive an update on every pattern because neither
input is zero.

## Step 7

Run the hand-designed McCulloch-Pitts XOR network:

```powershell
python step07_mcp_xor.py
```

Trace each row through the two hidden units and then the output unit. This network does not learn;
you provide the weights and thresholds deliberately.

## Step 8

Train XOR using backpropagation:

```powershell
python step08_backprop_xor.py
```

Read the `forward` and `train` functions together. The forward pass calculates the hidden and
output activations. The training loop then sends the output error backward and updates the output
layer before the hidden layer.
