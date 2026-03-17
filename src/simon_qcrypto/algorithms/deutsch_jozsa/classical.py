from __future__ import annotations

from simon_qcrypto.algorithms.deutsch_jozsa.oracles import DeutschJozsaProblem


def solve_classical(problem: DeutschJozsaProblem) -> dict[str, object]:
    outputs = list(problem.truth_table.values())
    classification = "constant" if len(set(outputs)) == 1 else "balanced"
    return {
        "classification": classification,
        "queries": len(problem.truth_table),
        "truth_table": dict(problem.truth_table),
    }
