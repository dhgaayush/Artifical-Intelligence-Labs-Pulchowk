import csv
import json
import importlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


simulation = importlib.import_module("06_simulation")
fitness_module = importlib.import_module("07_fitness")


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def load_history(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_chromosome(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def plot_fitness(history, path):
    generations = [int(row["generation"]) for row in history]
    average = [float(row["average"]) for row in history]
    best = [float(row["best"]) for row in history]
    worst = [float(row["worst"]) for row in history]

    figure, axis = plt.subplots(figsize=(10, 5.5))
    axis.plot(generations, best, label="Best", linewidth=2)
    axis.plot(generations, average, label="Average", linewidth=2)
    axis.plot(generations, worst, label="Worst", linewidth=1.5)
    axis.set_title("Painter-robot fitness over generations")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Efficiency")
    axis.set_ylim(0, 1.05)
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def plot_trajectory(room, trajectory, start, final_position, efficiency, path):
    figure, axis = plt.subplots(figsize=(10, 5.5))
    axis.imshow(room, cmap="Greys", vmin=0, vmax=2)

    columns = [position[1] for position in trajectory]
    rows = [position[0] for position in trajectory]
    axis.plot(columns, rows, color="tab:blue", linewidth=0.8, alpha=0.75)
    axis.scatter(start[1], start[0], color="tab:green", s=55, label="Start", zorder=3)
    axis.scatter(
        final_position[1],
        final_position[0],
        color="tab:red",
        s=55,
        label="End",
        zorder=3,
    )
    axis.set_title(f"Best trajectory ({efficiency:.2%} coverage)")
    axis.set_xlabel("Column")
    axis.set_ylabel("Row")
    axis.set_xlim(-0.5, simulation.COLS - 0.5)
    axis.set_ylim(simulation.ROWS - 0.5, -0.5)
    axis.set_xticks(range(0, simulation.COLS, 5))
    axis.set_yticks(range(0, simulation.ROWS, 5))
    axis.grid(alpha=0.2)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


if __name__ == "__main__":
    history = load_history(OUTPUT_DIR / "fitness_history.csv")
    chromosome = load_chromosome(OUTPUT_DIR / "best_chromosome.json")
    plot_fitness(history, OUTPUT_DIR / "fitness_curve.png")

    starts = fitness_module.make_starts(seed=21, count=3)
    episodes = [
        simulation.simulate(chromosome, row, col, direction, seed=100 + number)
        for number, (row, col, direction) in enumerate(starts)
    ]
    best_episode = max(episodes, key=lambda episode: episode["efficiency"])
    plot_trajectory(
        simulation.make_room(),
        best_episode["trajectory"],
        best_episode["trajectory"][0],
        best_episode["final_position"],
        best_episode["efficiency"],
        OUTPUT_DIR / "best_trajectory.png",
    )

    print("Fitness plot saved to:", OUTPUT_DIR / "fitness_curve.png")
    print("Trajectory plot saved to:", OUTPUT_DIR / "best_trajectory.png")
    print("Best plotted efficiency:", f'{best_episode["efficiency"]:.2%}')
