def is_zero(val):
    return val == 0 and not isinstance(val, bool)


def is_one(val):
    return val == 1 and not isinstance(val, bool)


def algebraic_simplification_pass(ir):
    new_ir = []

    for inst in ir:
        opcode = inst[0]

        if opcode == "BINOP":
            op, dest, src1, src2 = inst[1], inst[2], inst[3], inst[4]

            if op == "+":
                if is_zero(src1):
                    new_ir.append(
                        ("CONST", dest, src2)
                        if isinstance(src2, (int, float))
                        else ("COPY", dest, src2)
                    )
                elif is_zero(src2):
                    new_ir.append(
                        ("CONST", dest, src1)
                        if isinstance(src1, (int, float))
                        else ("COPY", dest, src1)
                    )
                else:
                    new_ir.append(inst)

            elif op == "-":
                if is_zero(src2):
                    new_ir.append(
                        ("CONST", dest, src1)
                        if isinstance(src1, (int, float))
                        else ("COPY", dest, src1)
                    )
                elif src1 == src2 and isinstance(src1, str):
                    new_ir.append(("CONST", dest, 0))
                else:
                    new_ir.append(inst)

            elif op == "*":
                if is_zero(src1) or is_zero(src2):
                    new_ir.append(("CONST", dest, 0))
                elif is_one(src1):
                    new_ir.append(
                        ("CONST", dest, src2)
                        if isinstance(src2, (int, float))
                        else ("COPY", dest, src2)
                    )
                elif is_one(src2):
                    new_ir.append(
                        ("CONST", dest, src1)
                        if isinstance(src1, (int, float))
                        else ("COPY", dest, src1)
                    )
                else:
                    new_ir.append(inst)

            elif op == "/":
                if is_zero(src1) and src2 != 0:
                    new_ir.append(("CONST", dest, 0))
                elif is_one(src2):
                    new_ir.append(
                        ("CONST", dest, src1)
                        if isinstance(src1, (int, float))
                        else ("COPY", dest, src1)
                    )
                elif src1 == src2 and isinstance(src1, str):
                    new_ir.append(("CONST", dest, 1))
                else:
                    new_ir.append(inst)

            else:
                new_ir.append(inst)

        else:
            new_ir.append(inst)

    return new_ir