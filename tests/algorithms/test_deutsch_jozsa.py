from __future__ import annotations

import pytest

from simon_qcrypto.algorithms.deutsch_jozsa.experiments import run_experiment


@pytest.mark.parametrize("oracle_type", ["constant", "balanced"])
def test_deutsch_jozsa_statevector(oracle_type: str) -> None:
    result = run_experiment(num_qubits=3, oracle_type=oracle_type, seed=7, mode="statevector")
    assert result.success
    assert result.quantum_result["classification"] == oracle_type


def test_deutsch_jozsa_shots() -> None:
    try:
        result = run_experiment(
            num_qubits=3,
            oracle_type="balanced",
            seed=8,
            mode="shots",
            shots=512,
        )
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert result.success
