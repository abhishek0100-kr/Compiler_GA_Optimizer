from ir import validate_ir, format_ir
from passes.copy_propagation import copy_propagation_pass


def test_copy_propagation():
    input_ir = [
        ("COPY", "y", "x"),
        ("BINOP", "+", "t1", "y", "y"),
        ("COPY", "z", "y"),
        ("BINOP", "*", "t2", "z", 5),
        ("COPY", "x", "w"),
        ("BINOP", "+", "t3", "y", "z"),
        ("PRINT", "t2"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    optimized_ir = copy_propagation_pass(input_ir)

    is_valid, msg = validate_ir(optimized_ir)
    assert is_valid, f"Optimized IR invalid: {msg}"

    expected_ir = [
        ("COPY", "y", "x"),
        ("BINOP", "+", "t1", "x", "x"),
        ("COPY", "z", "x"),
        ("BINOP", "*", "t2", "x", 5),
        ("COPY", "x", "w"),
        ("BINOP", "+", "t3", "y", "z"),
        ("PRINT", "t2"),
    ]

    assert (
        optimized_ir == expected_ir
    ), f"Mismatch!\nGot:\n{format_ir(optimized_ir)}\n\nExpected:\n{format_ir(expected_ir)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- After Copy Propagation ---")
    print(format_ir(optimized_ir))
    print("\n[PASS] Copy Propagation verified successfully.")


if __name__ == "__main__":
    test_copy_propagation()