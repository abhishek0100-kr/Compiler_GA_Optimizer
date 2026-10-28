import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from benchmarks import get_all_benchmarks
from ir import validate_ir, format_ir
from semantics import execute_ir, preserves_outputs
from pipeline_modes import execute_to_fixed_point
from passes import PASS_NAMES
from cost_model import compute_ir_cost, evaluate_pipeline_fitness
from ga.variable_engine import run_variable_length_ga

def test_input_ir_and_interpreter():
    ir=get_all_benchmarks()['BM6_Input_Arithmetic']
    assert validate_ir(ir)[0]
    assert execute_ir(ir,(2,3)) == [5]
    optimized,meta=execute_to_fixed_point(ir,PASS_NAMES)
    assert meta['converged']
    assert preserves_outputs(ir,optimized,((0,0),(1,2),(-3,7)))[0]
    assert compute_ir_cost(optimized) < compute_ir_cost(ir)

def test_semantics_in_fitness():
    ir=[('INPUT','x'),('BINOP','+','y','x',0),('PRINT','y')]
    result=evaluate_pipeline_fitness(ir,['AS','CP','CF','DCE'],input_cases=((0,),(1,),(-3,)))
    assert result['semantically_valid']
    assert result['cost'] < compute_ir_cost(ir)

def test_variable_length_ga():
    ir=get_all_benchmarks()['BM7_Input_Redundant_Computation']
    result=run_variable_length_ga(ir,input_cases=((0,0),(1,2),(-3,7)),pop_size=10,generations=3,seed=9)
    assert result['best_solution']['semantically_valid']
    assert 1 <= len(result['best_solution']['chromosome']) <= 12
    assert len(result['history'])==3

if __name__=='__main__':
    test_input_ir_and_interpreter(); test_semantics_in_fitness(); test_variable_length_ga()
    print('[PASS] Extended input, fixed-point, semantic validation and variable-length GA tests')
