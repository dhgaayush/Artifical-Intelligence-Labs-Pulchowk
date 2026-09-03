"""Second, independent implementation of the Lab 6 painter experiment.

This version keeps the lab-sheet interface idea but uses a different internal
design from the first run: state tuples are mapped through a lookup table,
parents are chosen with rank-weighted sampling, children use two crossover
cuts, and mutation replaces a chosen action with a different action.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np


HEIGHT, WIDTH = 20, 40
GENE_COUNT = 54
POPULATION = 50
GENERATIONS = 200
TRAINING_RUNS = 3
VALIDATION_RUNS = 8
MUTATION_RATE = 0.0025
ELITES = 3
STEP_MULTIPLIER = 3

EMPTY, FURNITURE, PAINTED = 0, 1, 2
MOVES = ((-1, 0), (0, 1), (1, 0), (0, -1))

# The order is [current, forward, left, right].  The current cell has only
# two legal values; the other readings have three.
STATE_INDEX = {
    state: number
    for number, state in enumerate(product((0, 2), (0, 1, 2), (0, 1, 2), (0, 1, 2)))
}

PALETTE = {
    "ink": "#101820",
    "paper": "#f4efe6",
    "teal": "#2ec4b6",
    "coral": "#ff6b6b",
    "gold": "#ffd166",
    "violet": "#9b5de5",
    "muted": "#9fb3c8",
}


@dataclass
class Walk:
    efficiency: float
    covered: int
    paintable: int
    steps: int
    path: list[tuple[int, int]]
    start: tuple[int, int]
    direction: int


@dataclass
class Evolution:
    champion: np.ndarray
    final_population: np.ndarray
    history: list[dict[str, float]]


def empty_room() -> np.ndarray:
    return np.zeros((HEIGHT, WIDTH), dtype=np.int8)


def furnished_room() -> np.ndarray:
    """A new 100-cell furniture arrangement for the second run."""

    room = empty_room()
    blocks = (
        (slice(2, 5), slice(3, 15)),    # 36 cells
        (slice(8, 12), slice(26, 35)),  # 36 cells
        (slice(14, 18), slice(17, 24)), # 28 cells
    )
    for rows, columns in blocks:
        room[rows, columns] = FURNITURE
    assert int(np.count_nonzero(room == FURNITURE)) == 100
    return room


def paintable_count(room: np.ndarray) -> int:
    return int(np.count_nonzero(room == EMPTY))


def cell(room: np.ndarray, row: int, column: int) -> int:
    if row < 0 or row >= HEIGHT or column < 0 or column >= WIDTH:
        return FURNITURE
    return int(room[row, column])


def state_number(room: np.ndarray, row: int, column: int, facing: int) -> int:
    left = (facing - 1) % 4
    right = (facing + 1) % 4
    readings = (
        cell(room, row, column),
        cell(room, row + MOVES[facing][0], column + MOVES[facing][1]),
        cell(room, row + MOVES[left][0], column + MOVES[left][1]),
        cell(room, row + MOVES[right][0], column + MOVES[right][1]),
    )
    return STATE_INDEX[readings]


def random_starts(room: np.ndarray, count: int, seed: int) -> list[tuple[tuple[int, int], int]]:
    rng = np.random.default_rng(seed)
    cells = np.argwhere(room == EMPTY)
    picks = rng.integers(0, len(cells), count)
    headings = rng.integers(0, 4, count)
    return [
        ((int(cells[pick, 0]), int(cells[pick, 1])), int(heading))
        for pick, heading in zip(picks, headings)
    ]


def walk(
    chromosome: Sequence[int],
    room: np.ndarray,
    start: tuple[int, int],
    direction: int,
    seed: int,
) -> Walk:
    """Run one policy until the paint is gone or the safety horizon expires."""

    floor = room.copy()
    total = paintable_count(floor)
    remaining = total
    row, column = start
    facing = direction % 4
    randomizer = random.Random(seed)
    route: list[tuple[int, int]] = []
    horizon = STEP_MULTIPLIER * total

    for step in range(horizon + 1):
        route.append((row, column))
        action = int(chromosome[state_number(floor, row, column, facing)])

        if action == 1:
            facing = (facing - 1) % 4
        elif action == 2:
            facing = (facing + 1) % 4
        elif action == 3:
            facing = (facing - 1 if randomizer.random() < 0.5 else facing + 1) % 4

        if floor[row, column] == EMPTY:
            floor[row, column] = PAINTED
            remaining -= 1
            if remaining == 0:
                return Walk(1.0, total, total, step + 1, route, start, direction)

        next_row = row + MOVES[facing][0]
        next_column = column + MOVES[facing][1]
        if 0 <= next_row < HEIGHT and 0 <= next_column < WIDTH:
            if floor[next_row, next_column] != FURNITURE:
                row, column = next_row, next_column

    covered = total - remaining
    return Walk(covered / total, covered, total, horizon + 1, route, start, direction)


def score(
    chromosome: Sequence[int],
    room: np.ndarray,
    starts: Sequence[tuple[tuple[int, int], int]],
    seed: int,
) -> tuple[float, list[Walk]]:
    trials = [
        walk(chromosome, room, start, direction, seed + 7919 * number)
        for number, (start, direction) in enumerate(starts)
    ]
    return float(np.mean([trial.efficiency for trial in trials])), trials


def rank_parent(population: np.ndarray, fitness: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    order = np.argsort(fitness)
    weights = np.arange(1, len(population) + 1, dtype=float)
    chosen_position = int(rng.choice(len(population), p=weights / weights.sum()))
    return population[order[chosen_position]]


def two_cut_children(
    first: np.ndarray, second: np.ndarray, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    cuts = np.sort(rng.choice(np.arange(1, GENE_COUNT), size=2, replace=False))
    left, right = int(cuts[0]), int(cuts[1])
    child_one = first.copy()
    child_two = second.copy()
    child_one[left:right] = second[left:right]
    child_two[left:right] = first[left:right]
    return child_one, child_two


def mutate(chromosome: np.ndarray, rng: np.random.Generator) -> None:
    for index in np.flatnonzero(rng.random(GENE_COUNT) < MUTATION_RATE):
        chromosome[index] = (int(chromosome[index]) + int(rng.integers(1, 4))) % 4


def evolve(room: np.ndarray, seed: int) -> Evolution:
    rng = np.random.default_rng(seed)
    population = rng.integers(0, 4, size=(POPULATION, GENE_COUNT), dtype=np.int8)
    starts = random_starts(room, TRAINING_RUNS, seed + 101)
    champion = population[0].copy()
    champion_score = -1.0
    history: list[dict[str, float]] = []

    for generation in range(GENERATIONS + 1):
        fitness = np.array(
            [score(individual, room, starts, seed + generation * 1009 + i)[0]
             for i, individual in enumerate(population)]
        )
        ranking = np.argsort(fitness)[::-1]
        if float(fitness[ranking[0]]) > champion_score:
            champion_score = float(fitness[ranking[0]])
            champion = population[ranking[0]].copy()
        history.append({
            "generation": generation,
            "average": float(np.mean(fitness)),
            "best": float(np.max(fitness)),
            "p90": float(np.percentile(fitness, 90)),
        })

        if generation == GENERATIONS:
            final_population = population.copy()
            break

        next_population = [population[index].copy() for index in ranking[:ELITES]]
        while len(next_population) < POPULATION:
            parent_a = rank_parent(population, fitness, rng)
            parent_b = rank_parent(population, fitness, rng)
            child_a, child_b = two_cut_children(parent_a, parent_b, rng)
            mutate(child_a, rng)
            mutate(child_b, rng)
            next_population.extend((child_a, child_b))
        population = np.asarray(next_population[:POPULATION], dtype=np.int8)

    return Evolution(champion, final_population, history)


def dark_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(PALETTE["ink"])
    ax.tick_params(colors=PALETTE["muted"])
    for spine in ax.spines.values():
        spine.set_color(PALETTE["muted"])
    ax.xaxis.label.set_color(PALETTE["muted"])
    ax.yaxis.label.set_color(PALETTE["muted"])
    ax.title.set_color(PALETTE["paper"])


def finish_figure(fig: plt.Figure, path: Path) -> None:
    fig.patch.set_facecolor(PALETTE["ink"])
    fig.tight_layout()
    fig.savefig(path, dpi=190, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_room_pair(empty: np.ndarray, furniture: np.ndarray, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), facecolor=PALETTE["ink"])
    for ax, room, title in zip(axes, (empty, furniture), ("Open floor", "Furniture layout")):
        dark_axes(ax)
        ax.imshow(room == FURNITURE, cmap=ListedColormap([PALETTE["paper"], PALETTE["coral"]]), interpolation="nearest")
        ax.set_title(title)
        ax.set_xlabel("column")
        ax.set_ylabel("row")
        ax.set_xticks(range(0, WIDTH, 5))
        ax.set_yticks(range(0, HEIGHT, 5))
    finish_figure(fig, path)


def plot_history(history: Sequence[dict[str, float]], title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    dark_axes(ax)
    generations = [item["generation"] for item in history]
    ax.plot(generations, [item["average"] for item in history], color=PALETTE["teal"], label="mean", linewidth=2.2)
    ax.plot(generations, [item["p90"] for item in history], color=PALETTE["gold"], label="90th percentile", linewidth=1.5)
    ax.plot(generations, [item["best"] for item in history], color=PALETTE["coral"], label="best", linewidth=2.0)
    ax.set_title(title)
    ax.set_xlabel("generation")
    ax.set_ylabel("covered fraction")
    ax.set_ylim(0, 1.02)
    ax.grid(color="#31404d", alpha=0.65)
    legend = ax.legend(frameon=False)
    for label in legend.get_texts():
        label.set_color(PALETTE["paper"])
    finish_figure(fig, path)


def plot_population(population: np.ndarray, title: str, path: Path) -> None:
    cmap = LinearSegmentedColormap.from_list(
        "midnight_sunset",
        [PALETTE["ink"], "#22577a", PALETTE["teal"], PALETTE["gold"], PALETTE["coral"]],
    )
    fig, ax = plt.subplots(figsize=(12, 5.8))
    dark_axes(ax)
    image = ax.imshow(population, aspect="auto", interpolation="nearest", cmap=cmap, vmin=0, vmax=3)
    ax.set_title(title)
    ax.set_xlabel("state gene")
    ax.set_ylabel("chromosome")
    ax.set_xticks(np.arange(0, GENE_COUNT, 3))
    colorbar = fig.colorbar(image, ax=ax, ticks=[0, 1, 2, 3])
    colorbar.ax.tick_params(colors=PALETTE["muted"])
    colorbar.set_label("action: none / left / right / random", color=PALETTE["muted"])
    finish_figure(fig, path)


def plot_walk(room: np.ndarray, result: Walk, title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5.7))
    dark_axes(ax)
    background = np.where(room == FURNITURE, 1, 0)
    ax.imshow(background, cmap=ListedColormap([PALETTE["paper"], PALETTE["coral"]]), interpolation="nearest")
    coordinates = np.asarray(result.path)
    if len(coordinates) > 1:
        colors = np.linspace(0, 1, len(coordinates))
        ax.plot(coordinates[:, 1], coordinates[:, 0], color=PALETTE["violet"], linewidth=0.7, alpha=0.65)
        ax.scatter(coordinates[:, 1], coordinates[:, 0], c=colors, cmap="viridis", s=3, alpha=0.7)
    ax.scatter(result.start[1], result.start[0], marker="o", s=70, color=PALETTE["teal"], label="start")
    ax.scatter(coordinates[-1, 1], coordinates[-1, 0], marker="X", s=70, color=PALETTE["gold"], label="end")
    ax.set_title(f"{title}  |  coverage {result.efficiency:.1%} ({result.covered}/{result.paintable})")
    ax.set_xlabel("column")
    ax.set_ylabel("row")
    ax.legend(frameon=False, labelcolor=PALETTE["paper"])
    finish_figure(fig, path)


def save_history(history: Sequence[dict[str, float]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("generation", "average", "best", "p90"))
        writer.writeheader()
        writer.writerows(history)


def summarize(chromosome: np.ndarray, room: np.ndarray, starts: Sequence[tuple[tuple[int, int], int]], seed: int) -> tuple[dict[str, float], list[Walk]]:
    mean, trials = score(chromosome, room, starts, seed)
    values = [trial.efficiency for trial in trials]
    return {
        "mean_efficiency": float(mean),
        "best_efficiency": float(max(values)),
        "worst_efficiency": float(min(values)),
        "paintable_cells": int(trials[0].paintable),
        "mean_steps": float(np.mean([trial.steps for trial in trials])),
    }, trials


def run_evolution(room: np.ndarray, name: str, seed: int, output: Path) -> tuple[Evolution, dict[str, float], list[Walk]]:
    result = evolve(room, seed)
    validation = random_starts(room, VALIDATION_RUNS, seed + 202)
    statistics, trials = summarize(result.champion, room, validation, seed + 303)
    save_history(result.history, output / f"{name}_fitness.csv")
    plot_history(result.history, f"{name.title()} room: population trend", output / f"{name}_fitness.png")
    plot_population(result.final_population, f"{name.title()} room: final chromosomes", output / f"{name}_population.png")
    plot_walk(room, max(trials, key=lambda trial: trial.efficiency), f"{name.title()} champion, strongest validation run", output / f"{name}_trajectory_best.png")
    return result, statistics, trials


def main() -> None:
    parser = argparse.ArgumentParser(description="Independent second run of the painter genetic algorithm")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent.parent / "outputs")
    parser.add_argument("--seed", type=int, default=40731)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    open_room = empty_room()
    blocked_room = furnished_room()
    plot_room_pair(open_room, blocked_room, args.output / "room_layouts.png")

    open_run, open_stats, _ = run_evolution(open_room, "empty", args.seed, args.output)

    transfer_starts = random_starts(blocked_room, VALIDATION_RUNS, args.seed + 808)
    transfer_stats, transfer_trials = summarize(open_run.champion, blocked_room, transfer_starts, args.seed + 909)
    plot_walk(blocked_room, max(transfer_trials, key=lambda trial: trial.efficiency), "Transferred empty-room champion, strongest run", args.output / "transfer_best.png")
    plot_walk(blocked_room, min(transfer_trials, key=lambda trial: trial.efficiency), "Transferred empty-room champion, weakest run", args.output / "transfer_weakest.png")

    furnished_run, furnished_stats, _ = run_evolution(blocked_room, "furnished", args.seed + 1000, args.output)

    summary = {
        "variant": "Assignment-Redone",
        "seed": args.seed,
        "population": POPULATION,
        "generations": GENERATIONS,
        "training_runs": TRAINING_RUNS,
        "validation_runs": VALIDATION_RUNS,
        "mutation_rate": MUTATION_RATE,
        "selection": "rank-weighted sampling with three elites",
        "crossover": "two-point crossover",
        "furniture_cells": int(np.count_nonzero(blocked_room == FURNITURE)),
        "empty_room": open_stats,
        "empty_champion_transferred": transfer_stats,
        "furnished_room_evolved": furnished_stats,
        "empty_champion": [int(value) for value in open_run.champion],
        "furnished_champion": [int(value) for value in furnished_run.champion],
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
