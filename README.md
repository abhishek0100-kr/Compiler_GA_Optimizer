# Compiler Studio — Genetic Algorithm-Based Compiler Optimization

A multi-page Streamlit application for exploring compiler optimization pass ordering over three-address code (3AC).

## Features
- **Overview:** project dashboard and guided workflow.
- **Optimize IR:** benchmark/custom input, configurable genetic algorithm, before/after IR, convergence chart, baseline comparison, and optimized IR download.
- **Optimization passes:** reference for all six compiler transformations.
- **Benchmarks:** inspect five built-in programs and their estimated starting costs.
- **Methodology:** explains representation, genetic search, static cost model, and limitations.
- Responsive styling, reusable result state, custom 3AC validation, and optional reproducible random seed.

## Run on Windows
1. Extract the project ZIP.
2. Open a terminal in the `Compiler_GA_Optimizer` folder.
3. Create and activate an environment (recommended):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   streamlit run app.py
   ```

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run tests
Run the existing test scripts from the project root, for example:
```bash
python test_ir.py
python test_all_passes.py
python test_pipeline.py
python test_cost_model.py
python test_ga.py
```

## Important interpretation note
The optimizer scores resulting IR with a static instruction-cost model (CONST=1, COPY=1, BINOP=3, PRINT=2). Results are estimated cost changes, not measured runtime speedups. Benchmark performance on a target runtime before making execution-speed claims.
