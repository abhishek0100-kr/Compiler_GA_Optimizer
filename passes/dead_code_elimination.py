def is_var(val):
    return isinstance(val, str) and len(val.strip()) > 0


def dead_code_elimination_pass(ir):
    live_vars = set()
    kept_instructions = []

    for inst in reversed(ir):
        opcode = inst[0]

        if opcode == "PRINT":
            src = inst[1]
            if is_var(src):
                live_vars.add(src)
            kept_instructions.append(inst)

        elif opcode == "CONST":
            dest = inst[1]
            if dest in live_vars:
                live_vars.remove(dest)
                kept_instructions.append(inst)

        elif opcode == "COPY":
            dest, src = inst[1], inst[2]
            if dest in live_vars:
                live_vars.remove(dest)
                if is_var(src):
                    live_vars.add(src)
                kept_instructions.append(inst)

        elif opcode == "BINOP":
            dest, src1, src2 = inst[2], inst[3], inst[4]
            if dest in live_vars:
                live_vars.remove(dest)
                if is_var(src1):
                    live_vars.add(src1)
                if is_var(src2):
                    live_vars.add(src2)
                kept_instructions.append(inst)

        else:
            kept_instructions.append(inst)

    kept_instructions.reverse()
    return kept_instructions