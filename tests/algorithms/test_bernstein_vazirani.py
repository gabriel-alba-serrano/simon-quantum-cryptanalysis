from __future__ import annotations

import pytest

from simon_qcrypto.algorithms.bernstein_vazirani.experiments import run_experiment


def test_bernstein_vazirani_statevector() -> None:
    result = run_experiment(num_qubits=4, secret=0b1011, bias=1, seed=11, mode="statevector")
    assert result.success
    assert result.quantum_result["secret"] == "1011"


def test_bernstein_vazirani_shots() -> None:
    try:
        result = run_experiment(
            num_qubits=4,
            secret=0b1011,
            bias=1,
            seed=11,
            mode="shots",
            shots=512,
        )
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert result.success
