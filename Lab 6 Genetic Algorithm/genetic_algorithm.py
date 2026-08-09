"""
genetic_algorithm.py

Generic Genetic Algorithm implementation for the
AI Painter Robot project.

This module is responsible ONLY for evolving
chromosomes.

Fitness evaluation is handled by fitness.py.
"""

import random
import numpy as np

from fitness import evaluate_population


# ==========================================================
# POPULATION INITIALIZATION
# ==========================================================

def initialize_chromosome(length=54, gene_values=(0, 1, 2, 3)):
    """
    Create one random chromosome.
    """

    return np.random.choice(
        gene_values,
        size=length
    )


def create_population(
    pop_size=50,
    chromosome_length=54,
    gene_values=(0, 1, 2, 3)
):
    """
    Create an initial random population.
    """

    return np.array([

        initialize_chromosome(
            chromosome_length,
            gene_values
        )

        for _ in range(pop_size)

    ])


# ==========================================================
# SELECTION
# ==========================================================

def roulette_wheel_selection(population, fitness):
    """
    Select one parent using roulette-wheel selection.
    """

    total = np.sum(fitness)

    # Prevent division by zero
    if total == 0:

        index = np.random.randint(len(population))

        return population[index]

    probabilities = fitness / total

    index = np.random.choice(
        len(population),
        p=probabilities
    )

    return population[index]


def tournament_selection(
    population,
    fitness,
    tournament_size=3
):
    """
    Tournament Selection.
    """

    indices = np.random.choice(
        len(population),
        tournament_size,
        replace=False
    )

    best = indices[np.argmax(fitness[indices])]

    return population[best]


def select_parents(
    population,
    fitness,
    method="roulette"
):
    """
    Select two parents.
    """

    if method == "roulette":

        parent1 = roulette_wheel_selection(
            population,
            fitness
        )

        parent2 = roulette_wheel_selection(
            population,
            fitness
        )

    elif method == "tournament":

        parent1 = tournament_selection(
            population,
            fitness
        )

        parent2 = tournament_selection(
            population,
            fitness
        )

    else:

        raise ValueError(
            "Unknown selection method."
        )

    return parent1.copy(), parent2.copy()


# ==========================================================
# CROSSOVER
# ==========================================================

def single_point_crossover(
    parent1,
    parent2
):
    """
    Perform single-point crossover.
    """

    point = random.randint(
        1,
        len(parent1) - 1
    )

    child1 = np.concatenate([

        parent1[:point],

        parent2[point:]

    ])

    child2 = np.concatenate([

        parent2[:point],

        parent1[point:]

    ])

    return child1, child2


# ==========================================================
# MUTATION
# ==========================================================

def mutate(
    chromosome,
    mutation_rate=0.002,
    gene_values=(0, 1, 2, 3)
):
    """
    Random mutation.
    """

    for i in range(len(chromosome)):

        if random.random() < mutation_rate:

            chromosome[i] = random.choice(
                gene_values
            )

    return chromosome


# ==========================================================
# NEXT GENERATION
# ==========================================================

def create_next_generation(
    population,
    fitness,
    mutation_rate=0.002,
    selection_method="roulette"
):
    """
    Create one new generation.
    """

    new_population = []

    while len(new_population) < len(population):

        parent1, parent2 = select_parents(
            population,
            fitness,
            selection_method
        )

        child1, child2 = single_point_crossover(
            parent1,
            parent2
        )

        child1 = mutate(
            child1,
            mutation_rate
        )

        child2 = mutate(
            child2,
            mutation_rate
        )

        new_population.append(child1)

        if len(new_population) < len(population):

            new_population.append(child2)

    return np.array(new_population)


# ==========================================================
# MAIN GENETIC ALGORITHM
# ==========================================================

def genetic_algorithm(
    room,
    generations=200,
    population_size=50,
    chromosome_length=54,
    mutation_rate=0.002,
    selection_method="roulette",
    runs_per_chromosome=5
):
    """
    Run the complete Genetic Algorithm.

    Parameters
    ----------
    room : ndarray

    generations : int

    population_size : int

    chromosome_length : int

    mutation_rate : float

    selection_method : str

    runs_per_chromosome : int

    Returns
    -------
    best_chromosome

    best_fitness

    fitness_history
    """

    population = create_population(
        population_size,
        chromosome_length
    )

    fitness_history = []

    best_chromosome = None

    best_fitness = -np.inf

    for generation in range(generations):

        fitness = evaluate_population(
            population,
            room,
            runs=runs_per_chromosome
        )

        average_fitness = np.mean(fitness)

        fitness_history.append(
            average_fitness
        )

        best_index = np.argmax(fitness)

        if fitness[best_index] > best_fitness:

            best_fitness = fitness[best_index]

            best_chromosome = population[
                best_index
            ].copy()

        population = create_next_generation(
            population,
            fitness,
            mutation_rate,
            selection_method
        )

    return (
        best_chromosome,
        best_fitness,
        fitness_history
    )


# ==========================================================
# TESTING
# ==========================================================

if __name__ == "__main__":

    from environment import create_empty_room

    room = create_empty_room()

    best, score, history = genetic_algorithm(
        room=room,
        generations=20,
        population_size=20,
        runs_per_chromosome=3
    )

    print("=" * 45)
    print("Genetic Algorithm Test")
    print("=" * 45)

    print("Best Fitness :", round(score, 3))
    print("History Length :", len(history))
    print("Chromosome Length :", len(best))