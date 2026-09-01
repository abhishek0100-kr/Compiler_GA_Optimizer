import altair as alt
import pandas as pd
import streamlit as st

from ir import validate_ir, format_ir
from cost_model import compute_ir_cost, evaluate_pipeline_fitness
from ga.engine import run_genetic_algorithm
from benchmarks import get_all_benchmarks
from run_experiments import FIXED_PIPELINE, run_random_search

COLOR_BG = "#F5F6F7"
COLOR_PANEL = "#FFFFFF"
COLOR_BORDER = "#D8DBDF"
COLOR_TEXT = "#1C1F24"
COLOR_MUTED = "#6B7280"

COLOR_O0 = "#e74c3c"
COLOR_FIXED = "#e67e22"
COLOR_RANDOM = "#f1c40f"
COLOR_GA = "#2ecc71"
COLOR_BEST_FIT = "#2980b9"
COLOR_AVG_FIT = "#8e44ad"

_BINOPS = {"+", "-", "*", "/"}


def _is_number(token):
    try:
        int(token)
        return True
    except ValueError:
        try:
            float(token)
            return True
        except ValueError:
            return False


def _to_number(token):
    try:
        return int(token)
    except ValueError:
        return float(token)


def _to_operand(token):
    return _to_number(token) if _is_number(token) else token


def parse_ir_text(source):
    ir_program = []
    errors = []

    for lineno, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.upper().startswith("PRINT"):
            operand_text = line[5:].strip()
            if not operand_text:
                errors.append(
                    f'Line {lineno}: PRINT requires an operand, e.g. "PRINT t1"'
                )
                continue
            ir_program.append(("PRINT", _to_operand(operand_text)))
            continue

        if "=" not in line:
            errors.append(
                f'Line {lineno}: expected an assignment ("x = ...") or '
                f'"PRINT x", got: {line!r}'
            )
            continue

        dest_text, rhs_text = line.split("=", 1)
        dest = dest_text.strip()
        rhs_tokens = rhs_text.strip().split()

        if not dest.isidentifier():
            errors.append(
                f"Line {lineno}: {dest!r} is not a valid variable name"
            )
            continue

        if len(rhs_tokens) == 1:
            token = rhs_tokens[0]
            if _is_number(token):
                ir_program.append(("CONST", dest, _to_number(token)))
            else:
                ir_program.append(("COPY", dest, token))
        elif len(rhs_tokens) == 3 and rhs_tokens[1] in _BINOPS:
            src1, op, src2 = rhs_tokens
            ir_program.append(
                ("BINOP", op, dest, _to_operand(src1), _to_operand(src2))
            )
        else:
            errors.append(
                f"Line {lineno}: could not parse right-hand side {rhs_text.strip()!r}"
            )

    return ir_program, errors


st.set_page_config(
    page_title="Compiler Pass Optimizer",
    layout="wide",
)

