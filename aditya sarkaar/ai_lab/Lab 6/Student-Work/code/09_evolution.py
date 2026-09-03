import csv
import importlib
import json
from pathlib import Path


fitness_module = importlib.import_module("07_fitness")
operators = importlib.import_module("08_genetic_operators")


POPULATION_SIZE = 50
GENERATIONS = 200
TRAINING_RUNS = 3


def score_population(population, starts):
    return [
        fitness_module.fitness(chromosome, starts)
        for chromosome in population
    ]


def evolve(seed=61):
    """Evolve a population and return its history and best chromosome."""
    starts = fitness_module.make_starts(seed=21, count=TRAINING_RUNS)
    population = fitness_module.make_population(
        size=POPULATION_SIZE,
        seed=seed,
    )
    history = []
    best_chromosome = None
    best_fitness = -1.0

    for generation in range(GENERATIONS):
        scores = score_population(population, starts)
        generation_best = max(scores)

        if generation_best > best_fitness:
            best_fitness = generation_best
            best_index = scores.index(generation_best)
            best_chromosome = population[best_index][:]

        history.append({
            "generation": generation,
            "average": sum(scores) / len(scores),
            "best": generation_best,
            "worst": min(scores),
        })

        population, _ = operators.make_next_generation(
            population,
            scores,
            seed=seed + generation + 1,
        )

    return history, best_chromosome


def save_history(history, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["generation", "average", "best", "worst"],
        )
        writer.writeheader()
        writer.writerows(history)


def save_chromosome(chromosome, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(chromosome, file, indent=2)


if __name__ == "__main__":
    history, best_chromosome = evolve()
    output_path = Path(__file__).resolve().parent.parent / "outputs" / "fitness_history.csv"
    chromosome_path = Path(__file__).resolve().parent.parent / "outputs" / "best_chromosome.json"
    save_history(history, output_path)
    save_chromosome(best_chromosome, chromosome_path)

    print("Population size:", POPULATION_SIZE)
    print("Generations:", GENERATIONS)
    print("Initial average fitness:", f"{history[0]['average']:.2%}")
    print("Final average fitness:", f"{history[-1]['average']:.2%}")
    print("Best fitness found:", f"{max(item['best'] for item in history):.2%}")
    print("Best chromosome length:", len(best_chromosome))
    print("History saved to:", output_path)
    print("Best chromosome saved to:", chromosome_path)
