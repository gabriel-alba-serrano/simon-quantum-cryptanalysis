from __future__ import annotations

from dataclasses import asdict

from simon_qcrypto.algorithms.bernstein_vazirani.classical import solve_classical
from simon_qcrypto.algorithms.bernstein_vazirani.oracles import (
    BernsteinVaziraniProblem,
    generate_problem,
)
from simon_qcrypto.algorithms.bernstein_vazirani.quantum import run_quantum
from simon_qcrypto.common.results import ExperimentResult


def run_experiment(
    problem: BernsteinVaziraniProblem | None = None,
    *,
    num_qubits: int = 4,
    secret: int | None = None,
    bias: int | None = None,
    seed: int | None = None,
    mode: str = "statevector",
    shots: int = 1024,
) -> ExperimentResult:
    active_problem = problem or generate_problem(
        num_qubits=num_qubits,
        secret=secret,
        bias=bias,
        seed=seed,
    )
    classical_result = solve_classical(active_problem)
    quantum_result = run_quantum(active_problem, mode=mode, shots=shots, seed=seed)
    success = classical_result["secret"] == quantum_result["secret"]
    return ExperimentResult(
        name="bernstein_vazirani",
        mode=mode,
        success=success,
        problem=asdict(active_problem),
        classical_result=classical_result,
        quantum_result=quantum_result,
        metadata={"bias_is_global_phase": True},
    )
