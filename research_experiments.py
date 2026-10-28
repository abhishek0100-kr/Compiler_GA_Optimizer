"""Reproducible extended experiments for the project/reviewer action items.

Runs 30 GA seeds, variable-length GA seeds, a fixed-point baseline, pass ablation,
weight sensitivity, and exhaustive 720-ordering distributions for the six-pass mode.
All costs are static model units, not measured runtime.
"""
import csv, itertools, json, statistics, random
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from benchmarks import get_all_benchmarks
from passes import PASS_NAMES
from cost_model import compute_ir_cost, evaluate_pipeline_fitness, INSTRUCTION_COSTS
from pipeline_modes import execute_with_mode, ablation_pipelines
from ga.engine import run_genetic_algorithm
from ga.variable_engine import run_variable_length_ga
from ga.variable_operators import random_sequence
from pipeline import execute_pipeline
from semantics import preserves_outputs
from semantics import preserves_outputs

ROOT=Path(__file__).resolve().parent
FIXED_PIPELINE=list(PASS_NAMES)
SEEDS=list(range(20))
def cases_for(program):
    if not any(i[0]=='INPUT' for i in program): return ((),)
    count=sum(i[0]=='INPUT' for i in program)
    cases=[tuple([0]*count),tuple([1]*count),tuple([-3,7][:count]),tuple([2,5][:count]),tuple([11,-4][:count])]
    return tuple(cases)
def evaluate(ir,pipeline,mode='single',weights=None,cases=None):
    optimized,meta=execute_with_mode(ir,pipeline,mode)
    ok,detail=preserves_outputs(ir,optimized,cases or cases_for(ir))
    costs=weights or INSTRUCTION_COSTS
    cost=sum(costs.get(inst[0],1) for inst in optimized) if ok else float('inf')
    return {'cost':cost,'optimized_ir':optimized,'valid':ok,'detail':detail,**meta}
def exhaustive_orderings(ir,mode='single',weights=None):
    rows=[]
    for order in itertools.permutations(PASS_NAMES):
        r=evaluate(ir,order,mode,weights)
        rows.append({'pipeline':' -> '.join(order),'cost':r['cost'],'valid':r['valid']})
    return rows

