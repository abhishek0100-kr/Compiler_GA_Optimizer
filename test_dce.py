from ir import validate_ir, format_ir
from passes.dead_code_elimination import dead_code_elimination_pass


def test_dead_code_elimination():
    input_ir = [
        ("CONST", "unused1", 999),
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "unused2", "a", "b"),
        ("BINOP", "+", "t1", "a", "b"),
        ("COPY", "unused3", "t1"),
        ("BINOP", "*", "result", "t1", 2),
        ("PRINT", "result"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    optimized_ir = dead_code_elimination_pass(input_ir)

    is_valid, msg = validate_ir(optimized_ir)
    assert is_valid, f"Optimized IR invalid: {msg}"

    expected_ir = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", "a", "b"),
        ("BINOP", "*", "result", "t1", 2),
        ("PRINT", "result"),
    ]

    assert (
        optimized_ir == expected_ir
    ), f"Mismatch!\nGot:\n{format_ir(optimized_ir)}\n\nExpected:\n{format_ir(expected_ir)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- After Dead Code Elimination ---")
    print(format_ir(optimized_ir))
    print("\n[PASS] Dead Code Elimination (DCE) verified successfully.")


if __name__ == "__main__":
    test_dead_code_elimination()