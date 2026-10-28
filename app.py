"""Compiler Studio — multi-page Streamlit interface for GA-based compiler optimization."""
import altair as alt
import pandas as pd
import streamlit as st

from ir import validate_ir, format_ir
from cost_model import compute_ir_cost, evaluate_pipeline_fitness
from ga.engine import run_genetic_algorithm
from benchmarks import get_all_benchmarks
from run_experiments import FIXED_PIPELINE, run_random_search

st.set_page_config(page_title="Compiler Studio | GA Optimizer", page_icon="⌘", layout="wide", initial_sidebar_state="expanded")

# Premium, restrained compiler-lab design system.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#f5f7f6;--ink:#152b2c;--muted:#6c7c7b;--line:#dce5e1;--green:#087f63;--mint:#e4f5ed;--dark:#102d2d;}
html,body,[class*="css"]{font-family:'Manrope',sans-serif;color:var(--ink)} .stApp{background:var(--bg)}
[data-testid="stHeader"]{background:rgba(245,247,246,.94)} .block-container{max-width:1450px;padding-top:1.5rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#102d2d;border-right:1px solid #214746} [data-testid="stSidebar"] *{color:#e6f0ec}
[data-testid="stSidebar"] [data-testid="stRadio"] label{padding:.45rem .2rem}
h1,h2,h3{letter-spacing:-.04em;color:var(--ink)} h1{font-weight:800} h2{font-weight:800;font-size:1.6rem}
.hero{background:linear-gradient(115deg,#102d2d 0%,#174842 100%);color:white;padding:2rem 2.15rem;border-radius:20px;margin-bottom:1.5rem;position:relative;overflow:hidden;border:1px solid #24534c;box-shadow:0 12px 35px #153e3215}
.hero:after{content:'⌘';position:absolute;right:4%;top:-42px;font-size:12rem;line-height:1;color:#ffffff0b;font-weight:800}
.eyebrow{font:500 .7rem 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.15em;color:#9be0c2;margin-bottom:.7rem}
.hero h1{font-size:clamp(2rem,4vw,3.15rem);line-height:1.06;color:white;margin:0}.hero p{color:#d1e3dc;max-width:760px;line-height:1.75;margin:.8rem 0 0;font-size:.98rem}
.hero-tag{display:inline-block;border:1px solid #4e8172;border-radius:99px;padding:.4rem .7rem;color:#d6f6e8;font:500 .68rem 'DM Mono',monospace;margin-top:1.1rem}
.kicker{font:500 .68rem 'DM Mono',monospace;color:var(--green);letter-spacing:.15em;text-transform:uppercase;margin:1.2rem 0 .4rem}
.subtle{color:var(--muted);font-size:.9rem;line-height:1.65;margin-top:-.3rem;margin-bottom:1rem}
.card{background:white;border:1px solid var(--line);border-radius:15px;padding:1.1rem 1.2rem;box-shadow:0 3px 12px #183e2b06;height:100%}
.card-label{font:500 .68rem 'DM Mono',monospace;color:var(--muted);letter-spacing:.09em;text-transform:uppercase;margin-bottom:.55rem}
.card-value{font-size:1.85rem;font-weight:800;letter-spacing:-.05em;color:var(--ink)}.card-note{font-size:.78rem;color:var(--muted);margin-top:.25rem}
.pass-card{background:#fff;border:1px solid var(--line);border-radius:13px;padding:1rem 1.05rem;margin-bottom:.6rem}.pass-code{font:500 .75rem 'DM Mono',monospace;color:var(--green);background:var(--mint);border-radius:6px;padding:.3rem .45rem;display:inline-block;margin-bottom:.55rem}.pass-card h4{margin:.1rem 0 .4rem;font-size:1rem}.pass-card p{color:var(--muted);font-size:.84rem;line-height:1.55;margin:0}
.pipeline{display:flex;gap:.5rem;flex-wrap:wrap;background:#eaf2ee;padding:1rem;border:1px solid #d7e4dc;border-radius:14px}.pipeline-item{background:#fff;border:1px solid #d7e4dc;border-top:3px solid var(--green);padding:.75rem .85rem;border-radius:9px;min-width:135px;flex:1}.pipeline-num{font:500 .68rem 'DM Mono',monospace;color:var(--green)}.pipeline-name{font-size:.85rem;font-weight:800;margin-top:.25rem}.pipeline-desc{font-size:.72rem;color:var(--muted);margin-top:.2rem}
div[data-testid="stButton"]>button{border-radius:9px;min-height:2.7rem;font-weight:700;border:1px solid #cadbd3}div[data-testid="stButton"]>button[kind="primary"]{background:var(--green);border-color:var(--green);color:#fff}div[data-testid="stButton"]>button[kind="primary"]:hover{background:#06664f;border-color:#06664f}
textarea,code,pre{font-family:'DM Mono',monospace!important}div[data-testid="stTextArea"] textarea{background:#fbfdfc;border:1px solid var(--line);border-radius:9px;line-height:1.7}
div[data-testid="stSelectbox"] div[data-baseweb="select"]>div,div[data-testid="stTextInput"] input{background:white;border-color:var(--line);border-radius:8px}
div[data-testid="stExpander"]{background:#fff;border:1px solid var(--line);border-radius:11px}
div[data-testid="stMetric"]{background:white;border:1px solid var(--line);border-radius:12px;padding:.8rem}
hr{border-color:var(--line)}.footer{padding-top:1.5rem;margin-top:2rem;border-top:1px solid var(--line);font-size:.76rem;color:var(--muted)}
@media(max-width:750px){.hero{padding:1.35rem}.hero:after{display:none}.pipeline-item{min-width:100%}}
</style>
""", unsafe_allow_html=True)

PASSES = [
    ("CP", "Constant Propagation", "Replace variables with known constant values to simplify downstream instructions.", "x = 12; y = x + 2 → y = 14"),
    ("CF", "Constant Folding", "Evaluate arithmetic expressions whose operands are compile-time constants.", "t1 = 4 * 5 → t1 = 20"),
    ("CopyP", "Copy Propagation", "Substitute copied variables with their original source where safe.", "b = a; c = b + 1 → c = a + 1"),
    ("CSE", "Common Subexpression Elimination", "Reuse equivalent expressions instead of calculating them repeatedly.", "u = a + b; v = a + b → v = u"),
    ("AS", "Algebraic Simplification", "Apply identities such as x + 0, x * 1, and x * 0.", "t = x * 1 → t = x"),
    ("DCE", "Dead Code Elimination", "Remove assignments whose results are never used and have no observable effect.", "unused = a + b → removed"),
]

def hero(title, subtitle, tag="COMPILER STUDIO / RESEARCH LAB"):
    st.markdown(f'<div class="hero"><div class="eyebrow">{tag}</div><h1>{title}</h1><p>{subtitle}</p><span class="hero-tag">3AC · GENETIC ALGORITHM · STATIC COST MODEL</span></div>', unsafe_allow_html=True)

def metric(label, value, note):
    st.markdown(f'<div class="card"><div class="card-label">{label}</div><div class="card-value">{value}</div><div class="card-note">{note}</div></div>', unsafe_allow_html=True)

def pipeline_view(names):
    full={p[0]:p[1] for p in PASSES}
    html=''.join(f'<div class="pipeline-item"><div class="pipeline-num">PASS {i:02d}</div><div class="pipeline-name">{n}</div><div class="pipeline-desc">{full.get(n,n)}</div></div>' for i,n in enumerate(names,1))
    st.markdown(f'<div class="pipeline">{html}</div>',unsafe_allow_html=True)

def parse_ir_text(source):
    program=[]; errors=[]
    for lineno, raw in enumerate(source.splitlines(),1):
        line=raw.strip()
        if not line or line.startswith('#'): continue
        if line.upper().startswith('PRINT'):
            operand=line[5:].strip()
            if not operand: errors.append(f'Line {lineno}: PRINT requires an operand.'); continue
            program.append(('PRINT', _operand(operand))); continue
        if '=' not in line: errors.append(f'Line {lineno}: expected assignment or PRINT.'); continue
        dest,rhs=line.split('=',1); dest=dest.strip(); tokens=rhs.strip().split()
        if not dest.isidentifier(): errors.append(f'Line {lineno}: {dest!r} is not a valid variable name.'); continue
        if len(tokens)==1:
            t=tokens[0]; program.append(('CONST',dest,_number(t)) if _is_number(t) else ('COPY',dest,t))
        elif len(tokens)==3 and tokens[1] in {'+','-','*','/'}: program.append(('BINOP',tokens[1],dest,_operand(tokens[0]),_operand(tokens[2])))
        else: errors.append(f'Line {lineno}: could not parse expression {rhs.strip()!r}.')
    return program,errors

def _is_number(x):
    try: float(x); return True
    except (ValueError,TypeError): return False
def _number(x):
    n=float(x); return int(n) if n.is_integer() else n
def _operand(x): return _number(x) if _is_number(x) else x

with st.sidebar:
    st.markdown('<div style="padding:.5rem 0 1.25rem"><div style="font:500 .68rem DM Mono,monospace;letter-spacing:.15em;color:#8bd8b7">OPTIMIZATION WORKSPACE</div><div style="font-size:1.45rem;font-weight:800;color:white;margin-top:.4rem">⌘ Compiler Studio</div><div style="color:#a9c4ba;font-size:.78rem;margin-top:.25rem">Genetic algorithm research toolkit</div></div>',unsafe_allow_html=True)
    page=st.radio("WORKSPACE",["Overview","Optimize IR","Optimization passes","Benchmarks","Methodology"],label_visibility="visible")
    st.markdown('<div style="margin-top:2rem;border-top:1px solid #31534c;padding-top:1rem;color:#a9c4ba;font-size:.76rem;line-height:1.8">PROJECT STATUS<br><span style="color:#9be0c2">●</span> Local optimization engine<br><span style="color:#9be0c2">●</span> Six compiler passes<br><span style="color:#9be0c2">●</span> Reproducible search seed</div>',unsafe_allow_html=True)

if page == "Overview":
    hero("Find a better order.\nBuild a smarter compiler.","A hands-on environment for exploring the compiler phase-ordering problem. Feed in three-address code, evolve optimization pipelines, and compare the resulting instruction-cost estimates.")
    bms=get_all_benchmarks()
    c1,c2,c3,c4=st.columns(4,gap="medium")
    with c1: metric("Optimization passes","06","Composable compiler transformations")
    with c2: metric("Built-in benchmarks",f"{len(bms):02d}","Programs with different optimization patterns")
    with c3: metric("Search strategy","GA","Selection · crossover · mutation")
    with c4: metric("Cost model","Static","Instruction-weighted estimate")
    st.markdown('<div class="kicker">WORKFLOW</div>',unsafe_allow_html=True); st.header("From source IR to an evolved pipeline")
    cols=st.columns(4,gap="medium")
    steps=[("01","Choose a program","Start from a benchmark or enter custom three-address code."),("02","Configure the search","Set population, generations, crossover, mutation and seed."),("03","Evolve pass orderings","The genetic algorithm searches candidate permutations."),("04","Inspect the outcome","Compare IR, cost, convergence and baseline methods.")]
    for col,(num,title,desc) in zip(cols,steps):
        with col: st.markdown(f'<div class="card"><div class="card-label">STEP {num}</div><h3 style="font-size:1.08rem;margin:.2rem 0 .5rem">{title}</h3><div style="font-size:.84rem;color:#6c7c7b;line-height:1.6">{desc}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="kicker">QUICK START</div>',unsafe_allow_html=True); st.header("Ready to run your first experiment?")
    st.write("Open **Optimize IR** to choose a benchmark, configure the search and run an optimization. Results remain available in this session as you explore other pages.")
    if st.button("Open optimization workspace →",type="primary"): st.session_state["navigate_optimize"]=True; st.rerun()
    st.markdown('<div class="footer">Compiler Studio · Genetic Algorithm-Based Compiler Optimization Pass Ordering<br>Research and educational use. Reported improvements are static cost-model estimates, not measured execution-time speedups.</div>',unsafe_allow_html=True)

elif page == "Optimize IR":
    hero("Optimization workspace","Configure a search, run the optimizer, and inspect the best pipeline discovered for your intermediate representation.","WORKSPACE / EXPERIMENT RUNNER")
    benchmarks=get_all_benchmarks()
    with st.container(border=True):
        st.markdown('<div class="kicker">01 / INPUT</div>',unsafe_allow_html=True); st.subheader("Program and search configuration")
        left,right=st.columns([1.1,.9],gap="large")
        with left:
            mode=st.radio("Program source",["Benchmark program","Custom 3AC"],horizontal=True)
            if mode=="Benchmark program":
                bm=st.selectbox("Select benchmark",list(benchmarks.keys()),format_func=lambda x:x.replace('_',' '))
                ir=benchmarks[bm]; st.code(format_ir(ir),language=None); errors=[]
            else:
                source=st.text_area("Three-address code",value="a = 10\nb = 20\nt1 = a + b\nc = a\nt2 = c * t1\nPRINT t2",height=220,help="One instruction per line. Supports constants, copies, binary arithmetic and PRINT.")
                ir,errors=parse_ir_text(source)
                for error in errors: st.error(error)
                if not errors and ir:
                    valid,msg=validate_ir(ir)
                    if not valid: st.error(f"IR validation failed: {msg}"); ir=None
                elif not ir: ir=None
            st.caption("The optimizer transforms an intermediate representation; it does not compile or execute native machine code.")
        with right:
            st.markdown("#### Genetic algorithm settings")
            pop=st.slider("Population size",10,100,30,5)
            gens=st.slider("Generations",5,100,30,5)
            mut=st.slider("Mutation rate",0.0,1.0,.15,.05)
            cross=st.slider("Crossover rate",0.0,1.0,.80,.05)
            elite=st.slider("Elitism count",0,5,2)
            seed_text=st.text_input("Random seed (optional)",placeholder="e.g. 42")
            baselines=st.checkbox("Compare fixed pipeline and random search",value=True)
            st.caption("Random-search baseline evaluates 750 candidate orderings and may take longer.")
        run=st.button("Run optimization  →",type="primary",use_container_width=True,disabled=ir is None or bool(errors))
    if run:
        seed=int(seed_text) if seed_text.strip().isdigit() else None
        with st.spinner("Evolving candidate optimization pipelines…"):
            result=run_genetic_algorithm(ir,pop_size=pop,generations=gens,crossover_rate=cross,mutation_rate=mut,elitism_count=elite,seed=seed)
            fixed=evaluate_pipeline_fitness(ir,FIXED_PIPELINE) if baselines else None
            random_result=run_random_search(ir,num_evaluations=750,seed=42) if baselines else None
        st.session_state["last_result"]={"ga":result,"ir":ir,"fixed":fixed,"random":random_result,"benchmark":bm if mode=="Benchmark program" else "Custom program","seed":seed}
    saved=st.session_state.get("last_result")
    if saved:
        result=saved["ga"]; original=saved["ir"]; best=result["best_solution"]; optimized=best["optimized_ir"]
        original_cost=compute_ir_cost(original); reduction=original_cost-best["cost"]; pct=100*reduction/original_cost if original_cost else 0
        st.markdown('<div class="kicker">02 / RESULTS</div>',unsafe_allow_html=True); st.header("Best discovered pipeline")
        st.caption(f"Program: {saved['benchmark']} · Seed: {saved['seed'] if saved['seed'] is not None else 'not fixed'} · Passes apply from left to right.")
        pipeline_view(result["best_pipeline_names"])
        m=st.columns(4,gap="medium")
        with m[0]: metric("Estimated cost",f"{original_cost} → {best['cost']}",f"{reduction:+g} cost units")
        with m[1]: metric("Cost reduction",f"{pct:.1f}%","Relative to original IR")
        with m[2]: metric("Instruction count",f"{len(original)} → {len(optimized)}","Before → after")
        with m[3]: metric("Best fitness",f"{best['fitness']:.3f}","Higher is better")
        a,b=st.columns(2,gap="medium")
        with a:
            st.markdown("#### Original IR"); st.code(format_ir(original),language=None)
        with b:
            st.markdown("#### Optimized IR"); st.code(format_ir(optimized),language=None)
        st.markdown("#### Search convergence"); st.caption("Best fitness tracks the strongest candidate found so far; average fitness describes the population.")
        hist=pd.DataFrame(result["history"]); long=hist.melt(id_vars=["generation"],value_vars=["best_fitness","avg_fitness"],var_name="series",value_name="fitness")
        long["series"]=long["series"].map({"best_fitness":"Best fitness","avg_fitness":"Average fitness"})
        chart=alt.Chart(long).mark_line(point=True,strokeWidth=2.5).encode(x=alt.X("generation:Q",title="Generation"),y=alt.Y("fitness:Q",title="Fitness",scale=alt.Scale(zero=False)),color=alt.Color("series:N",scale=alt.Scale(domain=["Best fitness","Average fitness"],range=["#087f63","#c47c46"]),title=None),tooltip=["generation:Q","series:N",alt.Tooltip("fitness:Q",format=".3f")]).properties(height=300)
        st.altair_chart(chart,use_container_width=True)
        if saved["fixed"] is not None:
            fixed=saved["fixed"]; rnd=saved["random"]
            df=pd.DataFrame([{"Method":"Unoptimized","Estimated cost":original_cost},{"Method":"Fixed pipeline","Estimated cost":fixed["cost"]},{"Method":"Random search","Estimated cost":rnd["cost"]},{"Method":"Genetic algorithm","Estimated cost":best["cost"]}])
            st.markdown("#### Baseline comparison"); st.caption("Lower estimated instruction cost is better; every method uses the same cost model.")
            bars=alt.Chart(df).mark_bar(cornerRadiusTopLeft=5,cornerRadiusTopRight=5).encode(x=alt.X("Method:N",sort=["Unoptimized","Fixed pipeline","Random search","Genetic algorithm"],axis=alt.Axis(labelAngle=0),title=None),y=alt.Y("Estimated cost:Q",scale=alt.Scale(zero=True)),color=alt.Color("Method:N",scale=alt.Scale(domain=["Unoptimized","Fixed pipeline","Random search","Genetic algorithm"],range=["#a8b8b0","#5485a0","#c99b47","#087f63"]),legend=None),tooltip=["Method","Estimated cost"]).properties(height=300)
            st.altair_chart(bars,use_container_width=True)
            st.caption(f"Fixed pipeline order: {' → '.join(FIXED_PIPELINE)}. Random search evaluated 750 orderings.")
        st.download_button("Download optimized IR (.txt)",format_ir(optimized),file_name="optimized_ir.txt",mime="text/plain")
    else:
        st.info("Configure your program and run an experiment to see the pipeline, before/after IR, convergence and cost comparison here.")

elif page == "Optimization passes":
    hero("The optimization toolkit","Six classical compiler transformations form the building blocks of the search space. Their ordering can change which simplifications become possible.","REFERENCE / PASS LIBRARY")
    st.markdown('<div class="kicker">PASS CATALOG</div>',unsafe_allow_html=True); st.header("Meet the transformations")
    cols=st.columns(3,gap="medium")
    for i,p in enumerate(PASSES):
        with cols[i%3]:
            st.markdown(f'<div class="pass-card"><span class="pass-code">{p[0]}</span><h4>{p[1]}</h4><p>{p[2]}</p><div style="margin-top:.8rem;background:#f2f7f4;border-radius:7px;padding:.6rem;font: .75rem DM Mono,monospace;color:#28564a">{p[3]}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="kicker">WHY ORDER MATTERS</div>',unsafe_allow_html=True); st.header("Optimization is not always commutative")
    st.write("One pass can expose opportunities for another. Constant propagation may turn an expression into constants; constant folding can then evaluate it. Dead-code elimination may only become effective after earlier passes simplify or remove uses. A different order can therefore produce a different final IR and cost.")
    st.info("The genetic algorithm searches permutations of the available passes. The best order depends on the input program and the project's static cost model.")

elif page == "Benchmarks":
    hero("Benchmark library","Explore the built-in three-address-code programs designed to exercise different optimization patterns before running your own experiment.","REFERENCE / PROGRAM SUITE")
    bms=get_all_benchmarks(); st.markdown('<div class="kicker">PROGRAM SUITE</div>',unsafe_allow_html=True); st.header(f"{len(bms)} built-in benchmarks")
    descriptions={"BM1_Arithmetic_Intensity":"Arithmetic expressions and identities that expose folding and simplification opportunities.","BM2_Redundant_Expressions":"Repeated and commuted expressions that test common-subexpression elimination.","BM3_Dead_Code_Heavy":"Unused intermediate values mixed with a small observable result.","BM4_Deep_Copy_Chain":"A chain of copies that tests copy propagation and downstream simplification.","BM5_Algebraic_Identities":"Zero and one identities that expose algebraic simplification and dead assignments."}
    for name,program in bms.items():
        with st.expander(f"{name.replace('_',' ')}  ·  {len(program)} instructions",expanded=False):
            st.write(descriptions.get(name,"A compiler optimization benchmark.")); st.code(format_ir(program),language=None)
            st.caption(f"Estimated starting cost: {compute_ir_cost(program)} cost units")
    st.markdown('<div class="kicker">CUSTOM INPUT</div>',unsafe_allow_html=True); st.write("Need a different workload? The **Optimize IR** page accepts custom 3AC with assignments, numeric constants, binary `+ - * /` expressions, copies, and `PRINT` statements.")

else:
    hero("How the optimizer works","A transparent overview of the search strategy, fitness function and evaluation limits behind the results.","REFERENCE / METHODOLOGY")
    st.markdown('<div class="kicker">01 / REPRESENTATION</div>',unsafe_allow_html=True); st.header("Three-address code")
    st.write("Programs are represented as a sequence of typed intermediate-representation instructions: constants, copies, binary operations and PRINT statements. Each candidate pipeline applies the selected optimization passes in a specific order.")
    st.markdown('<div class="kicker">02 / SEARCH</div>',unsafe_allow_html=True); st.header("Genetic algorithm lifecycle")
    cols=st.columns(4,gap="medium")
    for col,(title,desc) in zip(cols,[("Initialize","Create a population of candidate pass-order permutations."),("Evaluate","Apply each pipeline and score its resulting IR."),("Select & recombine","Tournament selection and order crossover create offspring."),("Mutate & preserve","Swap mutation explores new orders; elitism retains strong candidates.")]):
        with col: st.markdown(f'<div class="card"><h3 style="font-size:1rem">{title}</h3><p style="font-size:.83rem;color:#6c7c7b;line-height:1.6">{desc}</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="kicker">03 / FITNESS</div>',unsafe_allow_html=True); st.header("Static instruction-cost model")
    st.write("The project assigns weighted costs to IR instruction types and evaluates a candidate using the cost of its optimized output. The genetic algorithm maximizes fitness derived from that cost. This is a lightweight proxy for comparing transformations, not a hardware performance model.")
    cost_df=pd.DataFrame([{"Instruction":"CONST","Meaning":"Constant assignment","Cost":1},{"Instruction":"COPY","Meaning":"Copy assignment","Cost":1},{"Instruction":"BINOP","Meaning":"Binary arithmetic","Cost":3},{"Instruction":"PRINT","Meaning":"Observable output","Cost":2}])
    st.dataframe(cost_df,use_container_width=True,hide_index=True)
    st.markdown('<div class="kicker">04 / INTERPRETATION</div>',unsafe_allow_html=True); st.header("What results do — and do not — mean")
    st.success("A lower estimated cost means the resulting IR scores better under this project's cost model. Compare methods on the same program and cost model for a fair experiment.")
    st.warning("A cost reduction is not the same as a measured runtime speedup. Actual execution time can depend on target architecture, compiler backend, register allocation, memory behavior and workload. Use hardware benchmarks to validate performance claims.")

if page != "Overview":
    st.markdown('<div class="footer">Compiler Studio · GA-Based Compiler Optimization Pass Ordering · Results are based on a static instruction-cost model.</div>',unsafe_allow_html=True)
