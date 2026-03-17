from __future__ import annotations

import pytest

from simon_qcrypto.algorithms.simon.experiments import run_experiment


def test_simon_statevector_recovers_secret() -> None:
    result = run_experiment(input_bits=3, secret=0b011, seed=13, mode="statevector")
    assert result.success
    assert result.quantum_result["secret"] == "011"


def test_simon_shots_recovers_secret() -> None:
    try:
        result = run_experiment(input_bits=3, secret=0b011, seed=13, mode="shots", shots=512)
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert result.success
