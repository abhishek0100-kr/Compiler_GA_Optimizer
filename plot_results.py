import os
import matplotlib.pyplot as plt
from benchmarks import get_all_benchmarks
from cost_model import compute_ir_cost, evaluate_pipeline_fitness
from ga.engine import run_genetic_algorithm
from run_experiments import FIXED_PIPELINE, run_random_search


def generate_plots():
    benchmarks = get_all_benchmarks()
    bm_labels = []
    o0_costs = []
    fixed_costs = []
    random_costs = []
    ga_costs = []

    for name, ir_code in benchmarks.items():
        short_name = name.split("_")[0] + "\n" + "_".join(name.split("_")[1:])
        bm_labels.append(short_name)

        o0_costs.append(compute_ir_cost(ir_code))
        fixed_costs.append(evaluate_pipeline_fitness(ir_code, FIXED_PIPELINE)["cost"])
        random_costs.append(run_random_search(ir_code, num_evaluations=750, seed=42)["cost"])

        ga_res = run_genetic_algorithm(ir_code, pop_size=30, generations=25, seed=42)
        ga_costs.append(ga_res["best_solution"]["cost"])

    x = range(len(bm_labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar([i - 1.5 * width for i in x], o0_costs, width, label="O0 (Unoptimized)", color="#e74c3c")
    ax.bar([i - 0.5 * width for i in x], fixed_costs, width, label="Fixed Pipeline", color="#e67e22")
    ax.bar([i + 0.5 * width for i in x], random_costs, width, label="Random Search", color="#f1c40f")
    ax.bar([i + 1.5 * width for i in x], ga_costs, width, label="GA Optimal", color="#2ecc71")

    ax.set_xlabel("Benchmark Program", fontweight="bold")
    ax.set_ylabel("Estimated IR Execution Cost", fontweight="bold")
    ax.set_title("Compiler Optimization Cost Comparison Across Baselines", fontweight="bold", pad=15)
    ax.set_xticks(list(x))
    ax.set_xticklabels(bm_labels, fontsize=9)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("benchmark_comparison.png", dpi=300)
    plt.close()
    print("[PASS] Saved: benchmark_comparison.png")

    target_bm = benchmarks["BM2_Redundant_Expressions"]
    ga_run = run_genetic_algorithm(target_bm, pop_size=30, generations=30, seed=42)
    history = ga_run["history"]

    gens = [h["generation"] for h in history]
    best_fitness = [h["best_fitness"] for h in history]
    avg_fitness = [h["avg_fitness"] for h in history]

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.plot(gens, best_fitness, color="#2980b9", linewidth=2.2, label="Best Population Fitness")
    ax.plot(gens, avg_fitness, color="#8e44ad", linestyle="--", linewidth=1.8, label="Average Population Fitness")

    ax.set_xlabel("Generation", fontweight="bold")
    ax.set_ylabel("Fitness Score (1000 / (1 + Cost))", fontweight="bold")
    ax.set_title("GA Fitness Convergence Trajectory (BM2: Redundant Expressions)", fontweight="bold", pad=15)
    ax.legend(loc="lower right")
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("ga_convergence.png", dpi=300)
    plt.close()
    print("[PASS] Saved: ga_convergence.png")


if __name__ == "__main__":
    generate_plots()