st.markdown(
    f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {{
            font-family: 'IBM Plex Sans', sans-serif;
            color: {COLOR_TEXT};
        }}
        .stApp {{
            background-color: {COLOR_BG};
        }}
        code, pre, .stCodeBlock, .stCode {{
            font-family: 'IBM Plex Mono', monospace !important;
        }}
        h1, h2, h3 {{
            font-weight: 600;
            letter-spacing: -0.01em;
        }}
        .subtitle {{
            color: {COLOR_MUTED};
            font-size: 0.95rem;
            margin-top: -0.6rem;
            margin-bottom: 1.4rem;
        }}
        .pipeline-path {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 1.02rem;
            padding: 0.85rem 1rem;
            background-color: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            display: inline-block;
        }}
        .pipeline-step {{
            color: {COLOR_GA};
            font-weight: 500;
        }}
        .pipeline-arrow {{
            color: {COLOR_MUTED};
            margin: 0 0.35rem;
        }}
        .section-gap {{
            margin-top: 1.6rem;
        }}
        div[data-testid="stMetric"] {{
            background-color: {COLOR_PANEL};
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            padding: 0.7rem 0.9rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# Compiler Pass Optimizer")
st.markdown(
    '<div class="subtitle">Genetic algorithm search over compiler optimization pass orderings</div>',
    unsafe_allow_html=True,
)

st.markdown("### Program")

source_mode = st.radio(
    "Program source",
    options=["Standard benchmark", "Custom 3AC program"],
    horizontal=True,
    label_visibility="collapsed",
)

benchmarks = get_all_benchmarks()
ir_program = None
parse_errors = []

if source_mode == "Standard benchmark":
    bm_name = st.selectbox("Benchmark", options=list(benchmarks.keys()))
    ir_program = benchmarks[bm_name]
    st.code(format_ir(ir_program), language=None)
else:
    default_text = (
        "a = 10\n"
        "b = 20\n"
        "t1 = a + b\n"
        "c = a\n"
        "t2 = c * t1\n"
        "PRINT t2"
    )
    ir_text = st.text_area(
        "Custom 3AC program",
        value=default_text,
        height=220,
        label_visibility="collapsed",
        help=(
            "One instruction per line. Supported forms:\n"
            "  x = 10          (constant)\n"
            "  y = x           (copy)\n"
            "  t1 = a + b      (binary op: + - * /)\n"
            "  PRINT t1"
        ),
    )
    ir_program, parse_errors = parse_ir_text(ir_text)

    if parse_errors:
        for err in parse_errors:
            st.error(err)
        ir_program = None
    elif ir_program:
        is_valid, msg = validate_ir(ir_program)
        if not is_valid:
            st.error(f"IR validation failed: {msg}")
            ir_program = None

with st.expander("GA parameters", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        pop_size = st.slider(
            "Population size", min_value=10, max_value=50, value=30, step=5
        )
        generations = st.slider(
            "Generations", min_value=5, max_value=60, value=30, step=5
        )
    with col2:
        mutation_rate = st.slider(
            "Mutation rate",
            min_value=0.0,
            max_value=1.0,
            value=0.15,
            step=0.05,
        )
        crossover_rate = st.slider(
            "Crossover rate",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.05,
        )
    with col3:
        elitism_count = st.slider(
            "Elitism count", min_value=0, max_value=5, value=2, step=1
        )
        seed_input = st.text_input("Random seed (optional)", value="")

    include_baselines = st.checkbox(
        "Also run Random Search baseline for comparison (750 evaluations, slower)",
        value=True,
    )

run_clicked = st.button(
    "Run GA optimizer", type="primary", disabled=ir_program is None
)

if run_clicked and ir_program is not None:
    seed = int(seed_input) if seed_input.strip().isdigit() else None

    with st.spinner("Running genetic algorithm search..."):
        ga_result = run_genetic_algorithm(
            ir_program,
            pop_size=pop_size,
            generations=generations,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            elitism_count=elitism_count,
            seed=seed,
        )

    best = ga_result["best_solution"]
    best_pipeline_names = ga_result["best_pipeline_names"]
    optimized_ir = best["optimized_ir"]

    unoptimized_cost = compute_ir_cost(ir_program)
    cost_reduction = unoptimized_cost - best["cost"]
    pct_reduction = (
        (cost_reduction / unoptimized_cost) * 100
        if unoptimized_cost > 0
        else 0.0
    )

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown("### Best discovered pipeline")
    pipeline_html = '<span class="pipeline-arrow">&rarr;</span>'.join(
        f'<span class="pipeline-step">{name}</span>'
        for name in best_pipeline_names
    )
    st.markdown(
        f'<div class="pipeline-path">{pipeline_html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown("### Original vs. optimized IR")
    ir_col1, ir_col2 = st.columns(2)
    with ir_col1:
        st.markdown("**Original**")
        st.code(format_ir(ir_program), language=None)
    with ir_col2:
        st.markdown("**Optimized**")
        st.code(format_ir(optimized_ir), language=None)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric(
        "Cost", f"{unoptimized_cost} \u2192 {best['cost']}", f"-{cost_reduction}"
    )
    metric_col2.metric("Reduction", f"{pct_reduction:.1f}%")
    metric_col3.metric(
        "Instructions", f"{len(ir_program)} \u2192 {len(optimized_ir)}"
    )
    metric_col4.metric("Best fitness", f"{best['fitness']:.2f}")

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    st.markdown("### GA convergence")
    history_df = pd.DataFrame(ga_result["history"])
    convergence_long = history_df.melt(
        id_vars=["generation"],
        value_vars=["best_fitness", "avg_fitness"],
        var_name="series",
        value_name="fitness",
    )
    convergence_long["series"] = convergence_long["series"].map(
        {"best_fitness": "Best fitness", "avg_fitness": "Average fitness"}
    )
    convergence_chart = (
        alt.Chart(convergence_long)
        .mark_line(strokeWidth=2.2)
        .encode(
            x=alt.X("generation:Q", title="Generation"),
            y=alt.Y("fitness:Q", title="Fitness"),
            color=alt.Color(
                "series:N",
                title=None,
                scale=alt.Scale(
                    domain=["Best fitness", "Average fitness"],
                    range=[COLOR_BEST_FIT, COLOR_AVG_FIT],
                ),
            ),
            strokeDash=alt.condition(
                "datum.series == 'Average fitness'",
                alt.value([5, 4]),
                alt.value([1, 0]),
            ),
        )
        .properties(height=300)
        .configure_axis(grid=True, gridOpacity=0.25)
        .configure_view(strokeWidth=0)
    )
    st.altair_chart(convergence_chart, use_container_width=True)

    if include_baselines:
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        st.markdown("### Baseline comparison")

        with st.spinner("Running baseline comparisons..."):
            fixed_result = evaluate_pipeline_fitness(
                ir_program, FIXED_PIPELINE
            )
            random_result = run_random_search(
                ir_program, num_evaluations=750, seed=42
            )

        baseline_df = pd.DataFrame(
            [
                {"Method": "O0 (unoptimized)", "Cost": unoptimized_cost},
                {"Method": "Fixed pipeline", "Cost": fixed_result["cost"]},
                {"Method": "Random search", "Cost": random_result["cost"]},
                {"Method": "GA", "Cost": best["cost"]},
            ]
        )
        baseline_order = [
            "O0 (unoptimized)",
            "Fixed pipeline",
            "Random search",
            "GA",
        ]
        baseline_chart = (
            alt.Chart(baseline_df)
            .mark_bar()
            .encode(
                x=alt.X("Method:N", sort=baseline_order, title=None),
                y=alt.Y("Cost:Q", title="Estimated cost"),
                color=alt.Color(
                    "Method:N",
                    legend=None,
                    scale=alt.Scale(
                        domain=baseline_order,
                        range=[COLOR_O0, COLOR_FIXED, COLOR_RANDOM, COLOR_GA],
                    ),
                ),
            )
            .properties(height=280)
            .configure_axis(grid=True, gridOpacity=0.25)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(baseline_chart, use_container_width=True)

        st.caption(
            f"Fixed pipeline: {' \u2192 '.join(FIXED_PIPELINE)}  |  "
            f"Random search evaluated 750 random orderings."
        )
elif ir_program is None and source_mode == "Custom 3AC program" and not parse_errors:
    st.info("Enter a 3AC program above, then run the optimizer.")