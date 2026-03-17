from __future__ import annotations

from dataclasses import asdict

from simon_qcrypto.algorithms.deutsch_jozsa.classical import solve_classical
from simon_qcrypto.algorithms.deutsch_jozsa.oracles import DeutschJozsaProblem, generate_problem
from simon_qcrypto.algorithms.deutsch_jozsa.quantum import run_quantum
from simon_qcrypto.common.results import ExperimentResult


def run_experiment(
    problem: DeutschJozsaProblem | None = None,
    *,
    num_qubits: int = 3,
    oracle_type: str | None = None,
    seed: int | None = None,
    mode: str = "statevector",
    shots: int = 1024,
) -> ExperimentResult:
    active_problem = problem or generate_problem(
        num_qubits=num_qubits,
        oracle_type=oracle_type,
        seed=seed,
    )
    classical_result = solve_classical(active_problem)
    quantum_result = run_quantum(active_problem, mode=mode, shots=shots, seed=seed)
    success = classical_result["classification"] == quantum_result["classification"]
    return ExperimentResult(
        name="deutsch_jozsa",
        mode=mode,
        success=success,
        problem=asdict(active_problem),
        classical_result=classical_result,
        quantum_result=quantum_result,
    )
