from __future__ import annotations

from typing import Any

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector

try:
    from qiskit.providers.basic_provider import BasicSimulator
except Exception:  # pragma: no cover - import path depends on qiskit version
    BasicSimulator = None

from simon_qcrypto.common.bitstrings import int_to_bitstring


def get_statevector(circuit: QuantumCircuit) -> Statevector:
    if hasattr(circuit, "remove_final_measurements"):
        stripped = circuit.remove_final_measurements(inplace=False)
    else:  # pragma: no cover - compatibility fallback
        stripped = circuit.copy()
    return Statevector.from_instruction(stripped)


def get_counts(
    circuit: QuantumCircuit,
    shots: int = 1024,
    seed: int | None = None,
) -> dict[str, int]:
    if BasicSimulator is None:
        raise RuntimeError("Shot-based simulation requires qiskit's BasicSimulator provider.")

    backend = BasicSimulator()
    compiled = transpile(circuit, backend)
    run_options: dict[str, Any] = {"shots": shots}
    if seed is not None:
        run_options["seed_simulator"] = seed
    result = backend.run(compiled, **run_options).result()
    counts = result.get_counts()
    return {str(key): int(value) for key, value in counts.items()}


def marginal_probabilities(
    statevector: Statevector,
    measured_qubits: list[int],
) -> dict[str, float]:
    amplitudes = np.asarray(statevector.data, dtype=np.complex128)
    total_qubits = int(np.log2(len(amplitudes)))
    probabilities = np.zeros(1 << len(measured_qubits), dtype=float)

    for basis_index, amplitude in enumerate(amplitudes):
        projected_index = 0
        for output_offset, qubit in enumerate(measured_qubits):
            projected_index |= ((basis_index >> qubit) & 1) << output_offset
        probabilities[projected_index] += float(np.abs(amplitude) ** 2)

    return {
        int_to_bitstring(index, len(measured_qubits)): probability
        for index, probability in enumerate(probabilities.tolist())
        if probability > 1e-12
    }


def normalize_counts(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    if total == 0:
        return {}
    return {key: value / total for key, value in counts.items()}
