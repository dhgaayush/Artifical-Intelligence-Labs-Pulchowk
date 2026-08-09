"""
fitness.py

Fitness evaluation module for the Genetic Algorithm
Painter Robot project.
"""

import numpy as np

from painter import simulate_multiple_runs


# ==========================================================
# SINGLE CHROMOSOME
# ==========================================================

def evaluate_chromosome(chromosome, room, runs=5):
    """
    Evaluate a single chromosome by averaging multiple
    simulation runs.
    """

    result = simulate_multiple_runs(
        chromosome,
        room,
        runs
    )

    return result["average_efficiency"]


# ==========================================================
# POPULATION
# ==========================================================

def evaluate_population(population, room, runs=5):
    """
    Evaluate every chromosome in a population.

    Parameters
    ----------
    population : ndarray
    room : ndarray
    runs : int

    Returns
    -------
    ndarray
        Fitness values for every chromosome.
    """

    fitness = np.zeros(len(population))

    for i, chromosome in enumerate(population):

        fitness[i] = evaluate_chromosome(
            chromosome,
            room,
            runs
        )

    return fitness


# ==========================================================
# STATISTICS
# ==========================================================

def population_statistics(fitness):
    """
    Return useful statistics for a fitness array.
    """

    return {
        "best": float(np.max(fitness)),
        "worst": float(np.min(fitness)),
        "average": float(np.mean(fitness)),
        "std": float(np.std(fitness))
    }


# ==========================================================
# BEST CHROMOSOME
# ==========================================================

def get_best_chromosome(population, fitness):
    """
    Return the best chromosome and its fitness.
    """

    index = np.argmax(fitness)

    return (
        population[index].copy(),
        float(fitness[index])
    )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    from environment import create_empty_room
    from genetic_algorithm import create_population

    room = create_empty_room()

    population = create_population()

    fitness = evaluate_population(
        population,
        room,
        runs=3
    )

    stats = population_statistics(fitness)

    print("\nPopulation Statistics")
    print("---------------------")
    print(f"Best    : {stats['best']:.3f}")
    print(f"Average : {stats['average']:.3f}")
    print(f"Worst   : {stats['worst']:.3f}")
    print(f"Std Dev : {stats['std']:.3f}")