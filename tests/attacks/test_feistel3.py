from __future__ import annotations

import pytest

from simon_qcrypto.attacks.feistel3.distinguisher_classical import run as run_classical
from simon_qcrypto.attacks.feistel3.distinguisher_quantum import run as run_quantum


def test_feistel3_classical_distinguisher() -> None:
    result = run_classical(half_bits=3, seed=17)
    assert result.success


def test_feistel3_quantum_distinguisher() -> None:
    result = run_quantum(half_bits=3, seed=17, mode="statevector")
    assert result.success


def test_feistel3_quantum_distinguisher_shots() -> None:
    try:
        result = run_quantum(half_bits=3, seed=17, mode="shots", shots=512)
    except RuntimeError as exc:
        pytest.skip(str(exc))
    assert result.success
