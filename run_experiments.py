import random
from benchmarks import get_all_benchmarks
from cost_model import compute_ir_cost, evaluate_pipeline_fitness
from ga.engine import run_genetic_algorithm
from ga.operators import create_random_chromosome
from passes import PASS_NAMES

FIXED_PIPELINE = ["CP", "CF", "CopyP", "CSE", "AS", "DCE"]


def run_random_search(ir_program, num_evaluations=750, seed=42):
    random.seed(seed)
    best_eval = None

    for _ in range(num_evaluations):
        chrom = create_random_chromosome()
        eval_res = evaluate_pipeline_fitness(ir_program, chrom)
        if best_eval is None or eval_res["fitness"] > best_eval["fitness"]:
            best_eval = {
                "chromosome": chrom,
                "cost": eval_res["cost"],
                "fitness": eval_res["fitness"],
                "pipeline_names": [PASS_NAMES[i] for i in chrom],
                "optimized_ir": eval_res["optimized_ir"],
            }

    return best_eval


def run_benchmark_experiments():
    benchmarks = get_all_benchmarks()
    results = []

    print("=" * 80)
    print("COMPILER GA OPTIMIZER - EMPIRICAL BENCHMARK EVALUATION")
    print("=" * 80)

    for bm_name, ir_code in benchmarks.items():
        print(f"\nEvaluating: {bm_name} ({len(ir_code)} instructions)")

        o0_cost = compute_ir_cost(ir_code)

        fixed_res = evaluate_pipeline_fitness(ir_code, FIXED_PIPELINE)
        fixed_cost = fixed_res["cost"]

        rand_res = run_random_search(ir_code, num_evaluations=750, seed=42)
        rand_cost = rand_res["cost"]

        ga_res = run_genetic_algorithm(
            ir_code,
            pop_size=30,
            generations=25,
            seed=42,
            verbose=False,
        )
        ga_best = ga_res["best_solution"]
        ga_cost = ga_best["cost"]
        ga_pipeline = " -> ".join(ga_res["best_pipeline_names"])

        ga_reduction = (
            ((o0_cost - ga_cost) / o0_cost) * 100 if o0_cost > 0 else 0.0
        )

        row = {
            "Benchmark": bm_name,
            "O0_Cost": o0_cost,
            "Fixed_Cost": fixed_cost,
            "Random_Cost": rand_cost,
            "GA_Cost": ga_cost,
            "GA_Reduction_%": round(ga_reduction, 1),
            "GA_Pipeline": ga_pipeline,
        }
        results.append(row)

    print("\n" + "=" * 80)
    print("COMPARATIVE RESULTS SUMMARY")
    print("=" * 80)
    header = f"{'Benchmark':<28} | {'O0':<5} | {'Fixed':<6} | {'Random':<6} | {'GA':<5} | {'GA Red.%':<8}"
    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['Benchmark']:<28} | {r['O0_Cost']:<5} | {r['Fixed_Cost']:<6} | {r['Random_Cost']:<6} | {r['GA_Cost']:<5} | {r['GA_Reduction_%']}%"
        )

    print("=" * 80)
    return results


if __name__ == "__main__":
    run_benchmark_experiments()