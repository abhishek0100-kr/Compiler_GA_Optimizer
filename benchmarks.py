BENCHMARKS = {
    "BM1_Arithmetic_Intensity": [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", "a", "b"),
        ("BINOP", "*", "t2", "t1", 2),
        ("BINOP", "+", "t3", "t1", 0),
        ("BINOP", "*", "t4", "t3", 1),
        ("BINOP", "+", "t5", "t4", "t2"),
        ("PRINT", "t5"),
    ],
    "BM2_Redundant_Expressions": [
        ("CONST", "x", 4),
        ("CONST", "y", 8),
        ("BINOP", "+", "t1", "x", "y"),
        ("BINOP", "+", "t2", "y", "x"),
        ("BINOP", "*", "t3", "x", "y"),
        ("BINOP", "*", "t4", "x", "y"),
        ("BINOP", "+", "r1", "t1", "t2"),
        ("BINOP", "+", "r2", "t3", "t4"),
        ("BINOP", "+", "final", "r1", "r2"),
        ("PRINT", "final"),
    ],
    "BM3_Dead_Code_Heavy": [
        ("CONST", "base", 100),
        ("CONST", "d1", 50),
        ("BINOP", "+", "dead_acc", "base", "d1"),
        ("BINOP", "*", "dead_val", "dead_acc", 4),
        ("COPY", "dead_copy", "dead_val"),
        ("CONST", "active", 5),
        ("BINOP", "+", "res", "active", 10),
        ("PRINT", "res"),
    ],
    "BM4_Deep_Copy_Chain": [
        ("CONST", "val", 42),
        ("COPY", "c1", "val"),
        ("COPY", "c2", "c1"),
        ("COPY", "c3", "c2"),
        ("COPY", "c4", "c3"),
        ("BINOP", "+", "out", "c4", 8),
        ("PRINT", "out"),
    ],
    "BM5_Algebraic_Identities": [
        ("CONST", "p", 12),
        ("CONST", "q", 0),
        ("BINOP", "+", "t1", "p", "q"),
        ("BINOP", "-", "t2", "p", "q"),
        ("BINOP", "*", "t3", "t1", 0),
        ("BINOP", "*", "t4", "t2", 1),
        ("BINOP", "+", "total", "t3", "t4"),
        ("PRINT", "total"),
    ],
}


def get_all_benchmarks():
    return BENCHMARKS