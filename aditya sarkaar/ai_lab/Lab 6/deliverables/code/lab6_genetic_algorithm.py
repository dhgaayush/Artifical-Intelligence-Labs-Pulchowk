"""Genetic algorithm assignment for the painter-robot problem.

The lab sheet describes a chromosome with 54 rules.  A rule is indexed by
the state [current, forward, left, right], where current is 0 (unpainted) or
2 (painted) and the other three cells are 0 (empty), 1 (wall/furniture), or
2 (painted).  The action stored in a gene is:

    0: no turn      1: turn left      2: turn right      3: random left/right

This file runs both required experiments:

1. evolve a population in a 20x40 empty room;
2. reuse the empty-room champion in a furnished room, then evolve a new
   population for the furnished room from the beginning.

All experiments are deterministic for the supplied seed.  Outputs are saved
under results/ unless another directory is supplied with --output.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


EMPTY = 0
WALL = 1
PAINTED = 2
ROWS = 20
COLS = 40
CHROMOSOME_LENGTH = 54
POPULATION_SIZE = 50
GENERATIONS = 200
MUTATION_RATE = 0.002
ELITE_COUNT = 2
TOURNAMENT_SIZE = 3
# Three fixed starts are enough to make fitness depend on general behaviour
# rather than one lucky starting point, while keeping the required 200 x 50
# experiment practical on a student laptop.
TRAINING_EPISODES = 3
VALIDATION_EPISODES = 8
MAX_STEPS_FACTOR = 3

# Directions are clockwise: north, east, south, west.
DR = (-1, 0, 1, 0)
DC = (0, 1, 0, -1)


@dataclass
class EpisodeResult:
    efficiency: float
    painted: int
    paintable: int
    steps: int
    trajectory: list[tuple[int, int]]
    start: tuple[int, int]
    start_direction: int
    final_position: tuple[int, int]


@dataclass
class EvolutionResult:
    best_chromosome: np.ndarray
    final_population: np.ndarray
    history: list[dict[str, float]]
    training_starts: list[tuple[tuple[int, int], int]]


def make_empty_room() -> np.ndarray:
    """Return the required 20x40 empty room."""

    return np.zeros((ROWS, COLS), dtype=np.int8)


def make_furnished_room() -> np.ndarray:
    """Return a 20x40 room with exactly 100 furniture cells.

    Cells represent square metres, so the four rectangular pieces of
    furniture occupy 32 + 32 + 24 + 12 = 100 square metres.
    """

    room = make_empty_room()
    furniture = [
        (slice(2, 6), slice(5, 13)),      # 32 cells
        (slice(9, 13), slice(20, 28)),    # 32 cells
        (slice(5, 9), slice(31, 37)),     # 24 cells
        (slice(14, 16), slice(12, 18)),   # 12 cells
    ]
    for row_slice, col_slice in furniture:
        room[row_slice, col_slice] = WALL
    assert int(np.count_nonzero(room == WALL)) == 100
    return room


def paintable_cells(room: np.ndarray) -> int:
    return int(np.count_nonzero(room == EMPTY))


def in_room(room: np.ndarray, row: int, col: int) -> bool:
    return 0 <= row < room.shape[0] and 0 <= col < room.shape[1]


def sensed_value(room: np.ndarray, row: int, col: int) -> int:
    """Read one cell, treating positions outside the room as walls."""

    if not in_room(room, row, col):
        return WALL
    return int(room[row, col])


def state_index(room: np.ndarray, row: int, col: int, direction: int) -> int:
    """Encode [current, forward, left, right] into an integer in [0, 53]."""

    current = sensed_value(room, row, col)
    forward = sensed_value(room, row + DR[direction], col + DC[direction])
    left_direction = (direction - 1) % 4
    right_direction = (direction + 1) % 4
    left = sensed_value(room, row + DR[left_direction], col + DC[left_direction])
    right = sensed_value(room, row + DR[right_direction], col + DC[right_direction])

    # Current can only be 0 or 2 for a valid painter position.  Map these to
    # the two current-square values in the chromosome's 2 x 3 x 3 x 3 state
    # space.  The other values use their natural 0, 1, 2 indices.
    current_index = 0 if current == EMPTY else 1
    return (((current_index * 3 + forward) * 3 + left) * 3 + right)


def make_starts(room: np.ndarray, count: int, seed: int) -> list[tuple[tuple[int, int], int]]:
    """Create reproducible random start positions and directions."""

    rng = np.random.default_rng(seed)
    coordinates = np.argwhere(room == EMPTY)
    chosen = rng.integers(0, len(coordinates), size=count)
    directions = rng.integers(0, 4, size=count)
    return [
        ((int(coordinates[i, 0]), int(coordinates[i, 1])), int(direction))
        for i, direction in zip(chosen, directions)
    ]


def simulate(
    chromosome: Sequence[int],
    base_room: np.ndarray,
    start: tuple[int, int],
    start_direction: int,
    random_seed: int,
    max_steps: int | None = None,
) -> EpisodeResult:
    """Simulate one chromosome and return coverage plus its trajectory.

    The painter observes the state before each action, applies the rule,
    paints its current square if it is unpainted, and attempts to move one
    square forward.  A step limit prevents a chromosome that loops forever
    from making the GA unevaluable; the limit is three passes over the room.
    """

    room = np.array(base_room, copy=True)
    total_paintable = paintable_cells(room)
    if room[start] != EMPTY:
        raise ValueError(f"Start position {start} is not paintable")
    if max_steps is None:
        max_steps = MAX_STEPS_FACTOR * total_paintable

    rng = random.Random(random_seed)
    row, col = start
    direction = int(start_direction) % 4
    remaining = total_paintable
    trajectory: list[tuple[int, int]] = []

    for step in range(max_steps + 1):
        trajectory.append((row, col))
        action = int(chromosome[state_index(room, row, col, direction)])

        if action == 1:
            direction = (direction - 1) % 4
        elif action == 2:
            direction = (direction + 1) % 4
        elif action == 3:
            direction = (direction - 1 if rng.random() < 0.5 else direction + 1) % 4

        if room[row, col] == EMPTY:
            room[row, col] = PAINTED
            remaining -= 1
            if remaining == 0:
                return EpisodeResult(
                    efficiency=1.0,
                    painted=total_paintable,
                    paintable=total_paintable,
                    steps=step + 1,
                    trajectory=trajectory,
                    start=start,
                    start_direction=start_direction,
                    final_position=(row, col),
                )

        next_row = row + DR[direction]
        next_col = col + DC[direction]
        if in_room(room, next_row, next_col) and room[next_row, next_col] != WALL:
            row, col = next_row, next_col

    painted = total_paintable - remaining
    return EpisodeResult(
        efficiency=painted / total_paintable,
        painted=painted,
        paintable=total_paintable,
        steps=max_steps + 1,
        trajectory=trajectory,
        start=start,
        start_direction=start_direction,
        final_position=(row, col),
    )


def evaluate_chromosome(
    chromosome: Sequence[int],
    room: np.ndarray,
    starts: Sequence[tuple[tuple[int, int], int]],
    random_seed: int,
) -> tuple[float, list[EpisodeResult]]:
    """Evaluate a chromosome several times and average its efficiency."""

    episodes = [
        simulate(
            chromosome,
            room,
            start,
            direction,
            random_seed=random_seed + 104729 * episode_index,
        )
        for episode_index, (start, direction) in enumerate(starts)
    ]
    return float(np.mean([episode.efficiency for episode in episodes])), episodes


def tournament_pick(population: np.ndarray, fitness: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    indices = rng.integers(0, len(population), size=TOURNAMENT_SIZE)
    winner = indices[int(np.argmax(fitness[indices]))]
    return population[winner]


def evolve(
    room: np.ndarray,
    seed: int,
    generations: int = GENERATIONS,
    population_size: int = POPULATION_SIZE,
    episodes: int = TRAINING_EPISODES,
) -> EvolutionResult:
    """Run tournament-selection GA with single-point crossover and mutation."""

    rng = np.random.default_rng(seed)
    population = rng.integers(
        0, 4, size=(population_size, CHROMOSOME_LENGTH), dtype=np.int8
    )
    starts = make_starts(room, episodes, seed + 11)
    history: list[dict[str, float]] = []
    best_chromosome = population[0].copy()
    best_fitness = -1.0

    for generation in range(generations + 1):
        fitness = np.array(
            [
                evaluate_chromosome(
                    chromosome,
                    room,
                    starts,
                    random_seed=seed + 5003 * generation + index,
                )[0]
                for index, chromosome in enumerate(population)
            ],
            dtype=float,
        )
        order = np.argsort(fitness)[::-1]
        generation_best = float(fitness[order[0]])
        if generation_best > best_fitness:
            best_fitness = generation_best
            best_chromosome = population[order[0]].copy()
        history.append(
            {
                "generation": float(generation),
                "average": float(np.mean(fitness)),
                "median": float(np.median(fitness)),
                "best": generation_best,
            }
        )

        if generation == generations:
            final_population = population.copy()
            break

        next_population = [population[index].copy() for index in order[:ELITE_COUNT]]
        while len(next_population) < population_size:
            parent_a = tournament_pick(population, fitness, rng)
            parent_b = tournament_pick(population, fitness, rng)
            crossover_point = int(rng.integers(1, CHROMOSOME_LENGTH))
            child_a = np.concatenate((parent_a[:crossover_point], parent_b[crossover_point:])).copy()
            child_b = np.concatenate((parent_b[:crossover_point], parent_a[crossover_point:])).copy()

            for child in (child_a, child_b):
                mutation_mask = rng.random(CHROMOSOME_LENGTH) < MUTATION_RATE
                if np.any(mutation_mask):
                    child[mutation_mask] = rng.integers(0, 4, size=int(np.count_nonzero(mutation_mask)))
                next_population.append(child)
                if len(next_population) == population_size:
                    break
        population = np.asarray(next_population, dtype=np.int8)

    return EvolutionResult(
        best_chromosome=best_chromosome,
        final_population=final_population,
        history=history,
        training_starts=starts,
    )


def save_history_csv(history: Sequence[dict[str, float]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["generation", "average", "median", "best"])
        writer.writeheader()
        writer.writerows(history)


def plot_population(population: np.ndarray, title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 6.2))
    image = ax.imshow(population, aspect="auto", interpolation="nearest", cmap="viridis", vmin=0, vmax=3)
    ax.set_title(title)
    ax.set_xlabel("Gene / encoded state (0-53)")
    ax.set_ylabel("Chromosome in final population")
    ax.set_xticks(np.arange(0, CHROMOSOME_LENGTH, 3))
    fig.colorbar(image, ax=ax, ticks=[0, 1, 2, 3], label="Action (0 none, 1 left, 2 right, 3 random)")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_fitness(history: Sequence[dict[str, float]], title: str, path: Path) -> None:
    generations = [row["generation"] for row in history]
    averages = [row["average"] for row in history]
    medians = [row["median"] for row in history]
    best = [row["best"] for row in history]

    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    ax.plot(generations, averages, label="population average", linewidth=1.8)
    ax.plot(generations, medians, label="population median", linewidth=1.3, alpha=0.8)
    ax.plot(generations, best, label="generation best", linewidth=2.0)
    ax.set_title(title)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Efficiency (fraction of paintable cells)")
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_room(room: np.ndarray, title: str, path: Path) -> None:
    cmap = ListedColormap(["white", "#30343b"])
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.imshow(room != WALL, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_title(title)
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_xticks(np.arange(-0.5, COLS, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, ROWS, 1), minor=True)
    ax.grid(which="minor", color="#d9d9d9", linewidth=0.25)
    ax.tick_params(which="minor", bottom=False, left=False)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_trajectory(room: np.ndarray, episode: EpisodeResult, title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2))
    background = np.where(room == WALL, 0.0, 1.0)
    ax.imshow(background, cmap=ListedColormap(["#30343b", "white"]), vmin=0, vmax=1, interpolation="nearest")
    points = np.asarray(episode.trajectory)
    if len(points) > 1:
        colours = np.linspace(0, 1, len(points))
        ax.plot(points[:, 1], points[:, 0], color="#cf3f3f", linewidth=0.8, alpha=0.55, zorder=2)
        ax.scatter(points[:, 1], points[:, 0], c=colours, cmap="plasma", s=2.5, alpha=0.6, zorder=3)
    ax.scatter([episode.start[1]], [episode.start[0]], marker="o", s=55, color="#1677c8", label="start", zorder=5)
    ax.scatter([episode.final_position[1]], [episode.final_position[0]], marker="X", s=65, color="#1b8a45", label="end", zorder=5)
    ax.set_title(f"{title}\nEfficiency: {episode.efficiency:.1%}; {episode.painted}/{episode.paintable} cells; {episode.steps} steps")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_xticks(np.arange(-0.5, COLS, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, ROWS, 1), minor=True)
    ax.grid(which="minor", color="#d9d9d9", linewidth=0.25)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def summarize_evaluation(
    chromosome: np.ndarray,
    room: np.ndarray,
    starts: Sequence[tuple[tuple[int, int], int]],
    seed: int,
) -> tuple[dict[str, float], list[EpisodeResult]]:
    mean, episodes = evaluate_chromosome(chromosome, room, starts, seed)
    efficiencies = np.array([episode.efficiency for episode in episodes])
    summary = {
        "mean_efficiency": float(mean),
        "min_efficiency": float(np.min(efficiencies)),
        "max_efficiency": float(np.max(efficiencies)),
        "paintable_cells": float(episodes[0].paintable),
        "mean_steps": float(np.mean([episode.steps for episode in episodes])),
    }
    return summary, episodes


def run_evolution_experiment(
    room: np.ndarray,
    label: str,
    seed: int,
    output_dir: Path,
) -> tuple[EvolutionResult, dict[str, float], list[EpisodeResult]]:
    result = evolve(room, seed=seed)
    prefix = output_dir / label
    plot_population(result.final_population, f"Final chromosome population: {label}", prefix.with_name(prefix.name + "_final_population.png"))
    plot_fitness(result.history, f"Fitness over generations: {label}", prefix.with_name(prefix.name + "_fitness.png"))
    save_history_csv(result.history, prefix.with_name(prefix.name + "_fitness.csv"))

    validation_starts = make_starts(room, VALIDATION_EPISODES, seed + 991)
    summary, episodes = summarize_evaluation(result.best_chromosome, room, validation_starts, seed + 2003)
    best_episode = max(episodes, key=lambda episode: episode.efficiency)
    plot_trajectory(
        room,
        best_episode,
        f"Best {label} chromosome on its most successful validation run",
        prefix.with_name(prefix.name + "_best_trajectory.png"),
    )
    return result, summary, episodes


def chromosome_as_list(chromosome: np.ndarray) -> list[int]:
    return [int(value) for value in chromosome.tolist()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    default_output = Path(__file__).resolve().parent.parent / "outputs"
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    empty_room = make_empty_room()
    furnished_room = make_furnished_room()
    plot_room(empty_room, "20 x 40 empty room", args.output / "empty_room.png")
    plot_room(furnished_room, "20 x 40 room with 100 square metres of furniture", args.output / "furnished_room.png")

    empty_result, empty_summary, _ = run_evolution_experiment(
        empty_room, "empty", args.seed, args.output
    )

    # Assignment 4: directly transfer the empty-room champion to the new room.
    furnished_starts = make_starts(furnished_room, VALIDATION_EPISODES, args.seed + 3001)
    reused_summary, reused_episodes = summarize_evaluation(
        empty_result.best_chromosome,
        furnished_room,
        furnished_starts,
        args.seed + 4001,
    )
    reused_episode = max(reused_episodes, key=lambda episode: episode.efficiency)
    plot_trajectory(
        furnished_room,
        reused_episode,
        "Empty-room champion reused in furnished room (best validation run)",
        args.output / "furnished_reuse_trajectory.png",
    )
    reused_worst_episode = min(reused_episodes, key=lambda episode: episode.efficiency)
    plot_trajectory(
        furnished_room,
        reused_worst_episode,
        "Empty-room champion reused in furnished room (worst validation run)",
        args.output / "furnished_reuse_worst_trajectory.png",
    )

    furnished_result, furnished_summary, _ = run_evolution_experiment(
        furnished_room, "furnished", args.seed + 5000, args.output
    )

    # Paired comparison: both champions face exactly the same furnished-room
    # starts, making the transfer cost easier to interpret than two unrelated
    # validation samples.
    paired_starts = make_starts(furnished_room, VALIDATION_EPISODES, args.seed + 5000 + 991)
    paired_reuse_summary, _ = summarize_evaluation(
        empty_result.best_chromosome,
        furnished_room,
        paired_starts,
        args.seed + 5000 + 2003,
    )
    paired_furnished_summary, _ = summarize_evaluation(
        furnished_result.best_chromosome,
        furnished_room,
        paired_starts,
        args.seed + 5000 + 2003,
    )

    summary = {
        "configuration": {
            "room_shape": [ROWS, COLS],
            "population_size": POPULATION_SIZE,
            "chromosome_length": CHROMOSOME_LENGTH,
            "generations": GENERATIONS,
            "training_episodes_per_chromosome": TRAINING_EPISODES,
            "validation_episodes": VALIDATION_EPISODES,
            "mutation_rate": MUTATION_RATE,
            "max_steps_factor": MAX_STEPS_FACTOR,
            "selection": "tournament selection, size 3, with 2 elite chromosomes",
            "crossover": "single-point crossover",
            "seed": args.seed,
        },
        "empty_room": empty_summary,
        "empty_champion_on_furnished_room": reused_summary,
        "furnished_room_evolved_from_start": furnished_summary,
        "paired_furnished_comparison": {
            "shared_validation_starts": VALIDATION_EPISODES,
            "empty_champion": paired_reuse_summary,
            "furnished_champion": paired_furnished_summary,
        },
        "chromosomes": {
            "empty_best": chromosome_as_list(empty_result.best_chromosome),
            "furnished_best": chromosome_as_list(furnished_result.best_chromosome),
        },
    }
    with (args.output / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
