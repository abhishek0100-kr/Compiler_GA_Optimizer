# Genetic Algorithm-Based Compiler Optimization Pass Ordering

An automated compiler optimization tool that uses a Genetic Algorithm (GA) to find an effective ordering of optimization passes for Three-Address Code (3AC) Intermediate Representation.

## Project Overview

The project addresses the Compiler Phase Ordering Problem, where different orders of optimization passes can produce different optimization results.

The system uses:
- Non-SSA 3AC Intermediate Representation
- 6 compiler optimization passes
- Static instruction cost model
- Genetic Algorithm for pass ordering
- Benchmark programs for evaluation

## Optimization Passes

1. Constant Propagation (CP)
2. Constant Folding (CF)
3. Copy Propagation (CopyP)
4. Common Subexpression Elimination (CSE)
5. Algebraic Simplification (AS)
6. Dead Code Elimination (DCE)

## Genetic Algorithm

- Chromosome: Permutation of 6 optimization passes
- Selection: Tournament Selection
- Crossover: Order Crossover (OX)
- Mutation: Swap Mutation
- Elitism: Top 2 candidates
- Population: 30–50
- Generations: 50

## Cost Model

| Instruction | Cost |
|---|---:|
| CONST | 1 |
| COPY | 1 |
| BINOP | 3 |
| PRINT | 2 |

Fitness is calculated from the final optimized IR cost.

## Project Structure

```text
Compiler_GA_Optimizer/
├── ga/
├── passes/
├── benchmarks.py
├── cost_model.py
├── ir.py
├── pipeline.py
├── main.py
├── run_experiments.py
├── plot_results.py
├── test_*.py
├── requirements.txt
└── README.md

How to Run

Setup:

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Run Tests

python test_ir.py
python test_all_passes.py
python test_pipeline.py
python test_cost_model.py
python test_ga.py

Run the Project

python main.py
Run Experiments
python run_experiments.py
python plot_results.py

Goal

To automatically find effective compiler optimization pass orderings using a Genetic Algorithm and compare them with unoptimized, random, and manually selected orderings.