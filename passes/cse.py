COMMUTATIVE_OPS = {"+", "*"}


def canonicalize_expr(op, src1, src2):
    if op in COMMUTATIVE_OPS:
        s1, s2 = str(src1), str(src2)
        if s1 > s2:
            return (op, src2, src1)
    return (op, src1, src2)


def invalidate_variable(var, expr_table):
    keys_to_delete = []
    for expr_key, dest_var in expr_table.items():
        _, src1, src2 = expr_key
        if src1 == var or src2 == var or dest_var == var:
            keys_to_delete.append(expr_key)

    for k in keys_to_delete:
        del expr_table[k]


def cse_pass(ir):
    expr_table = {}
    new_ir = []

    for inst in ir:
        opcode = inst[0]

        if opcode == "CONST":
            dest, val = inst[1], inst[2]
            invalidate_variable(dest, expr_table)
            new_ir.append(inst)

        elif opcode == "COPY":
            dest, src = inst[1], inst[2]
            invalidate_variable(dest, expr_table)
            new_ir.append(inst)

        elif opcode == "BINOP":
            op, dest, src1, src2 = inst[1], inst[2], inst[3], inst[4]
            expr_key = canonicalize_expr(op, src1, src2)

            if expr_key in expr_table:
                prev_dest = expr_table[expr_key]
                invalidate_variable(dest, expr_table)
                new_ir.append(("COPY", dest, prev_dest))
            else:
                invalidate_variable(dest, expr_table)
                expr_table[expr_key] = dest
                new_ir.append(inst)

        elif opcode == "PRINT":
            new_ir.append(inst)

        else:
            new_ir.append(inst)

    return new_ir