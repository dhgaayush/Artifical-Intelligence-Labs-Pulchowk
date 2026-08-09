"""
main.py

Entry point for the AI Genetic Painter Robot project.
"""

from environment import (
    create_empty_room,
    # create_furnished_room
)

from genetic_algorithm import genetic_algorithm

from visualisation import (
    plot_fitness_history,
    display_best_solution,
    print_ga_summary
)


# ==========================================================
# SETTINGS
# ==========================================================

ROOM_TYPE = "empty"          # "empty" or "furnished"

# GENERATIONS = 200
# POPULATION_SIZE = 50
# MUTATION_RATE = 0.002

GENERATIONS = 5
POPULATION_SIZE = 10
RUNS_PER_CHROMOSOME = 1

SELECTION_METHOD = "roulette"

RUNS_PER_CHROMOSOME = 5

MUTATION_RATE = 0.002


# ==========================================================
# MAIN
# ==========================================================

def main():

    # ------------------------------------------------------
    # Create environment
    # ------------------------------------------------------

    if ROOM_TYPE.lower() == "empty":
        room = create_empty_room()

    # elif ROOM_TYPE.lower() == "furnished":
    #     room = create_furnished_room()

    else:
        raise ValueError("Unknown room type.")

    # ------------------------------------------------------
    # Run Genetic Algorithm
    # ------------------------------------------------------

    best_chromosome, best_fitness, fitness_history = genetic_algorithm(
        room=room,
        generations=GENERATIONS,
        population_size=POPULATION_SIZE,
        mutation_rate=MUTATION_RATE,
        selection_method=SELECTION_METHOD,
        runs_per_chromosome=RUNS_PER_CHROMOSOME
    )

    # ------------------------------------------------------
    # Display Results
    # ------------------------------------------------------

    print_ga_summary(
        best_fitness,
        fitness_history
    )

    plot_fitness_history(
        fitness_history
    )

    display_best_solution(
        best_chromosome,
        room
    )


# ==========================================================
# PROGRAM ENTRY
# ==========================================================

if __name__ == "__main__":

    main()