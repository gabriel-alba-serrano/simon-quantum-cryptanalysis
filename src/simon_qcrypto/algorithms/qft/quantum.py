from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit

from simon_qcrypto.algorithms.qft.oracles import QFTProblem
from simon_qcrypto.common.qiskit_runner import get_counts, get_statevector, normalize_counts


def _apply_qft(circuit: QuantumCircuit, num_qubits: int) -> None:
    for target in range(num_qubits):
        circuit.h(target)
        for control in range(target + 1, num_qubits):
            angle = np.pi / (2 ** (control - target))
            circuit.cp(angle, control, target)
    for offset in range(num_qubits // 2):
        circuit.swap(offset, num_qubits - offset - 1)


def build_circuit(problem: QFTProblem, measure: bool = False) -> QuantumCircuit:
    classical_bits = problem.num_qubits if measure else 0
    circuit = QuantumCircuit(problem.num_qubits, classical_bits)
    for bit in range(problem.num_qubits):
        if (problem.basis_state >> bit) & 1:
            circuit.x(bit)
    _apply_qft(circuit, problem.num_qubits)
    if measure:
        circuit.measure(range(problem.num_qubits), range(problem.num_qubits))
    return circuit


def run_quantum(
    problem: QFTProblem,
    mode: str = "statevector",
    shots: int = 1024,
    seed: int | None = None,
) -> dict[str, object]:
    if mode == "statevector":
        statevector = get_statevector(build_circuit(problem, measure=False))
        return {
            "amplitudes": np.asarray(statevector.data, dtype=np.complex128),
            "query_count": 0,
        }

    if mode == "shots":
        counts = get_counts(build_circuit(problem, measure=True), shots=shots, seed=seed)
        return {
            "counts": counts,
            "probabilities": normalize_counts(counts),
            "query_count": shots,
        }

    raise ValueError("mode must be 'statevector' or 'shots'.")
