from ir import validate_ir
from pipeline import execute_pipeline

INSTRUCTION_COSTS = {
    "INPUT": 1,
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


def evaluate_pipeline_fitness(ir, pipeline, input_cases=None):
    """Evaluate a candidate and reject outputs failing finite semantic checks.

    This is translation validation on supplied test cases, not a formal proof.
    """
    from semantics import preserves_outputs
    optimized_ir = execute_pipeline(ir, pipeline)
    if input_cases is None:
        input_count = sum(1 for inst in ir if inst[0] == "INPUT")
        input_cases = (tuple([v] * input_count) for v in (0, 1, -3, 7, 13)) if input_count else ((),)
        input_cases = tuple(input_cases)
    valid, detail = preserves_outputs(ir, optimized_ir, input_cases)
    cost = compute_ir_cost(optimized_ir) if valid else float("inf")
    fitness = compute_fitness(cost) if valid else 0.0
    return {"optimized_ir": optimized_ir, "cost": cost, "fitness": fitness,
            "semantically_valid": valid, "validation_detail": detail}
