# Project revision changelog

## Implemented
- Extended 3AC with `INPUT` and a reference interpreter for straight-line programs.
- Added semantic output checks inside fitness evaluation. Candidate transformations that change outputs on supplied test vectors are penalized with zero fitness.
- Added a variable-length GA chromosome: passes may be omitted or repeated; sequence length is capped at 12.
- Added fixed-point pipeline application with a convergence cap.
- Added input-driven arithmetic benchmarks.
- Added a reproducible 20-seed experiment harness, exhaustive 720-ordering enumeration, matched-budget variable-length GA/random search, pass ablation, weight-sensitivity ranking correlations, CSV result files, and research figures.
- Added draft Abstract/Index Terms and a reviewer action checklist.
- Added tests for the new functionality.

## Verification
- Existing tests and the new extended-feature test pass in the development environment.
- `streamlit` was not installed in the packaging environment, so the Streamlit UI could not be launched for a browser-level smoke test here. Install dependencies from `requirements.txt` and run `streamlit run app.py` locally.

## Deliberately not claimed as completed
- Branches and loops: the IR remains straight-line; safe control-flow optimization requires CFG-aware data-flow analyses.
- Runtime/cycle/code-size correlation: current cost remains a static model. Weight-sensitivity results are included, but hardware measurements are not.
- Formal equivalence: finite test-vector checks are useful translation validation, not proof.
- IEEE manuscript edits and reference/DOI verification: the source manuscript was not included in the provided ZIP. See `paper_assets/reviewer_action_checklist.md`.
- Public repository publication, author emails, and author photographs: require author-supplied information and an owner-controlled publication step.
