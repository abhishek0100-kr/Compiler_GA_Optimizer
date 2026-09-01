from ir import validate_ir, format_ir
from passes.algebraic_simplification import algebraic_simplification_pass


def test_algebraic_simplification():
    input_ir = [
        ("BINOP", "+", "t1", "x", 0),
        ("BINOP", "+", "t2", 0, "y"),
        ("BINOP", "-", "t3", "z", 0),
        ("BINOP", "-", "t4", "w", "w"),
        ("BINOP", "*", "t5", "a", 1),
        ("BINOP", "*", "t6", 1, "b"),
        ("BINOP", "*", "t7", "c", 0),
        ("BINOP", "/", "t8", "d", 1),
        ("BINOP", "/", "t9", "k", "k"),
        ("PRINT", "t1"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    optimized_ir = algebraic_simplification_pass(input_ir)

    is_valid, msg = validate_ir(optimized_ir)
    assert is_valid, f"Optimized IR invalid: {msg}"

    expected_ir = [
        ("COPY", "t1", "x"),
        ("COPY", "t2", "y"),
        ("COPY", "t3", "z"),
        ("CONST", "t4", 0),
        ("COPY", "t5", "a"),
        ("COPY", "t6", "b"),
        ("CONST", "t7", 0),
        ("COPY", "t8", "d"),
        ("CONST", "t9", 1),
        ("PRINT", "t1"),
    ]

    assert (
        optimized_ir == expected_ir
    ), f"Mismatch!\nGot:\n{format_ir(optimized_ir)}\n\nExpected:\n{format_ir(expected_ir)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- After Algebraic Simplification ---")
    print(format_ir(optimized_ir))
    print(
        "\n[PASS] Algebraic Simplification (AS) verified successfully."
    )


if __name__ == "__main__":
    test_algebraic_simplification()