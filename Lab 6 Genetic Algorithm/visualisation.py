"""
visualization.py

Visualization utilities for the Genetic Algorithm
Painter Robot project.

This module contains plotting functions only.
No simulation or GA logic belongs here.
"""

import numpy as np
import matplotlib.pyplot as plt

from painter import (
    simulate_painter,
    simulate_multiple_runs
)

# ==========================================================
# COLOUR MAP
# ==========================================================

CELL_COLORS = {
    0: "white",      # Empty
    1: "black",      # Obstacle
    2: "limegreen"   # Painted
}


# ==========================================================
# ROOM VISUALIZATION
# ==========================================================

def plot_room(room, title="Room"):
    """
    Display a room.

    0 -> Empty
    1 -> Obstacle
    2 -> Painted
    """

    cmap = plt.matplotlib.colors.ListedColormap(
        [
            CELL_COLORS[0],
            CELL_COLORS[1],
            CELL_COLORS[2]
        ]
    )

    plt.figure(figsize=(12, 6))

    plt.imshow(
        room,
        cmap=cmap,
        vmin=0,
        vmax=2,
        interpolation="nearest"
    )

    plt.title(title)

    plt.xticks([])
    plt.yticks([])

    plt.grid(False)

    plt.show()


# ==========================================================
# TRAJECTORY
# ==========================================================

def plot_trajectory(
    room,
    trajectory,
    title="Robot Trajectory"
):
    """
    Plot the robot trajectory over the room.
    """

    cmap = plt.matplotlib.colors.ListedColormap(
        [
            CELL_COLORS[0],
            CELL_COLORS[1],
            CELL_COLORS[2]
        ]
    )

    plt.figure(figsize=(12, 6))

    plt.imshow(
        room,
        cmap=cmap,
        vmin=0,
        vmax=2,
        interpolation="nearest"
    )

    if len(trajectory) > 0:

        rows = [p[0] for p in trajectory]
        cols = [p[1] for p in trajectory]

        plt.plot(
            cols,
            rows,
            color="red",
            linewidth=1.5,
            label="Path"
        )

        plt.scatter(
            cols[0],
            rows[0],
            color="blue",
            s=70,
            label="Start"
        )

        plt.scatter(
            cols[-1],
            rows[-1],
            color="yellow",
            edgecolors="black",
            s=80,
            label="End"
        )

    plt.title(title)

    plt.legend()

    plt.xticks([])
    plt.yticks([])

    plt.show()


# ==========================================================
# FITNESS HISTORY
# ==========================================================

def plot_fitness_history(history):
    """
    Plot average fitness versus generation.
    """

    plt.figure(figsize=(10, 5))

    plt.plot(
        history,
        linewidth=2
    )

    plt.xlabel("Generation")

    plt.ylabel("Average Fitness")

    plt.title("Fitness Evolution")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ==========================================================
# BEST SOLUTION
# ==========================================================

def display_best_solution(
    chromosome,
    room,
    runs=20
):
    """
    Display a representative run of the best chromosome.

    The Genetic Algorithm evaluates chromosomes using the
    average efficiency over several random runs.

    Therefore, instead of displaying one completely random run,
    this function performs multiple simulations and displays the
    run whose efficiency is closest to the average efficiency.
    """

    multi_result = simulate_multiple_runs(
        chromosome,
        room,
        runs
    )

    average_efficiency = multi_result["average_efficiency"]

    # Choose the run closest to the average efficiency
    representative_result = min(
        multi_result["results"],
        key=lambda r: abs(
            r["efficiency"] - average_efficiency
        )
    )

    print("=" * 45)
    print("Best Solution")
    print("=" * 45)

    print(
        f"Average Efficiency ({runs} runs): "
        f"{average_efficiency:.3f}"
    )

    print(
        f"Displayed Run Efficiency       : "
        f"{representative_result['efficiency']:.3f}"
    )

    print(
        f"Steps                          : "
        f"{len(representative_result['trajectory'])}"
    )

    plot_room(
        representative_result["painted_room"],
        title="Representative Painted Room"
    )

    plot_trajectory(
        representative_result["painted_room"],
        representative_result["trajectory"],
        title="Representative Robot Trajectory"
    )

    return representative_result


# ==========================================================
# FITNESS COMPARISON
# ==========================================================

def compare_histories(
    histories,
    labels
):
    """
    Compare multiple GA runs.

    Parameters
    ----------
    histories : list

    labels : list
    """

    plt.figure(figsize=(10, 5))

    for history, label in zip(
        histories,
        labels
    ):

        plt.plot(
            history,
            linewidth=2,
            label=label
        )

    plt.xlabel("Generation")

    plt.ylabel("Average Fitness")

    plt.title("Fitness Comparison")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ==========================================================
# SUMMARY
# ==========================================================

def print_ga_summary(
    best_fitness,
    history
):
    """
    Print GA summary.
    """

    print("=" * 45)

    print("Genetic Algorithm Summary")

    print("=" * 45)

    print(f"Generations      : {len(history)}")
    print(f"Final Fitness    : {best_fitness:.3f}")
    print(f"Best Average     : {max(history):.3f}")
    print(f"Initial Average  : {history[0]:.3f}")
    print(f"Final Average    : {history[-1]:.3f}")

    print("=" * 45)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    from environment import create_empty_room
    from painter import generate_random_chromosome

    room = create_empty_room()

    chromosome = generate_random_chromosome()

    result = simulate_painter(
        chromosome,
        room
    )

    plot_room(
        result["painted_room"],
        "Painted Room"
    )

    plot_trajectory(
        result["painted_room"],
        result["trajectory"]
    )

    plot_fitness_history(
        np.random.rand(25)
    )

    display_best_solution(
        chromosome,
        room,
        runs=10
    )