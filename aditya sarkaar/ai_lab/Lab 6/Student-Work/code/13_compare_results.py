import importlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


furnished = importlib.import_module("11_furnished_room")


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def load_chromosome(filename):
    with (OUTPUT_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def summarize(episodes):
    efficiencies = [episode["efficiency"] for episode in episodes]
    return {
        "mean": sum(efficiencies) / len(efficiencies),
        "best": max(efficiencies),
        "worst": min(efficiencies),
        "paintable_cells": episodes[0]["paintable_cells"],
        "mean_steps": sum(episode["steps"] for episode in episodes) / len(episodes),
    }


def plot_comparison(summary, path):
    labels = ["Transferred\nempty champion", "Evolved\nfurnished champion"]
    means = [
        summary["transferred_empty_champion"]["mean"],
        summary["furnished_champion"]["mean"],
    ]
    best = [
        summary["transferred_empty_champion"]["best"],
        summary["furnished_champion"]["best"],
    ]
    worst = [
        summary["transferred_empty_champion"]["worst"],
        summary["furnished_champion"]["worst"],
    ]

    positions = range(len(labels))
    width = 0.24
    figure, axis = plt.subplots(figsize=(8, 5.5))
    axis.bar([position - width for position in positions], means, width, label="Mean")
    axis.bar(positions, best, width, label="Best")
    axis.bar([position + width for position in positions], worst, width, label="Worst")
    axis.set_title("Furnished-room champion comparison")
    axis.set_ylabel("Efficiency")
    axis.set_ylim(0, 1.05)
    axis.set_xticks(list(positions), labels)
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


if __name__ == "__main__":
    room = furnished.make_furnished_room()
    starts = furnished.make_starts(room, seed=81, count=furnished.VALIDATION_RUNS)
    empty_champion = load_chromosome("best_chromosome.json")
    furnished_champion = load_chromosome("furnished_best_chromosome.json")

    transferred_episodes = furnished.evaluate(empty_champion, room, starts)
    furnished_episodes = furnished.evaluate(furnished_champion, room, starts)
    summary = {
        "room": {
            "rows": furnished.simulation.ROWS,
            "columns": furnished.simulation.COLS,
            "obstacle_cells": sum(
                cell == furnished.simulation.OBSTACLE
                for row in room
                for cell in row
            ),
            "paintable_cells": sum(
                cell == furnished.simulation.EMPTY
                for row in room
                for cell in row
            ),
        },
        "shared_validation_starts": len(starts),
        "transferred_empty_champion": summarize(transferred_episodes),
        "furnished_champion": summarize(furnished_episodes),
    }

    summary_path = OUTPUT_DIR / "comparison_summary.json"
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    chart_path = OUTPUT_DIR / "champion_comparison.png"
    plot_comparison(summary, chart_path)

    transferred = summary["transferred_empty_champion"]
    evolved = summary["furnished_champion"]
    print("Shared validation starts:", len(starts))
    print("Transferred mean efficiency:", f'{transferred["mean"]:.2%}')
    print("Furnished champion mean efficiency:", f'{evolved["mean"]:.2%}')
    print("Mean improvement:", f'{(evolved["mean"] - transferred["mean"]):.2%}')
    print("Summary saved to:", summary_path)
    print("Comparison chart saved to:", chart_path)
