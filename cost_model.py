from ir import validate_ir
from pipeline import execute_pipeline

INSTRUCTION_COSTS = {
    "CONST": 1,
    "COPY": 1,
    "BINOP": 3,
    "PRINT": 2,
}


def compute_instruction_cost(inst):
    opcode = inst[0]
    if opcode in INSTRUCTION_COSTS:
        return INSTRUCTION_COSTS[opcode]
    raise ValueError(f"Unknown opcode '{opcode}' encountered during cost evaluation")


def compute_ir_cost(ir):
    is_valid, msg = validate_ir(ir)
    if not is_valid:
        raise ValueError(f"IR validation failed: {msg}")

    total_cost = 0
    for inst in ir:
        total_cost += compute_instruction_cost(inst)
    return total_cost


def compute_fitness(cost):
    return round(1000.0 / (1.0 + cost), 4)


def evaluate_pipeline_fitness(ir, pipeline):
    optimized_ir = execute_pipeline(ir, pipeline)
    cost = compute_ir_cost(optimized_ir)
    fitness = compute_fitness(cost)
    return {
        "optimized_ir": optimized_ir,
        "cost": cost,
        "fitness": fitness,
    }