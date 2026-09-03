import importlib
import random


fitness_module = importlib.import_module("07_fitness")


ELITE_COUNT = 2
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.002


def tournament_select(population, scores, generator):
    """Choose the fittest chromosome from a random tournament."""
    contestants = [
        generator.randrange(len(population))
        for _ in range(TOURNAMENT_SIZE)
    ]
    winner = max(contestants, key=lambda index: scores[index])
    return population[winner][:]


def crossover(parent_a, parent_b, generator):
    """Combine two parents at one randomly chosen crossover point."""
    point = generator.randrange(1, len(parent_a))
    child = parent_a[:point] + parent_b[point:]
    return child


def mutate(chromosome, generator, rate=MUTATION_RATE):
    """Randomly replace genes while keeping the action alphabet 0 to 3."""
    mutation_count = 0

    for index, old_action in enumerate(chromosome):
        if generator.random() < rate:
            possible_actions = [0, 1, 2, 3]
            possible_actions.remove(old_action)
            chromosome[index] = generator.choice(possible_actions)
            mutation_count += 1

    return mutation_count


def make_next_generation(population, scores, seed=41):
    """Create one new population using elitism and genetic operators."""
    generator = random.Random(seed)
    ranking = sorted(
        range(len(population)),
        key=lambda index: scores[index],
        reverse=True,
    )

    next_population = [population[index][:] for index in ranking[:ELITE_COUNT]]
    mutation_count = 0

    while len(next_population) < len(population):
        parent_a = tournament_select(population, scores, generator)
        parent_b = tournament_select(population, scores, generator)
        child = crossover(parent_a, parent_b, generator)
        mutation_count += mutate(child, generator)
        next_population.append(child)

    return next_population, mutation_count


def score_population(population, starts):
    return [fitness_module.fitness(chromosome, starts) for chromosome in population]


if __name__ == "__main__":
    starts = fitness_module.make_starts()
    population = fitness_module.make_population()
    old_scores = score_population(population, starts)
    next_population, mutation_count = make_next_generation(population, old_scores)
    new_scores = score_population(next_population, starts)

    print("Population size:", len(next_population))
    print("Elite chromosomes preserved:", ELITE_COUNT)
    print("Mutated genes:", mutation_count)
    print("Old best fitness:", f"{max(old_scores):.2%}")
    print("New best fitness:", f"{max(new_scores):.2%}")
    print("New average fitness:", f"{sum(new_scores) / len(new_scores):.2%}")
