from ir import validate_ir
from passes import PASS_NAMES, PASS_REGISTRY


def resolve_pass_name(pass_id):
    if isinstance(pass_id, int):
        if 0 <= pass_id < len(PASS_NAMES):
            return PASS_NAMES[pass_id]
        raise ValueError(
            f"Pass index {pass_id} out of bounds (0 to {len(PASS_NAMES) - 1})"
        )
    if isinstance(pass_id, str):
        if pass_id in PASS_REGISTRY:
            return pass_id
        raise ValueError(
            f"Unknown pass '{pass_id}'. Valid passes: {PASS_NAMES}"
        )
    raise TypeError(
        f"Pass identifier must be int or str, got {type(pass_id).__name__}"
    )


def execute_pipeline(ir, pipeline, trace=False):
    is_valid, msg = validate_ir(ir)
    if not is_valid:
        raise ValueError(f"Input IR validation failed: {msg}")

    current_ir = list(ir)

    for step_num, pass_id in enumerate(pipeline, start=1):
        pass_name = resolve_pass_name(pass_id)
        pass_fn = PASS_REGISTRY[pass_name]

        current_ir = pass_fn(current_ir)

        is_valid, msg = validate_ir(current_ir)
        if not is_valid:
            raise RuntimeError(
                f"IR corrupted after pass {step_num} ({pass_name}): {msg}"
            )

        if trace:
            print(f"Step {step_num}: Applied {pass_name}")

    return current_ir