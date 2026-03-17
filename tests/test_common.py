from __future__ import annotations

import numpy as np
import pytest
from qiskit import QuantumCircuit

from simon_qcrypto.common.bitstrings import bits_to_int, bitstring_to_int, int_to_bits, xor_ints
from simon_qcrypto.common.gf2 import ints_to_matrix, matrix_rank_mod2, recover_hidden_xor
from simon_qcrypto.common.qiskit_runner import get_counts, get_statevector, marginal_probabilities


def test_bitstring_helpers() -> None:
    assert int_to_bits(6, 3) == [0, 1, 1]
    assert bits_to_int([1, 0, 1]) == 5
    assert bitstring_to_int("101") == 5
    assert xor_ints(6, 3) == 5


def test_gf2_recovery() -> None:
    matrix = ints_to_matrix([0b110, 0b101], 3)
    assert matrix_rank_mod2(matrix) == 2
    assert recover_hidden_xor([0b110, 0b101], 3) == 0b111


def test_qiskit_statevector_runner() -> None:
    circuit = QuantumCircuit(1)
    circuit.h(0)
    statevector = get_statevector(circuit)
    probabilities = marginal_probabilities(statevector, [0])
    assert np.isclose(probabilities["0"], 0.5)
    assert np.isclose(probabilities["1"], 0.5)


def test_qiskit_counts_runner() -> None:
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    try:
        counts = get_counts(circuit, shots=256, seed=3)
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert set(counts) <= {"0", "1"}
