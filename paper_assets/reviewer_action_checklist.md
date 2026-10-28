# Reviewer action checklist — implementation status

## Implemented in this project archive
- [x] Added variable-length chromosomes (length 1–12) allowing omitted and repeated passes.
- [x] Added fixed-point iteration for a pipeline until the IR stops changing (bounded by a maximum round count).
- [x] Added input-driven straight-line 3AC benchmarks (`INPUT`) and an interpreter for finite output comparisons.
- [x] Integrated finite test-case semantic validation into candidate fitness. Invalid candidates receive zero fitness/infinite cost.
- [x] Added 20-seed experiments, exhaustive enumeration of all 720 single-use permutations, a matched 750-candidate-evaluation comparison for variable-length GA versus variable-length random search, and result CSVs.
- [x] Added fixed-point baseline, pass ablation, weight sensitivity across all six-pass permutations, and figures for ordering-cost histograms, GA convergence, and architecture workflow.
- [x] Added a draft Abstract and Index Terms LaTeX insert.
- [x] Added tests for the new input, fixed-point, semantic validation, and variable-length search functionality.

## Partially addressed / remaining
- [ ] Benchmarks now include inputs and nontrivial arithmetic, but the current IR remains straight-line. Branches, loops, CFG construction, and data-flow analysis across control-flow edges require a larger IR/compiler redesign and are not claimed as implemented.
- [ ] Finite input-vector validation is not formal equivalence proof. It can miss edge cases; add translation validation or a sound semantics checker for stronger claims.
- [ ] The cost model remains hand-weighted. Weight-sensitivity outputs are included, but measured runtime, machine cycles, generated-code size, or LLVM/native-code experiments are not implemented.
- [ ] Do not claim GA superiority where matched-budget results tie. The generated tables intentionally expose ties and cases where random search is competitive.
- [ ] A screenshot of the running Streamlit UI must be captured by running the app on the target machine; no synthetic screenshot is passed off as a real one.
- [ ] The provided archive does not contain the full IEEE manuscript, so its body, running headers, author biographies, references, DOI metadata, and figures cannot be safely edited in-place here.
- [ ] Author emails and photographs must be supplied by the authors; they must not be fabricated.
- [ ] Publishing to a public Git repository requires an owner-controlled remote and explicit publication action. Use the included source archive and metadata; do not claim that a repository has been published.

## Important interpretation
The 720-permutation search remains exactly enumerable. The fixed-length GA's high success rate on this small space is not evidence that GA is necessary. The extended search increases the sequence space but results must be reported neutrally, with matched candidate-evaluation budgets and the fixed-point baseline.
