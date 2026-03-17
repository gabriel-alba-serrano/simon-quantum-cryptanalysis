from __future__ import annotations

import numpy as np

from simon_qcrypto.algorithms.qft.oracles import QFTProblem


def _bit_reverse(value: int, width: int) -> int:
    reversed_bits = format(value, f"0{width}b")[::-1]
    return int(reversed_bits, 2)


def solve_classical(problem: QFTProblem) -> dict[str, object]:
    dimension = 1 << problem.num_qubits
    indices = np.arange(dimension)
    logical_amplitudes = (
        np.exp(2j * np.pi * problem.basis_state * indices / dimension) / np.sqrt(dimension)
    )
    amplitudes = np.empty_like(logical_amplitudes)
    for logical_index, amplitude in enumerate(logical_amplitudes):
        amplitudes[_bit_reverse(logical_index, problem.num_qubits)] = amplitude
    return {
        "basis_state": format(problem.basis_state, f"0{problem.num_qubits}b"),
        "amplitudes": amplitudes,
        "ordering": "qiskit_little_endian",
    }
