from __future__ import annotations

from dataclasses import asdict

from simon_qcrypto.algorithms.simon.classical import solve_classical
from simon_qcrypto.algorithms.simon.oracles import SimonProblem, generate_problem
from simon_qcrypto.algorithms.simon.quantum import run_quantum
from simon_qcrypto.common.results import ExperimentResult


def run_experiment(
    problem: SimonProblem | None = None,
    *,
    input_bits: int = 3,
    output_bits: int | None = None,
    secret: int | None = None,
    seed: int | None = None,
    mode: str = "statevector",
    shots: int = 1024,
) -> ExperimentResult:
    active_problem = problem or generate_problem(
        input_bits=input_bits,
        output_bits=output_bits,
        secret=secret,
        seed=seed,
    )
    classical_result = solve_classical(active_problem)
    quantum_result = run_quantum(active_problem, mode=mode, shots=shots, seed=seed)
    success = classical_result["secret"] == quantum_result["secret"]
    return ExperimentResult(
        name="simon",
        mode=mode,
        success=success,
        problem=asdict(active_problem),
        classical_result=classical_result,
        quantum_result=quantum_result,
    )
