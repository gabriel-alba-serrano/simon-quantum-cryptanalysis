from __future__ import annotations

from simon_qcrypto.attacks.cbc_mac.oracle import build_oracle as build_cbc_oracle
from simon_qcrypto.crypto.feistel3 import generate_feistel3


def test_feistel3_encrypt_is_deterministic() -> None:
    construction = generate_feistel3(half_bits=3, seed=17)
    first = construction.encrypt(0b101, 0b001)
    second = construction.encrypt(0b101, 0b001)
    assert first == second
    assert all(0 <= value < 8 for value in first)


def test_cbc_mac_hidden_period_relation_holds() -> None:
    oracle = build_cbc_oracle(block_bits=3, seed=19)
    period = oracle.hidden_period()
    domain_size = 1 << (oracle.construction.block_bits + 1)
    for value in range(domain_size):
        assert oracle.evaluate(value) == oracle.evaluate(value ^ period)
