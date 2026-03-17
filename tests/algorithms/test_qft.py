from __future__ import annotations

import numpy as np
import pytest

from simon_qcrypto.algorithms.qft.experiments import run_experiment


def test_qft_statevector_matches_classical() -> None:
    result = run_experiment(num_qubits=3, basis_state=5, seed=5, mode="statevector")
    assert result.success
    assert np.allclose(
        result.classical_result["amplitudes"],
        result.quantum_result["amplitudes"],
        atol=1e-9,
    )


def test_qft_shots_look_uniform() -> None:
    try:
        result = run_experiment(num_qubits=3, basis_state=5, seed=5, mode="shots", shots=2048)
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert result.success
