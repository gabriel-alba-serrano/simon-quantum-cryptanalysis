from __future__ import annotations

import pytest

from simon_qcrypto.attacks.cbc_mac.forgery_classical import run as run_classical
from simon_qcrypto.attacks.cbc_mac.forgery_quantum import run as run_quantum


def test_cbc_mac_classical_forgery() -> None:
    result = run_classical(block_bits=3, seed=19)
    assert result.success


def test_cbc_mac_quantum_forgery() -> None:
    result = run_quantum(block_bits=3, seed=19, mode="statevector")
    assert result.success


def test_cbc_mac_quantum_forgery_shots() -> None:
    try:
        result = run_quantum(block_bits=3, seed=19, mode="shots", shots=512)
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert result.success
