from ir import validate_ir, format_ir
from passes.constant_folding import constant_folding_pass


def test_constant_folding():
    input_ir = [
        ("CONST", "a", 10),
        ("BINOP", "+", "t1", 10, 20),
        ("BINOP", "*", "t2", 5, 4),
        ("BINOP", "-", "t3", 100, 30),
        ("BINOP", "/", "t4", 50, 2),
        ("BINOP", "+", "t5", "a", 5),
        ("PRINT", "t1"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    optimized_ir = constant_folding_pass(input_ir)

    is_valid, msg = validate_ir(optimized_ir)
    assert is_valid, f"Optimized IR invalid: {msg}"

    expected_ir = [
        ("CONST", "a", 10),
        ("CONST", "t1", 30),
        ("CONST", "t2", 20),
        ("CONST", "t3", 70),
        ("CONST", "t4", 25),
        ("BINOP", "+", "t5", "a", 5),
        ("PRINT", "t1"),
    ]

    assert (
        optimized_ir == expected_ir
    ), f"Mismatch!\nGot:\n{format_ir(optimized_ir)}\n\nExpected:\n{format_ir(expected_ir)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- After Constant Folding ---")
    print(format_ir(optimized_ir))
    print("\n[PASS] Constant Folding verified successfully.")


if __name__ == "__main__":
    test_constant_folding()