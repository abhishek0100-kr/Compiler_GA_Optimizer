"""Single-shot and fixed-point pipeline execution helpers."""
from pipeline import execute_pipeline

def execute_to_fixed_point(ir,pipeline,max_rounds=20):
    current=list(ir)
    for round_no in range(1,max_rounds+1):
        updated=execute_pipeline(current,pipeline)
        if updated==current: return updated,{"rounds":round_no,"converged":True}
        current=updated
    return current,{"rounds":max_rounds,"converged":False}

def execute_with_mode(ir,pipeline,mode='single',max_rounds=20):
    if mode=='single': return execute_pipeline(ir,pipeline),{"rounds":1,"converged":True}
    if mode=='fixed-point': return execute_to_fixed_point(ir,pipeline,max_rounds)
    raise ValueError("mode must be 'single' or 'fixed-point'")

def ablation_pipelines(pass_names):
    return {('all_passes' if omitted is None else 'without_'+omitted):
            list(pass_names) if omitted is None else [p for p in pass_names if p!=omitted]
            for omitted in [None,*pass_names]}
