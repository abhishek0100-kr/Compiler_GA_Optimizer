from ir import validate_ir, format_ir
from pipeline import execute_pipeline


def test_pipeline_executor():
    input_ir = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("BINOP", "+", "t1", "a", "b"),
        ("BINOP", "*", "unused", "t1", 2),
        ("PRINT", "t1"),
    ]

    is_valid, msg = validate_ir(input_ir)
    assert is_valid, f"Input IR invalid: {msg}"

    pipeline_a = ["CP", "CF", "DCE"]
    result_a = execute_pipeline(input_ir, pipeline_a)

    expected_a = [
        ("CONST", "t1", 30),
        ("PRINT", "t1"),
    ]
    assert (
        result_a == expected_a
    ), f"Pipeline A failed.\nGot:\n{format_ir(result_a)}\nExpected:\n{format_ir(expected_a)}"

    result_indices = execute_pipeline(input_ir, [0, 1, 5])
    assert (
        result_indices == expected_a
    ), "Pipeline execution with integer indices failed"

    pipeline_b = ["DCE", "CP", "CF"]
    result_b = execute_pipeline(input_ir, pipeline_b)

    expected_b = [
        ("CONST", "a", 10),
        ("CONST", "b", 20),
        ("CONST", "t1", 30),
        ("PRINT", "t1"),
    ]
    assert (
        result_b == expected_b
    ), f"Pipeline B failed.\nGot:\n{format_ir(result_b)}\nExpected:\n{format_ir(expected_b)}"

    print("--- Input IR ---")
    print(format_ir(input_ir))
    print("\n--- Pipeline A (CP -> CF -> DCE) Result ---")
    print(format_ir(result_a))
    print("\n--- Pipeline B (DCE -> CP -> CF) Result ---")
    print(format_ir(result_b))
    print(
        "\n[PASS] Pipeline Executor and Pass Ordering differences verified successfully."
    )


if __name__ == "__main__":
    test_pipeline_executor()