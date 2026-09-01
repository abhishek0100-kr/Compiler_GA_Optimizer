from passes.constant_propagation import constant_propagation_pass
from passes.constant_folding import constant_folding_pass
from passes.copy_propagation import copy_propagation_pass
from passes.cse import cse_pass
from passes.algebraic_simplification import algebraic_simplification_pass
from passes.dead_code_elimination import dead_code_elimination_pass

PASS_REGISTRY = {
    "CP": constant_propagation_pass,
    "CF": constant_folding_pass,
    "CopyP": copy_propagation_pass,
    "CSE": cse_pass,
    "AS": algebraic_simplification_pass,
    "DCE": dead_code_elimination_pass,
}

PASS_NAMES = ["CP", "CF", "CopyP", "CSE", "AS", "DCE"]