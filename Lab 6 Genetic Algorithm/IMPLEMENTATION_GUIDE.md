# Implementation Guide

This file explains the implementation details of the genetic algorithm and the robot simulation used in this project.

## 1. Overall flow

The project is built around a simple loop:

1. A population of chromosomes is created.
2. Each chromosome is evaluated by simulating the robot.
3. Better chromosomes are selected as parents.
4. New children are produced by crossover and mutation.
5. The process repeats for several generations.

## 2. Representation choices agreed in advance

The implementation uses a fixed representation so the GA can work consistently:

- Chromosome length: 54
- Gene values: 0, 1, 2, 3
- Room representation: NumPy array of integers
- Robot state: current cell plus the cells in front, left, and right
- Action mapping: each chromosome entry chooses an action for a specific state

## 3. Chromosome meaning

Each chromosome is a lookup table for the robot.

The robot observes a local state:

- current cell
- forward cell
- left cell
- right cell

That state is encoded into an index from 0 to 53. The chromosome entry at that index tells the robot what action to take.

Possible actions:

- 0: go straight
- 1: turn left
- 2: turn right
- 3: random left/right choice

## 4. Array ranges and shapes

### Room array

- The room is a 2D NumPy array.
- Values are:
  - 0 = empty
  - 1 = obstacle
  - 2 = painted

### Chromosome array

- A chromosome is a 1D NumPy array of length 54.
- Each entry is an integer in the set {0, 1, 2, 3}.

### Population array

- The population is a 2D NumPy array.
- Shape is roughly: (population_size, 54).

## 5. GA components

### Initialization

The function initialize_chromosome creates one random chromosome.

The function create_population creates the first population.

### Selection

Two selection methods are supported:

- roulette wheel selection
- tournament selection

### Crossover

The implementation uses single-point crossover.

A random crossover point is chosen, and the two parents swap gene segments after that point.

### Mutation

Mutation randomly changes some genes according to a mutation rate.

## 6. Program modules and responsibilities

### main.py

Runs the whole project.

It:

- creates the room,
- runs the GA,
- prints a summary,
- plots fitness history,
- displays the best solution.

### genetic_algorithm.py

Contains the GA core.

It handles:

- population creation,
- parent selection,
- crossover,
- mutation,
- generation evolution.

### fitness.py

Evaluates chromosomes.

It calls the simulation code and returns fitness values.

### painter.py

This is the robot simulator.

It handles:

- sensing the environment,
- choosing an action from the chromosome,
- turning the robot,
- painting cells,
- moving forward,
- computing efficiency.

### environment.py

Creates and manages the room environment.

### visualisation.py

Shows plots and summaries for the GA run.

## 7. Important implementation detail

The GA evaluates each chromosome using multiple simulation runs.

This matters because the robot starts in a random position and orientation. A single run can be noisy, so averaging several runs produces a more reliable fitness value.

## 8. Call flow

A simplified call chain is:

- main.py -> genetic_algorithm.py
- genetic_algorithm.py -> fitness.py
- fitness.py -> painter.py
- painter.py -> environment.py
- visualisation.py -> painter.py for display results

## 9. Dependencies

The project requires:

- numpy
- matplotlib

These are listed in requirements.txt.

## 10. Running the project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```
