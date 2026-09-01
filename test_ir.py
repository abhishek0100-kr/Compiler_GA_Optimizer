from ir import validate_ir, format_ir, print_ir


def run_tests():
    sample_program = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("COPY", "x", "a"),
        ("BINOP", "+", "t1", "x", "b"),
        ("PRINT", "t1"),
    ]

    is_valid, msg = validate_ir(sample_program)
    assert is_valid, f"Sample program validation failed: {msg}"
    print("[PASS] Sample program validated successfully.")

    reassign_program = [
        ("CONST", "x", 10),
        ("BINOP", "+", "y", "x", "x"),
        ("CONST", "x", 20),
        ("BINOP", "+", "z", "x", "y"),
        ("PRINT", "z"),
    ]
    is_valid, msg = validate_ir(reassign_program)
    assert is_valid, f"Reassignment program validation failed: {msg}"
    print("[PASS] Reassignment program validated successfully.")

    invalid_test_cases = [
        ("Not a list", "ir must be a list"),
        ([("CONST", "a")], "CONST missing value"),
        ([("COPY", "a", "b", "c")], "COPY arity > 3"),
        ([("BINOP", "+", "a")], "BINOP arity < 5"),
        ([("BINOP", "%", "c", "a", "b")], "Unsupported operator '%'"),
        ([("UNKNOWN", "a", "b")], "Invalid opcode"),
        ([("CONST", 123, 10)], "Numeric dest in CONST"),
    ]

    for bad_ir, desc in invalid_test_cases:
        is_valid, msg = validate_ir(bad_ir)
        assert not is_valid, f"Expected validation failure for: {desc}"
        print(f"[PASS] Correctly rejected: {desc} -> {msg}")

    print("\n--- Pretty-Printed Sample Program ---")
    print_ir(sample_program)

    print("\n--- Pretty-Printed Reassignment Program ---")
    print_ir(reassign_program)

    print("\nAll IR foundation unit tests passed successfully.")


if __name__ == "__main__":
    run_tests()
