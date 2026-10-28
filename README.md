# Compiler Studio — Genetic Algorithm-Based Compiler Optimization

A multi-page Streamlit application for experiments on compiler optimization-pass ordering over a simplified three-address-code (3AC) IR.

## New in this revision
- **Variable-length/repeated-pass GA:** candidate sequences can omit or repeat passes; sequence length is capped at 12, greatly enlarging the search space compared with the 720 one-use permutations.
- **Fixed-point pipeline:** repeatedly applies a pass sequence until the IR stops changing, with a bounded round count.
- **Semantic checks in fitness:** the evaluator runs original and optimized straight-line IR on finite input vectors; candidates that fail are assigned zero fitness. This is testing/translation validation on sampled cases, not a formal equivalence proof.
- **Input-driven benchmarks:** added `INPUT` statements and non-constant straight-line benchmarks. Branches and loops are not supported yet.
- **Research experiments:** 20-seed runs, exact enumeration of the 720 single-use orderings, a matched-budget (750 candidate evaluations) variable-length GA versus random-search comparison, fixed-point baseline, pass ablation, weight sensitivity, and figures.
- **Paper assets:** draft Abstract/Index Terms and a reviewer action checklist.

## Technology stack
- Python — IR, optimization passes, cost model, GA and experiment harness.
- Streamlit — multi-page web UI.
- Pandas — experiment tables and CSVs.
- Altair / Matplotlib — charts and generated research figures.

## Run on Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
Or run `run_app.bat` after dependencies are installed.

## Run tests
From the `Compiler_GA_Optimizer` project directory:
```bash
python test_ir.py
python test_all_passes.py
python test_pipeline.py
python test_cost_model.py
python test_ga.py
python tests/test_extended_features.py
```

## Reproduce research artifacts
```bash
python research_experiments.py
```
Outputs are saved in `results/`:
- `benchmark_summary.csv`
- `ga_20_seed_results.csv` (20 seeds)
- `variable_ga_vs_random_20_seeds.csv` (20 seeds)
- `exhaustive_ordering_costs.csv`
- `pass_ablation_fixed_point.csv`
- `weight_sensitivity.csv` (Spearman rank correlation of all single-use ordering ranks under weight perturbations)
- `ga_convergence_by_seed.csv`
- `architecture_workflow.png`, `ga_convergence_20_seeds.png`, `ordering_cost_histograms.png`

The experiment script uses 20 seeds and matched budgets of 750 candidate evaluations for the variable-length GA and random-search comparator. Exact enumeration is performed for the six-pass, one-use permutation space (720 orderings). That space is small enough that a GA is not justified by itself; the GA's role must be assessed on the enlarged variable-length search space and reported neutrally against the matched-budget random baseline.

## IR syntax
```text
INPUT x
INPUT y
t1 = x + y
t2 = t1 * 1
PRINT t2
```
Supported operations are `INPUT`, numeric assignments, copies, `+ - * /`, and `PRINT`. The current IR is straight-line and has no branches or loops. The interpreter used for semantic checking uses supplied finite test vectors; passing these tests does not constitute formal proof of equivalence.

## Interpreting the cost model
The model uses predefined weights (`INPUT=1`, `CONST=1`, `COPY=1`, `BINOP=3`, `PRINT=2`). These are model units, not measured cycles or runtime. The weight-sensitivity experiment evaluates how perturbing weights affects rankings of the 720 one-use orderings. Actual runtime and code-size measurements remain future work.

## Manuscript status
See `paper_assets/reviewer_action_checklist.md` and `paper_assets/abstract_index_terms.tex`. The ZIP supplied for this revision did not include the IEEE manuscript itself, so manuscript-specific edits (reference DOI verification, author details/photos, running headers, template metadata, and inserting figures into the final paper) remain to be completed against the actual manuscript. Do not fabricate author emails, photographs, DOIs, or a public repository URL.
