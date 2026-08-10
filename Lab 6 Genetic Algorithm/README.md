# AI Genetic Painter Robot

This project uses a genetic algorithm to evolve a control policy for a painting robot. The robot explores a room, paints empty cells, and avoids obstacles. The genetic algorithm searches for a chromosome that makes the robot behave well over many simulation runs.

## 1. Biological inspiration

Biological evolution is not purely deterministic and not purely random:

- Mutation and recombination are largely stochastic.
- Natural selection is not random; it favors organisms that survive and reproduce better.
- So evolution is best understood as random variation guided by selection.

That same idea is used here:

- the algorithm creates random candidate solutions,
- it combines and mutates them,
- and it keeps the ones that perform better according to fitness.

## 2. What we agreed on before implementing

To make the system practical, the implementation uses a few fixed constraints:

- The robot policy is encoded as a chromosome of length 54.
- Each gene is one of four action values: 0, 1, 2, or 3.
- The room is represented as a 2D integer array.
- The robot’s current environment is reduced to a small state tuple.
- Fitness is measured by how efficiently the robot paints the room over repeated runs.

These choices keep the problem simple enough to evolve while still being meaningful.

## 3. Main idea of the program

The program works in this order:

1. Create an initial random population of chromosomes.
2. Evaluate each chromosome by simulating the robot.
3. Select parents based on fitness.
4. Create children using crossover and mutation.
5. Repeat for several generations.
6. Return the best chromosome found.

## 4. Key terms

- Chromosome: one candidate policy for the robot.
- Gene: one value inside the chromosome.
- Population: a group of chromosomes.
- Fitness: how good a chromosome is.
- Selection: choosing parents for the next generation.
- Crossover: combining two parent chromosomes.
- Mutation: randomly changing one or more genes.
- Generation: one full round of evaluation and reproduction.

## 5. Project structure

- main.py: entry point of the program
- genetic_algorithm.py: GA logic
- fitness.py: fitness evaluation
- painter.py: robot simulation and chromosome decoding
- environment.py: room creation and environment helpers
- visualisation.py: plotting and reporting
- requirements.txt: Python dependencies

## 6. Dependency overview

The project depends mainly on:

- numpy
- matplotlib

## 7. How the modules relate

- main.py calls genetic_algorithm.py
- genetic_algorithm.py calls fitness.py
- fitness.py calls painter.py
- painter.py uses environment.py
- visualisation.py is used to display results after the GA finishes

## 8. Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

## 9. Notes

This is a simplified GA model. It is inspired by biology, but it is not a full biological simulation. It is a practical computational method for searching for a good robot policy.
