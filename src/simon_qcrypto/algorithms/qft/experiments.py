from __future__ import annotations

from dataclasses import asdict

import numpy as np

from simon_qcrypto.algorithms.qft.classical import solve_classical
from simon_qcrypto.algorithms.qft.oracles import QFTProblem, generate_problem
from simon_qcrypto.algorithms.qft.quantum import run_quantum
from simon_qcrypto.common.results import ExperimentResult


def run_experiment(
    problem: QFTProblem | None = None,
    *,
    num_qubits: int = 3,
    basis_state: int | None = None,
    seed: int | None = None,
    mode: str = "statevector",
    shots: int = 1024,
) -> ExperimentResult:
    active_problem = problem or generate_problem(
        num_qubits=num_qubits,
        basis_state=basis_state,
        seed=seed,
    )
    classical_result = solve_classical(active_problem)
    quantum_result = run_quantum(active_problem, mode=mode, shots=shots, seed=seed)

    if mode == "statevector":
        success = np.allclose(
            classical_result["amplitudes"],
            quantum_result["amplitudes"],
            atol=1e-9,
        )
    else:
        dimension = 1 << active_problem.num_qubits
        expected_probability = 1.0 / dimension
        observed = quantum_result["probabilities"]
        success = (
            max(
                abs(
                    observed.get(format(index, f"0{active_problem.num_qubits}b"), 0.0)
                    - expected_probability
                )
                for index in range(dimension)
            )
            < 0.2
        )

    return ExperimentResult(
        name="qft",
        mode=mode,
        success=success,
        problem=asdict(active_problem),
        classical_result=classical_result,
        quantum_result=quantum_result,
    )
