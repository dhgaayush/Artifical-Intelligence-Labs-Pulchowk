import importlib
import random


# The filename starts with a number, so importlib is used instead of a normal
# ``from 06_simulation import ...`` statement.
simulation = importlib.import_module("06_simulation")


TRAINING_RUNS = 3
POPULATION_SIZE = 10


def make_starts(seed=21, count=TRAINING_RUNS):
    """Create reproducible starting positions and directions."""
    generator = random.Random(seed)
    starts = []

    for _ in range(count):
        row = generator.randrange(simulation.ROWS)
        col = generator.randrange(simulation.COLS)
        direction = generator.randrange(4)
        starts.append((row, col, direction))

    return starts


def fitness(chromosome, starts):
    """Return average coverage across several starting positions."""
    efficiencies = []

    for run_number, (row, col, direction) in enumerate(starts):
        result = simulation.simulate(
            chromosome,
            row,
            col,
            direction,
            seed=100 + run_number,
        )
        efficiencies.append(result["efficiency"])

    return sum(efficiencies) / len(efficiencies)


def make_population(size=POPULATION_SIZE, seed=31):
    generator = random.Random(seed)
    return [
        [generator.randrange(4) for _ in range(simulation.STATE_COUNT)]
        for _ in range(size)
    ]


if __name__ == "__main__":
    starts = make_starts()
    population = make_population()
    scored_population = [
        (fitness(chromosome, starts), number, chromosome)
        for number, chromosome in enumerate(population, start=1)
    ]
    scored_population.sort(reverse=True, key=lambda item: item[0])

    print("Training starts:", starts)
    print("Population size:", len(population))
    print("Best fitness:", f"{scored_population[0][0]:.2%}")
    print("Worst fitness:", f"{scored_population[-1][0]:.2%}")
    print("Ranking:")

    for score, number, _ in scored_population:
        print(f"  Chromosome {number:02d}: {score:.2%}")
