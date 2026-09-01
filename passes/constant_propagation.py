def constant_propagation_pass(ir):
    known_constants = {}
    new_ir = []

    for inst in ir:
        opcode = inst[0]

        if opcode == "CONST":
            dest, val = inst[1], inst[2]
            known_constants[dest] = val
            new_ir.append(inst)

        elif opcode == "COPY":
            dest, src = inst[1], inst[2]
            if src in known_constants:
                val = known_constants[src]
                known_constants[dest] = val
                new_ir.append(("CONST", dest, val))
            else:
                if dest in known_constants:
                    del known_constants[dest]
                new_ir.append(inst)

        elif opcode == "BINOP":
            op, dest, src1, src2 = inst[1], inst[2], inst[3], inst[4]

            new_src1 = known_constants[src1] if src1 in known_constants else src1
            new_src2 = known_constants[src2] if src2 in known_constants else src2

            if dest in known_constants:
                del known_constants[dest]

            new_ir.append(("BINOP", op, dest, new_src1, new_src2))

        elif opcode == "PRINT":
            src = inst[1]
            new_src = known_constants[src] if src in known_constants else src
            new_ir.append(("PRINT", new_src))

        else:
            new_ir.append(inst)

    return new_ir