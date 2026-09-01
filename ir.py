VALID_OPCODES = {"CONST", "COPY", "BINOP", "PRINT"}
VALID_BINOPS = {"+", "-", "*", "/"}


def is_operand(val):
    if isinstance(val, (int, float)):
        return True
    if isinstance(val, str) and len(val.strip()) > 0:
        return True
    return False


def is_var_name(val):
    return isinstance(val, str) and len(val.strip()) > 0


def validate_instruction(inst):
    if not isinstance(inst, tuple):
        return False, f"Instruction must be a tuple, got {type(inst).__name__}: {inst}"

    if len(inst) == 0:
        return False, "Instruction tuple cannot be empty"

    opcode = inst[0]
    if opcode not in VALID_OPCODES:
        return False, f"Unknown opcode '{opcode}'. Valid opcodes: {sorted(list(VALID_OPCODES))}"

    if opcode == "CONST":
        if len(inst) != 3:
            return False, f"CONST requires 3 elements ('CONST', dest, value), got {len(inst)}: {inst}"
        dest, value = inst[1], inst[2]
        if not is_var_name(dest):
            return False, f"CONST dest must be a non-empty string variable name, got: {dest}"
        if not isinstance(value, (int, float)):
            return False, f"CONST value must be an int or float, got {type(value).__name__}: {value}"

    elif opcode == "COPY":
        if len(inst) != 3:
            return False, f"COPY requires 3 elements ('COPY', dest, src), got {len(inst)}: {inst}"
        dest, src = inst[1], inst[2]
        if not is_var_name(dest):
            return False, f"COPY dest must be a non-empty string variable name, got: {dest}"
        if not is_var_name(src):
            return False, f"COPY src must be a non-empty string variable name, got: {src}"

    elif opcode == "BINOP":
        if len(inst) != 5:
            return False, f"BINOP requires 5 elements ('BINOP', op, dest, src1, src2), got {len(inst)}: {inst}"
        op, dest, src1, src2 = inst[1], inst[2], inst[3], inst[4]
        if op not in VALID_BINOPS:
            return False, f"Invalid binary operator '{op}'. Valid operators: {sorted(list(VALID_BINOPS))}"
        if not is_var_name(dest):
            return False, f"BINOP dest must be a non-empty string variable name, got: {dest}"
        if not is_operand(src1):
            return False, f"BINOP src1 must be a variable name or number, got: {src1}"
        if not is_operand(src2):
            return False, f"BINOP src2 must be a variable name or number, got: {src2}"

    elif opcode == "PRINT":
        if len(inst) != 2:
            return False, f"PRINT requires 2 elements ('PRINT', src), got {len(inst)}: {inst}"
        src = inst[1]
        if not is_operand(src):
            return False, f"PRINT src must be a variable name or number, got: {src}"

    return True, ""


def validate_ir(ir):
    if not isinstance(ir, list):
        return False, f"IR program must be a list of instruction tuples, got {type(ir).__name__}"

    for idx, inst in enumerate(ir):
        is_valid, msg = validate_instruction(inst)
        if not is_valid:
            return False, f"Error at instruction {idx + 1}: {msg}"

    return True, ""


def format_instruction(inst):
    opcode = inst[0]
    if opcode == "CONST":
        return f"{inst[1]} = {inst[2]}"
    elif opcode == "COPY":
        return f"{inst[1]} = {inst[2]}"
    elif opcode == "BINOP":
        return f"{inst[2]} = {inst[3]} {inst[1]} {inst[4]}"
    elif opcode == "PRINT":
        return f"PRINT {inst[1]}"
    return str(inst)


def format_ir(ir):
    lines = []
    for idx, inst in enumerate(ir, start=1):
        lines.append(f"{idx:2d}: {format_instruction(inst)}")
    return "\n".join(lines)


def print_ir(ir):
    print(format_ir(ir))
