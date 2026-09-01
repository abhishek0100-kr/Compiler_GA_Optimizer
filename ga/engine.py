import random
from cost_model import evaluate_pipeline_fitness
from ga.operators import (
    create_initial_population,
    tournament_selection,
    order_crossover,
    swap_mutation,
)
from passes import PASS_NAMES


def run_genetic_algorithm(
    ir_program,
    pop_size=30,
    generations=40,
    crossover_rate=0.8,
    mutation_rate=0.15,
    elitism_count=2,
    tournament_k=3,
    seed=None,
    verbose=False,
):
    if seed is not None:
        random.seed(seed)

    population = create_initial_population(pop_size)
    history = []
    best_overall = None

    for gen in range(1, generations + 1):
        evaluated_pop = []
        for chrom in population:
            eval_result = evaluate_pipeline_fitness(ir_program, chrom)
            evaluated_pop.append(
                {
                    "chromosome": chrom,
                    "cost": eval_result["cost"],
                    "fitness": eval_result["fitness"],
                    "optimized_ir": eval_result["optimized_ir"],
                }
            )

        evaluated_pop.sort(key=lambda item: item["fitness"], reverse=True)

        current_best = evaluated_pop[0]
        if best_overall is None or current_best["fitness"] > best_overall["fitness"]:
            best_overall = current_best

        avg_fitness = sum(item["fitness"] for item in evaluated_pop) / len(
            evaluated_pop
        )
        avg_cost = sum(item["cost"] for item in evaluated_pop) / len(
            evaluated_pop
        )

        gen_stats = {
            "generation": gen,
            "best_fitness": current_best["fitness"],
            "best_cost": current_best["cost"],
            "avg_fitness": round(avg_fitness, 4),
            "avg_cost": round(avg_cost, 2),
            "best_chromosome": list(current_best["chromosome"]),
            "best_pipeline": [PASS_NAMES[i] for i in current_best["chromosome"]],
        }
        history.append(gen_stats)

        if verbose and (gen == 1 or gen % 10 == 0 or gen == generations):
            print(
                f"Gen {gen:2d} | Best Cost: {current_best['cost']:2d} | "
                f"Best Fitness: {current_best['fitness']:8.4f} | "
                f"Avg Cost: {avg_cost:5.2f} | "
                f"Pipeline: {' -> '.join(gen_stats['best_pipeline'])}"
            )

        new_population = []

        for i in range(elitism_count):
            new_population.append(list(evaluated_pop[i]["chromosome"]))

        while len(new_population) < pop_size:
            parent1 = tournament_selection(evaluated_pop, k=tournament_k)
            parent2 = tournament_selection(evaluated_pop, k=tournament_k)

            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2)
            else:
                child = list(parent1)

            child = swap_mutation(child, mutation_rate=mutation_rate)
            new_population.append(child)

        population = new_population

    return {
        "best_solution": best_overall,
        "best_pipeline_names": [
            PASS_NAMES[i] for i in best_overall["chromosome"]
        ],
        "history": history,
    }