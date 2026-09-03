import importlib
import json
import random
from pathlib import Path


simulation = importlib.import_module("06_simulation")
results = importlib.import_module("10_results")


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
VALIDATION_RUNS = 8


def make_furnished_room():
    """Create a room with 100 obstacle cells in two rectangular blocks."""
    room = simulation.make_room()

    # 4 x 10 = 40 cells.
    for row in range(4, 8):
        for col in range(8, 18):
            room[row][col] = simulation.OBSTACLE

    # 5 x 12 = 60 cells, for 100 obstacle cells in total.
    for row in range(12, 17):
        for col in range(25, 37):
            room[row][col] = simulation.OBSTACLE

    return room


def make_starts(room, seed=81, count=VALIDATION_RUNS):
    generator = random.Random(seed)
    starts = []

    while len(starts) < count:
        row = generator.randrange(simulation.ROWS)
        col = generator.randrange(simulation.COLS)

        if room[row][col] == simulation.EMPTY:
            direction = generator.randrange(4)
            starts.append((row, col, direction))

    return starts


def evaluate(chromosome, room, starts):
    episodes = [
        simulation.simulate(
            chromosome,
            row,
            col,
            direction,
            seed=200 + number,
            room_template=room,
        )
        for number, (row, col, direction) in enumerate(starts)
    ]
    return episodes


if __name__ == "__main__":
    with (OUTPUT_DIR / "best_chromosome.json").open(encoding="utf-8") as file:
        chromosome = json.load(file)

    room = make_furnished_room()
    starts = make_starts(room)
    episodes = evaluate(chromosome, room, starts)
    mean_efficiency = sum(item["efficiency"] for item in episodes) / len(episodes)
    best_episode = max(episodes, key=lambda item: item["efficiency"])
    worst_episode = min(episodes, key=lambda item: item["efficiency"])

    results.plot_trajectory(
        room,
        best_episode["trajectory"],
        best_episode["trajectory"][0],
        best_episode["final_position"],
        best_episode["efficiency"],
        OUTPUT_DIR / "furnished_transfer_trajectory.png",
    )

    print("Obstacle cells:", sum(cell == simulation.OBSTACLE for row in room for cell in row))
    print("Paintable cells:", sum(cell == simulation.EMPTY for row in room for cell in row))
    print("Mean transfer efficiency:", f"{mean_efficiency:.2%}")
    print("Best transfer efficiency:", f'{best_episode["efficiency"]:.2%}')
    print("Worst transfer efficiency:", f'{worst_episode["efficiency"]:.2%}')
    print("Trajectory plot saved to:", OUTPUT_DIR / "furnished_transfer_trajectory.png")
