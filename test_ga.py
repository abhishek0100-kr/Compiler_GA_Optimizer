from ga.operators import (
    create_random_chromosome,
    create_initial_population,
    order_crossover,
    swap_mutation,
)
from ga.engine import run_genetic_algorithm
from ir import validate_ir, format_ir


def test_ga_operators():
    chrom = create_random_chromosome()
    assert len(chrom) == 6, f"Expected chromosome length 6, got {len(chrom)}"
    assert sorted(chrom) == [0, 1, 2, 3, 4, 5], "Chromosome is not a valid permutation"

    pop = create_initial_population(20)
    assert len(pop) == 20
    for individual in pop:
        assert sorted(individual) == [0, 1, 2, 3, 4, 5]

    p1 = [0, 1, 2, 3, 4, 5]
    p2 = [5, 4, 3, 2, 1, 0]
    for _ in range(20):
        child = order_crossover(p1, p2)
        assert len(child) == 6
        assert sorted(child) == [0, 1, 2, 3, 4, 5], "OX produced invalid permutation"

    for _ in range(20):
        mut = swap_mutation(p1, mutation_rate=1.0)
        assert len(mut) == 6
        assert sorted(mut) == [0, 1, 2, 3, 4, 5], "Mutation corrupted permutation"

    print("[PASS] GA Operators (Permutation, OX, Swap Mutation) verified successfully.")


def test_ga_engine_run():
    # Benchmark IR where ordering is strictly critical
    # Pipeline finding CP -> CF -> DCE eliminates almost everything
    sample_ir = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", "a", "b"),
        ("BINOP", "*", "t2", "t1", 2),
        ("COPY", "unused", "t2"),
        ("PRINT", "t1"),
    ]

    is_valid, msg = validate_ir(sample_ir)
    assert is_valid, f"Sample IR invalid: {msg}"

    print("\n--- Running GA Search on Sample IR ---")
    result = run_genetic_algorithm(
        sample_ir,
        pop_size=25,
        generations=20,
        seed=42,
        verbose=True,
    )

    best = result["best_solution"]
    pipeline_names = result["best_pipeline_names"]

    print("\nGA Search Results:")
    print(f"Optimal Pipeline Found: {' -> '.join(pipeline_names)}")
    print(f"Initial Cost: 11 | Final Cost: {best['cost']} | Fitness: {best['fitness']}")
    print("\nOptimized IR Produced:")
    print(format_ir(best["optimized_ir"]))

    assert best["cost"] <= 5, f"GA failed to optimize program well, cost={best['cost']}"
    assert len(result["history"]) == 20, "History length mismatch"
    print("\n[PASS] GA Engine execution and convergence verified successfully.")


if __name__ == "__main__":
    test_ga_operators()
    test_ga_engine_run()