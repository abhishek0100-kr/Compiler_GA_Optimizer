def is_number(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def evaluate_binop(op, val1, val2):
    if op == "+":
        return val1 + val2
    elif op == "-":
        return val1 - val2
    elif op == "*":
        return val1 * val2
    elif op == "/":
        if val2 == 0:
            return None
        if isinstance(val1, int) and isinstance(val2, int) and val1 % val2 == 0:
            return val1 // val2
        return val1 / val2
    return None


def constant_folding_pass(ir):
    new_ir = []

    for inst in ir:
        opcode = inst[0]

        if opcode == "BINOP":
            op, dest, src1, src2 = inst[1], inst[2], inst[3], inst[4]

            if is_number(src1) and is_number(src2):
                folded_val = evaluate_binop(op, src1, src2)
                if folded_val is not None:
                    new_ir.append(("CONST", dest, folded_val))
                else:
                    new_ir.append(inst)
            else:
                new_ir.append(inst)
        else:
            new_ir.append(inst)

    return new_ir