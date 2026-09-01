import sys
from ir import validate_ir, format_ir
from cost_model import compute_ir_cost, evaluate_pipeline_fitness
from ga.engine import run_genetic_algorithm
from pipeline import execute_pipeline


def print_divider(title=""):
    if title:
        print(f"\n{'=' * 20} {title} {'=' * 20}")
    else:
        print("=" * 60)


def run_optimizer(
    ir_program,
    program_name="Custom Program",
    pop_size=30,
    generations=30,
    verbose=True,
):
    is_valid, msg = validate_ir(ir_program)
    if not is_valid:
        print(f"Error: Invalid IR Program - {msg}")
        return

    unoptimized_cost = compute_ir_cost(ir_program)

    print_divider(f"PROGRAM: {program_name}")
    print("Initial (Unoptimized) IR:")
    print(format_ir(ir_program))
    print(f"Initial Instruction Count : {len(ir_program)}")
    print(f"Initial Estimated Cost    : {unoptimized_cost}")

    print_divider("GENETIC ALGORITHM SEARCH")
    ga_result = run_genetic_algorithm(
        ir_program,
        pop_size=pop_size,
        generations=generations,
        verbose=verbose,
    )

    best_solution = ga_result["best_solution"]
    best_pipeline = ga_result["best_pipeline_names"]
    optimized_ir = best_solution["optimized_ir"]
    optimized_cost = best_solution["cost"]
    best_fitness = best_solution["fitness"]

    cost_reduction = unoptimized_cost - optimized_cost
    pct_reduction = (
        (cost_reduction / unoptimized_cost) * 100
        if unoptimized_cost > 0
        else 0.0
    )

    print_divider("OPTIMIZATION SUMMARY")
    print(f"Best Pass Pipeline Found : {' -> '.join(best_pipeline)}")
    print(f"Best Fitness Score       : {best_fitness:.4f}")
    print(
        f"Instruction Count        : {len(ir_program)} -> {len(optimized_ir)} "
        f"(-{len(ir_program) - len(optimized_ir)})"
    )
    print(
        f"Estimated Cost           : {unoptimized_cost} -> {optimized_cost} "
        f"(-{cost_reduction}, {pct_reduction:.1f}% reduction)"
    )

    print("\nFinal Optimized IR:")
    print(format_ir(optimized_ir))
    print_divider()


def main():
    sample_program = [
        ("CONST", "x", 5),
        ("CONST", "y", 10),
        ("BINOP", "+", "t1", "x", "y"),
        ("COPY", "a", "t1"),
        ("BINOP", "+", "t2", "x", "y"),
        ("BINOP", "*", "t3", "t2", 1),
        ("BINOP", "+", "t4", "t3", 0),
        ("BINOP", "+", "dead1", "x", 99),
        ("COPY", "dead2", "dead1"),
        ("BINOP", "+", "ans", "a", "t4"),
        ("PRINT", "ans"),
    ]

    run_optimizer(
        sample_program,
        program_name="Integration Sample Program",
        pop_size=30,
        generations=25,
        verbose=True,
    )


if __name__ == "__main__":
    main()