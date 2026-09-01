from ir import validate_ir, format_ir
from passes.cse import cse_pass


def test_cse():
    input_ir = [
        ("BINOP", "+", "t1", "a", "b"),
        ("BINOP", "+", "t2", "b", "a"),
        ("BINOP", "*", "t3", "x", "y"),
        ("BINOP", "*", "t4", "x", "y"),
        ("CONST", "a", 100),
        ("BINOP", "+", "t5", "a", "b"),
        ("PRINT", "t2"),
        ("PRINT", "t4"),
        ("PRINT", "t5"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    optimized_ir = cse_pass(input_ir)

    is_valid, msg = validate_ir(optimized_ir)
    assert is_valid, f"Optimized IR invalid: {msg}"

    expected_ir = [
        ("BINOP", "+", "t1", "a", "b"),
        ("COPY", "t2", "t1"),
        ("BINOP", "*", "t3", "x", "y"),
        ("COPY", "t4", "t3"),
        ("CONST", "a", 100),
        ("BINOP", "+", "t5", "a", "b"),
        ("PRINT", "t2"),
        ("PRINT", "t4"),
        ("PRINT", "t5"),
    ]

    assert (
        optimized_ir == expected_ir
    ), f"Mismatch!\nGot:\n{format_ir(optimized_ir)}\n\nExpected:\n{format_ir(expected_ir)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- After Common Subexpression Elimination ---")
    print(format_ir(optimized_ir))
    print(
        "\n[PASS] Common Subexpression Elimination (CSE) verified successfully."
    )


if __name__ == "__main__":
    test_cse()