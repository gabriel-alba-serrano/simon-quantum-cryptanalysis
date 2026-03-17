from __future__ import annotations

from simon_qcrypto.algorithms.simon.oracles import SimonProblem
from simon_qcrypto.common.bitstrings import int_to_bitstring


def solve_classical(problem: SimonProblem) -> dict[str, object]:
    seen: dict[int, int] = {}
    recovered_secret = None
    for input_value in range(1 << problem.input_bits):
        output_value = problem.truth_table[input_value]
        if output_value in seen:
            recovered_secret = input_value ^ seen[output_value]
            break
        seen[output_value] = input_value

    if recovered_secret is None:
        recovered_secret = 0

    return {
        "secret": int_to_bitstring(recovered_secret, problem.input_bits),
        "queries": len(problem.truth_table),
        "truth_table": dict(problem.truth_table),
    }
