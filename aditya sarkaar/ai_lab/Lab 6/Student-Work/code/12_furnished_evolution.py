import importlib
from pathlib import Path


furnished = importlib.import_module("11_furnished_room")
fitness_module = importlib.import_module("07_fitness")
operators = importlib.import_module("08_genetic_operators")
evolution = importlib.import_module("09_evolution")
results = importlib.import_module("10_results")


POPULATION_SIZE = 50
GENERATIONS = 200
TRAINING_RUNS = 3
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def score_population(population, room, starts):
    scores = []

    for chromosome in population:
        episodes = furnished.evaluate(chromosome, room, starts)
        scores.append(
            sum(item["efficiency"] for item in episodes) / len(episodes)
        )

    return scores


def evolve(room, seed=71):
    starts = furnished.make_starts(room, seed=90, count=TRAINING_RUNS)
    population = fitness_module.make_population(size=POPULATION_SIZE, seed=seed)
    history = []
    best_chromosome = None
    best_fitness = -1.0

    for generation in range(GENERATIONS):
        scores = score_population(population, room, starts)
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


if __name__ == "__main__":
    room = furnished.make_furnished_room()
    history, chromosome = evolve(room)

    history_path = OUTPUT_DIR / "furnished_fitness_history.csv"
    chromosome_path = OUTPUT_DIR / "furnished_best_chromosome.json"
    evolution.save_history(history, history_path)
    evolution.save_chromosome(chromosome, chromosome_path)
    results.plot_fitness(history, OUTPUT_DIR / "furnished_fitness_curve.png")

    validation_starts = furnished.make_starts(room, seed=81, count=furnished.VALIDATION_RUNS)
    episodes = furnished.evaluate(chromosome, room, validation_starts)
    best_episode = max(episodes, key=lambda item: item["efficiency"])
    mean_efficiency = sum(item["efficiency"] for item in episodes) / len(episodes)

    results.plot_trajectory(
        room,
        best_episode["trajectory"],
        best_episode["trajectory"][0],
        best_episode["final_position"],
        best_episode["efficiency"],
        OUTPUT_DIR / "furnished_best_trajectory.png",
    )

    print("Population size:", POPULATION_SIZE)
    print("Generations:", GENERATIONS)
    print("Initial average fitness:", f"{history[0]['average']:.2%}")
    print("Final average fitness:", f"{history[-1]['average']:.2%}")
    print("Best training fitness:", f"{max(item['best'] for item in history):.2%}")
    print("Validation mean efficiency:", f"{mean_efficiency:.2%}")
    print("Validation best efficiency:", f'{best_episode["efficiency"]:.2%}')
    print("Furnished history saved to:", history_path)
    print("Furnished chromosome saved to:", chromosome_path)
