def resolve_copy(var, copies):
    current = var
    visited = set()
    while isinstance(current, str) and current in copies:
        if current in visited:
            break
        visited.add(current)
        current = copies[current]
    return current


def invalidate_var(var, copies):
    if var in copies:
        del copies[var]
    to_delete = [dest for dest, src in copies.items() if src == var]
    for dest in to_delete:
        del copies[dest]


def copy_propagation_pass(ir):
    copies = {}
    new_ir = []

    for inst in ir:
        opcode = inst[0]

        if opcode == "CONST":
            dest, val = inst[1], inst[2]
            invalidate_var(dest, copies)
            new_ir.append(inst)

        elif opcode == "COPY":
            dest, src = inst[1], inst[2]
            resolved_src = resolve_copy(src, copies)

            invalidate_var(dest, copies)

            if dest != resolved_src:
                copies[dest] = resolved_src

            new_ir.append(("COPY", dest, resolved_src))

        elif opcode == "BINOP":
            op, dest, src1, src2 = inst[1], inst[2], inst[3], inst[4]
            new_src1 = resolve_copy(src1, copies) if isinstance(src1, str) else src1
            new_src2 = resolve_copy(src2, copies) if isinstance(src2, str) else src2

            invalidate_var(dest, copies)
            new_ir.append(("BINOP", op, dest, new_src1, new_src2))

        elif opcode == "PRINT":
            src = inst[1]
            new_src = resolve_copy(src, copies) if isinstance(src, str) else src
            new_ir.append(("PRINT", new_src))

        else:
            new_ir.append(inst)

    return new_ir