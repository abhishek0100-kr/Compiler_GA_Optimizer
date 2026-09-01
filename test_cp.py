from ir import validate_ir, format_ir
from passes.constant_propagation import constant_propagation_pass


def test_constant_propagation():
    input_ir = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", "a", "b"),
        ("COPY", "c", "a"),
        ("BINOP", "*", "t2", "c", "t1"),
        ("CONST", "a", 50),
        ("BINOP", "+", "t3", "a", "b"),
        ("PRINT", "t3"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    optimized_ir = constant_propagation_pass(input_ir)

    is_valid, msg = validate_ir(optimized_ir)
    assert is_valid, f"Optimized IR invalid: {msg}"

    expected_ir = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", 10, 20),
        ("CONST", "c", 10),
        ("BINOP", "*", "t2", 10, "t1"),
        ("CONST", "a", 50),
        ("BINOP", "+", "t3", 50, 20),
        ("PRINT", "t3"),
    ]

    assert (
        optimized_ir == expected_ir
    ), f"Mismatch!\nGot:\n{format_ir(optimized_ir)}\n\nExpected:\n{format_ir(expected_ir)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- After Constant Propagation ---")
    print(format_ir(optimized_ir))
    print("\n[PASS] Constant Propagation verified successfully.")


if __name__ == "__main__":
    test_constant_propagation()