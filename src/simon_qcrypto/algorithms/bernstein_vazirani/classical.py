from __future__ import annotations

from simon_qcrypto.algorithms.bernstein_vazirani.oracles import BernsteinVaziraniProblem, evaluate


def solve_classical(problem: BernsteinVaziraniProblem) -> dict[str, object]:
    bias = evaluate(problem, 0)
    secret = 0
    for bit in range(problem.num_qubits):
        if evaluate(problem, 1 << bit) ^ bias:
            secret |= 1 << bit

    return {
        "secret": format(secret, f"0{problem.num_qubits}b"),
        "bias": bias,
        "queries": problem.num_qubits + 1,
    }
