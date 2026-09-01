import random
from passes import PASS_NAMES

NUM_PASSES = len(PASS_NAMES)


def create_random_chromosome():
    genes = list(range(NUM_PASSES))
    random.shuffle(genes)
    return genes


def create_initial_population(pop_size):
    return [create_random_chromosome() for _ in range(pop_size)]


def tournament_selection(population_with_fitness, k=3):
    selected_k = random.sample(population_with_fitness, k)
    selected_k.sort(key=lambda item: item["fitness"], reverse=True)
    return selected_k[0]["chromosome"]


def order_crossover(parent1, parent2):
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[idx1 : idx2 + 1] = parent1[idx1 : idx2 + 1]

    copied_genes = set(child[idx1 : idx2 + 1])
    p2_remaining = [gene for gene in parent2 if gene not in copied_genes]

    p2_idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = p2_remaining[p2_idx]
            p2_idx += 1

    return child


def swap_mutation(chromosome, mutation_rate=0.15):
    mutated = list(chromosome)
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated