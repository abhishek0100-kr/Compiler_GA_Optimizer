from passes import PASS_REGISTRY, PASS_NAMES
from test_cp import test_constant_propagation
from test_cf import test_constant_folding
from test_copy_p import test_copy_propagation
from test_cse import test_cse
from test_as import test_algebraic_simplification
from test_dce import test_dead_code_elimination


def run_all_pass_tests():
    print("=" * 60)
    print("RUNNING UNIT TESTS FOR ALL 6 OPTIMIZATION PASSES")
    print("=" * 60)

    print("\n[1/6] Testing Constant Propagation (CP)...")
    test_constant_propagation()

    print("\n[2/6] Testing Constant Folding (CF)...")
    test_constant_folding()

    print("\n[3/6] Testing Copy Propagation (CopyP)...")
    test_copy_propagation()

    print("\n[4/6] Testing Common Subexpression Elimination (CSE)...")
    test_cse()

    print("\n[5/6] Testing Algebraic Simplification (AS)...")
    test_algebraic_simplification()

    print("\n[6/6] Testing Dead Code Elimination (DCE)...")
    test_dead_code_elimination()

    assert (
        len(PASS_NAMES) == 6
    ), f"Expected 6 passes in registry, found {len(PASS_NAMES)}"
    for name in PASS_NAMES:
        assert name in PASS_REGISTRY, f"Pass {name} missing from PASS_REGISTRY"

    print("\n" + "=" * 60)
    print("ALL 6 OPTIMIZATION PASSES VERIFIED AND REGISTERED SUCCESSFULLY.")
    print("=" * 60)


if __name__ == "__main__":
    run_all_pass_tests()