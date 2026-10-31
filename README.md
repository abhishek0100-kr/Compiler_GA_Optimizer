# Compiler Studio — Genetic Algorithm-Based Compiler Optimization

A multi-page Streamlit application for studying compiler optimization-pass ordering using Genetic Algorithms (GA) over a simplified Three-Address Code (3AC) Intermediate Representation (IR).

## Project Overview

This project investigates how Genetic Algorithms can be used to search for effective compiler optimization-pass sequences. It implements a simplified compiler optimization environment with multiple optimization passes, a cost model, semantic validation, and experimental comparisons.

## Key Features

- **Variable-Length Genetic Algorithm:** Supports optimization sequences that can omit or repeat passes, with a maximum sequence length of 12.
- **Fixed-Point Pipeline:** Repeatedly applies optimization passes until the IR stops changing or a predefined round limit is reached.
- **Semantic Validation:** Compares original and optimized programs using finite input test vectors. This is sampled validation, not a formal proof of equivalence.
- **Input-Driven Benchmarks:** Supports INPUT statements and straight-line, non-constant benchmarks.
- **Optimization Passes:** Includes Constant Propagation (CP), Constant Folding (CF), Copy Propagation (CopyP), Common Subexpression Elimination (CSE), Algebraic Simplification (AS), and Dead Code Elimination (DCE).
- **Research Experiments:** Includes 20-seed experiments, exhaustive ordering enumeration, GA versus random-search comparison, pass ablation, and weight-sensitivity analysis.
- **Visualization:** Generates experiment graphs and result summaries.

## Technology Stack

- **Python:** Intermediate representation, optimization passes, cost model, Genetic Algorithm, and experiment execution.
- **Streamlit:** Interactive application interface.
- **Pandas:** Experiment data and CSV handling.
- **Altair and Matplotlib:** Data visualization and research figures.

## Project Structure

```text
Compiler_GA_Optimizer/
│
├── app.py
├── main.py
├── ir.py
├── benchmarks.py
├── cost_model.py
├── pipeline.py
├── pipeline_modes.py
├── semantics.py
├── research_experiments.py
├── run_experiments.py
├── plot_results.py
├── requirements.txt
├── README.md
│
├── ga/
│   └── Genetic Algorithm implementation
│
├── passes/
│   └── Compiler optimization passes
│
├── results/
│   └── Experiment CSV files, metadata, and figures
│
├── tests/
│   └── Extended feature tests
│
├── paper_assets/
│   └── Supporting manuscript materials
│
└── .streamlit/
    └── Application configuration
```

## Installation and Execution on Windows

### 1. Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Compiler_GA_Optimizer
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the application

```powershell
python -m streamlit run app.py
```

Alternatively, run `run_app.bat` after installing the dependencies.

## Running Tests

Execute the following commands from the project root directory:

```powershell
python test_ir.py
python test_all_passes.py
python test_pipeline.py
python test_cost_model.py
python test_ga.py
python tests/test_extended_features.py
```

These scripts verify the intermediate representation, optimization passes, pipeline, cost model, Genetic Algorithm, and extended features.

## Reproducing Research Experiments

Run:

```powershell
python research_experiments.py
```

The experiment outputs are stored in the `results/` directory.

The generated research artifacts include:

- `benchmark_summary.csv`
- `ga_20_seed_results.csv`
- `variable_ga_vs_random_20_seeds.csv`
- `exhaustive_ordering_costs.csv`
- `pass_ablation_fixed_point.csv`
- `weight_sensitivity.csv`
- `ga_convergence_by_seed.csv`
- `architecture_workflow.png`
- `ga_convergence_20_seeds.png`
- `ordering_cost_histograms.png`

The experimental setup includes:

- 20-seed Genetic Algorithm experiments.
- Exhaustive enumeration of all 720 single-use permutations of six optimization passes.
- A matched budget of 750 candidate evaluations for variable-length GA and random search.
- Fixed-point pipeline evaluation.
- Pass ablation and cost-weight sensitivity analysis.

The six-pass, single-use permutation space contains only 720 possible orderings and is small enough for exhaustive enumeration. Therefore, the experiments also investigate the enlarged variable-length search space and compare GA performance against random search.

## Intermediate Representation (IR)

The project uses a simplified Three-Address Code representation.

Example:

```text
INPUT x
INPUT y
t1 = x + y
t2 = t1 * 1
PRINT t2
```

Supported operations include:

- INPUT
- Numeric constants and assignments
- Copy operations
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- PRINT

The current implementation supports straight-line programs only. Branches, loops, and control-flow graphs are not implemented.

Semantic validation uses finite input test vectors. Passing these tests does not establish formal equivalence.

## Cost Model

The project uses a predefined static cost model:

| Instruction | Cost |
|---|---:|
| INPUT | 1 |
| CONST | 1 |
| COPY | 1 |
| BINOP | 3 |
| PRINT | 2 |

These values represent project-defined cost units. They are not measured processor cycles or actual execution times.

The weight-sensitivity experiment evaluates how changes in these weights affect the rankings of the 720 single-use optimization-pass orderings.

Actual runtime and code-size measurements are outside the current implementation.

## Experimental Scope and Limitations

- The compiler operates on a simplified, straight-line 3AC representation.
- Branches, loops, and control-flow graphs are not supported.
- Semantic validation uses finite test inputs rather than formal equivalence checking.
- The cost model uses predefined static weights.
- Native execution-time and machine-code-size measurements are not included.
- The fixed-length six-pass search space is exhaustively enumerable.

These limitations define the scope of the current experimental implementation.

## Manuscript and Submission Materials

The final IEEE manuscript PDF has been successfully prepared and is maintained as a separate submission artifact.

The editable LaTeX source package has been completed and is included as part of the submission materials.

All supporting research materials have been properly organized and are available in the paper_assets/ directory.

All required components have been prepared and verified to ensure a complete and correct submission package.