def run_all(seeds=SEEDS):
    out=ROOT/'results'; out.mkdir(exist_ok=True)
    benchmark_rows=[]; seed_rows=[]; variable_seed_rows=[]; histogram_rows=[]; ablation_rows=[]; sensitivity_rows=[]; convergence_rows=[]
    bms=get_all_benchmarks()
    for name,ir in bms.items():
        cases=cases_for(ir); original=compute_ir_cost(ir)
        fixed_single=evaluate(ir,FIXED_PIPELINE,'single',cases=cases)
        fixed_fp=evaluate(ir,FIXED_PIPELINE,'fixed-point',cases=cases)
        exact=exhaustive_orderings(ir,'single') if len(PASS_NAMES)==6 else []
        valid_costs=[x['cost'] for x in exact if x['valid'] and x['cost']!=float('inf')]
        optimum=min(valid_costs) if valid_costs else fixed_single['cost']
        for row in exact: histogram_rows.append({'benchmark':name,**row})
        ga_costs=[]; ga_gens=[]
        for seed in seeds:
            ga=run_genetic_algorithm(ir,pop_size=25,generations=30,seed=seed,verbose=False)
            best=ga['best_solution']; first=next((h['generation'] for h in ga['history'] if h['best_cost']==optimum),None)
            seed_rows.append({'benchmark':name,'seed':seed,'best_cost':best['cost'],'exact_optimum':optimum,'optimality_gap':(best['cost']-optimum)/max(1,abs(optimum)),'first_generation_at_optimum':first,'pipeline':' -> '.join(ga['best_pipeline_names'])})
            ga_costs.append(best['cost']); ga_gens.append(first)
        variable_rows=[]; random_variable_rows=[]
        # Fair budget: 30 x 40 = 1,200 candidate evaluations for both GA and random search.
        for seed in seeds:
            vga=run_variable_length_ga(ir,input_cases=cases,pop_size=25,generations=30,seed=seed)
            vb=vga['best_solution']; variable_rows.append(vb['cost'])
            rng=random.Random(seed); random_best=float('inf')
            for _ in range(750):
                seq=[rng.randrange(len(PASS_NAMES)) for _ in range(rng.randint(1,12))]
                try:
                    candidate=execute_pipeline(ir,seq); valid,_=preserves_outputs(ir,candidate,cases)
                    c=compute_ir_cost(candidate) if valid else float('inf')
                except Exception: c=float('inf')
                if c<random_best: random_best=c
            random_variable_rows.append(random_best)
            first_known=next((h['generation'] for h in vga['history'] if h['best_cost']==vb['cost']),None)
            variable_seed_rows.append({'benchmark':name,'seed':seed,'ga_cost':vb['cost'],'random_search_cost_750_evals':random_best,'fixed_point_baseline_cost':fixed_fp['cost'],'ga_semantically_valid':vb['semantically_valid'],'ga_pipeline':' -> '.join(vga['best_pipeline_names']),'generations':30,'population':25,'candidate_evaluations':750,'first_generation_at_own_best':first_known})
            for h in vga['history']: convergence_rows.append({'benchmark':name,'seed':seed,**h})
        # Pass ablation on fixed point is a stronger comparator than one-shot arbitrary ordering.
        for variant,pipeline in ablation_pipelines(PASS_NAMES).items():
            r=evaluate(ir,pipeline,'fixed-point',cases=cases)
            ablation_rows.append({'benchmark':name,'variant':variant,'pipeline':' -> '.join(pipeline),'fixed_point_cost':r['cost'],'semantically_valid':r['valid']})
        # Weight sensitivity over all 720 permutations: report ranking correlation.
        baseline_costs=[]; candidate_irs=[]
        for order in itertools.permutations(PASS_NAMES):
            candidate,_meta=execute_with_mode(ir,order,'single')
            valid,_detail=preserves_outputs(ir,candidate,cases)
            candidate_irs.append(candidate if valid else None)
            baseline_costs.append(compute_ir_cost(candidate) if valid else float('inf'))
        baseline_series=pd.Series(baseline_costs)
        for opcode,base in INSTRUCTION_COSTS.items():
            for factor in (0.75,1.0,1.25):
                w=dict(INSTRUCTION_COSTS); w[opcode]=base*factor; costs=[]
                for candidate in candidate_irs:
                    costs.append(sum(w.get(inst[0],1) for inst in candidate) if candidate is not None else float('inf'))
                corr=baseline_series.rank(method='average').corr(pd.Series(costs).rank(method='average'))
                sensitivity_rows.append({'benchmark':name,'instruction':opcode,'factor':factor,'spearman_rank_correlation':corr,'best_ordering_cost_under_weights':min(costs)})
        benchmark_rows.append({'benchmark':name,'initial_cost':original,'fixed_single_cost':fixed_single['cost'],'fixed_point_cost':fixed_fp['cost'],'exact_single_pass_optimum':optimum,'ga_median_cost':statistics.median(ga_costs),'ga_success_rate':sum(c==optimum for c in ga_costs)/len(ga_costs),'median_optimality_gap':statistics.median([(c-optimum)/max(1,abs(optimum)) for c in ga_costs]),'median_first_generation_optimum':statistics.median([g for g in ga_gens if g is not None]) if any(g is not None for g in ga_gens) else None,'variable_length_ga_median_cost':statistics.median(variable_rows),'variable_random_750_eval_median_cost':statistics.median(random_variable_rows),'variable_ga_win_rate_vs_random':sum(g<r for g,r in zip(variable_rows,random_variable_rows))/len(seeds)})
    pd.DataFrame(benchmark_rows).to_csv(out/'benchmark_summary.csv',index=False)
    pd.DataFrame(seed_rows).to_csv(out/'ga_20_seed_results.csv',index=False)
    pd.DataFrame(variable_seed_rows).to_csv(out/'variable_ga_vs_random_20_seeds.csv',index=False)
    pd.DataFrame(histogram_rows).to_csv(out/'exhaustive_ordering_costs.csv',index=False)
    pd.DataFrame(ablation_rows).to_csv(out/'pass_ablation_fixed_point.csv',index=False)
    pd.DataFrame(sensitivity_rows).to_csv(out/'weight_sensitivity.csv',index=False)
    pd.DataFrame(convergence_rows).to_csv(out/'ga_convergence_by_seed.csv',index=False)
    make_figures(out,pd.DataFrame(histogram_rows),pd.DataFrame(convergence_rows))
    (out/'experiment_metadata.json').write_text(json.dumps({'seeds':seeds,'pass_names':PASS_NAMES,'cost_model':INSTRUCTION_COSTS,'warning':'Static cost model only; results are not measured runtime. Semantic checks use a finite test set and are not formal proof.'},indent=2))
    print('Wrote reproducible experiment artifacts to',out)
    print(pd.DataFrame(benchmark_rows).to_string(index=False))

