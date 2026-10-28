"""Variable-length GA with semantic validation integrated into candidate scoring."""
import random
from passes import PASS_NAMES
from cost_model import compute_ir_cost,compute_fitness
from pipeline import execute_pipeline
from semantics import preserves_outputs
from ga.variable_operators import initial_population,crossover,mutate

def run_variable_length_ga(ir_program,input_cases=((),),pop_size=40,generations=60,crossover_rate=.8,mutation_rate=.2,elitism_count=2,seed=None,max_len=12):
    if seed is not None: random.seed(seed)
    population=initial_population(pop_size); history=[]; best=None
    for gen in range(1,generations+1):
        scored=[]
        for chrom in population:
            try:
                optimized=execute_pipeline(ir_program,chrom)
                valid,detail=preserves_outputs(ir_program,optimized,input_cases)
                cost=compute_ir_cost(optimized) if valid else float('inf')
            except Exception as exc:
                optimized=list(ir_program); valid=False; detail=str(exc); cost=float('inf')
            scored.append({'chromosome':list(chrom),'optimized_ir':optimized,'cost':cost,'fitness':compute_fitness(cost) if valid else 0.0,'semantically_valid':valid,'validation_detail':detail})
        scored.sort(key=lambda x:(x['semantically_valid'],x['fitness']),reverse=True); cur=scored[0]
        if best is None or (cur['semantically_valid'] and (not best['semantically_valid'] or cur['fitness']>best['fitness'])): best=cur
        costs=[x['cost'] for x in scored if x['semantically_valid']]
        history.append({'generation':gen,'best_cost':cur['cost'] if cur['semantically_valid'] else None,'best_fitness':cur['fitness'],'avg_fitness':sum(x['fitness'] for x in scored)/len(scored),'avg_cost':sum(costs)/len(costs) if costs else None,'valid_candidates':len(costs)})
        elite_n=max(0,min(elitism_count,pop_size)); new=[list(x['chromosome']) for x in scored[:elite_n]]
        while len(new)<pop_size:
            p1=_tournament(scored); p2=_tournament(scored)
            child=crossover(p1,p2) if random.random()<crossover_rate else list(p1)
            new.append(mutate(child,mutation_rate)[:max_len])
        population=new
    names=[PASS_NAMES[i] for i in best['chromosome']]; best['pipeline_names']=names
    return {'best_solution':best,'best_pipeline_names':names,'history':history,'search_space_note':'Variable-length sequences; passes can be omitted or repeated; maximum length 12.'}

def _tournament(scored,k=3):
    selected=random.sample(scored,min(k,len(scored))); selected.sort(key=lambda x:(x['semantically_valid'],x['fitness']),reverse=True); return selected[0]['chromosome']
