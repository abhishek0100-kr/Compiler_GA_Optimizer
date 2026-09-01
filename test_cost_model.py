from cost_model import (
    compute_instruction_cost,
    compute_ir_cost,
    compute_fitness,
    evaluate_pipeline_fitness,
)
from ir import validate_ir


def test_cost_model_and_fitness():
    assert compute_instruction_cost(("CONST", "a", 10)) == 1
    assert compute_instruction_cost(("COPY", "b", "a")) == 1
    assert compute_instruction_cost(("BINOP", "+", "c", "a", "b")) == 3
    assert compute_instruction_cost(("PRINT", "c")) == 2

    sample_ir = [
        ("CONST", "a", 10),  # 1
        ("CONST", "b", 20),  # 1
        ("BINOP", "+", "t1", "a", "b"),  # 3
        ("PRINT", "t1"),  # 2
    ]
    # Total cost = 1 + 1 + 3 + 2 = 7
    total_cost = compute_ir_cost(sample_ir)
    assert total_cost == 7, f"Expected cost 7, got {total_cost}"

    expected_fitness = round(1000.0 / (1.0 + 7), 4)  # 1000 / 8 = 125.0
    fitness_val = compute_fitness(total_cost)
    assert (
        fitness_val == expected_fitness
    ), f"Expected {expected_fitness}, got {fitness_val}"

    # Verify pipeline evaluation comparison
    # Pipeline A (CP -> CF -> DCE) produces 2 instructions (CONST t1, PRINT t1) -> Cost = 1 + 2 = 3
    # Pipeline B (DCE -> CP -> CF) produces 4 instructions (CONST a, CONST b, CONST t1, PRINT t1) -> Cost = 1 + 1 + 1 + 2 = 5
    test_program = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", "a", "b"),
        ("BINOP", "*", "unused", "t1", 2),
        ("PRINT", "t1"),
    ]

    res_a = evaluate_pipeline_fitness(test_program, ["CP", "CF", "DCE"])
    res_b = evaluate_pipeline_fitness(test_program, ["DCE", "CP", "CF"])

    assert res_a["cost"] == 3, f"Expected Pipeline A cost 3, got {res_a['cost']}"
    assert res_b["cost"] == 5, f"Expected Pipeline B cost 5, got {res_b['cost']}"
    assert (
        res_a["fitness"] > res_b["fitness"]
    ), "Pipeline A should have higher fitness than Pipeline B"

    print("=" * 60)
    print("COST MODEL & FITNESS EVALUATION TEST")
    print("=" * 60)
    print(f"Sample IR Cost: {total_cost} | Fitness: {fitness_val}")
    print(
        f"Pipeline A (Good order) Cost: {res_a['cost']} | Fitness: {res_a['fitness']}"
    )
    print(
        f"Pipeline B (Poor order) Cost: {res_b['cost']} | Fitness: {res_b['fitness']}"
    )
    print("\n[PASS] Cost model and fitness evaluator verified successfully.")


if __name__ == "__main__":
    test_cost_model_and_fitness()