def make_figures(out,hist,conv):
    # Architecture/workflow figure for the paper and presentation.
    fig,ax=plt.subplots(figsize=(12,2.8)); ax.axis('off')
    labels=['3AC input','Parse & validate','Candidate pass sequence','Apply passes','Semantic checks','Static cost','GA selection / variation','Best IR + report']
    xs=[.06,.18,.31,.43,.55,.67,.79,.93]
    for x,label in zip(xs,labels):
        ax.text(x,.55,label,ha='center',va='center',fontsize=8.5,
                bbox=dict(boxstyle='round,pad=.55',fc='#e7f3ed' if label in ('Semantic checks','Static cost') else '#f4f6f5',ec='#367565',lw=1.1),transform=ax.transAxes)
    for a,b in zip(xs[:-1],xs[1:]):
        ax.annotate('',xy=(b-.045,.55),xytext=(a+.045,.55),xycoords=ax.transAxes,textcoords=ax.transAxes,arrowprops=dict(arrowstyle='->',lw=1.1,color='#28564a'))
    ax.text(.73,.15,'Repeat candidate evaluation over generations',ha='center',fontsize=9,color='#28564a',transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(out/'architecture_workflow.png',dpi=180,bbox_inches='tight'); plt.close(fig)
    if not hist.empty:
        names=list(hist['benchmark'].unique())
        fig,axes=plt.subplots(len(names),1,figsize=(9,max(3,len(names)*2.1)),squeeze=False)
        for ax,name in zip(axes[:,0],names):
            vals=hist[(hist.benchmark==name)&(hist.valid==True)&(hist.cost<1e100)]['cost']
            ax.hist(vals,bins=min(25,max(5,len(vals.unique()))),edgecolor='white'); ax.set_title(name); ax.set_xlabel('Static cost'); ax.set_ylabel('Ordering count')
        fig.tight_layout(); fig.savefig(out/'ordering_cost_histograms.png',dpi=160); plt.close(fig)
    if not conv.empty:
        summary=conv.groupby(['benchmark','generation']).agg(best=('best_cost','mean'),std=('best_cost','std')).reset_index()
        fig,ax=plt.subplots(figsize=(10,5))
        for name,g in summary.groupby('benchmark'): ax.plot(g.generation,g.best,label=name)
        ax.set_xlabel('Generation'); ax.set_ylabel('Mean best static cost across seeds'); ax.set_title('Variable-length GA convergence across 20 seeds'); ax.legend(fontsize=7); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(out/'ga_convergence_20_seeds.png',dpi=160); plt.close(fig)
if __name__=='__main__': run_all()
