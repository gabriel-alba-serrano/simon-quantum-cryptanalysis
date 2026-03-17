from __future__ import annotations

from simon_qcrypto.attacks.cbc_mac.oracle import build_oracle
from simon_qcrypto.common.bitstrings import int_to_bitstring
from simon_qcrypto.common.results import AttackResult


def run(
    block_bits: int = 3,
    seed: int | None = None,
    alpha0: int = 0,
    alpha1: int = 1,
) -> AttackResult:
    oracle = build_oracle(block_bits=block_bits, seed=seed, alpha0=alpha0, alpha1=alpha1)
    domain_size = 1 << block_bits

    left_table: dict[int, int] = {}
    for x_value in range(domain_size):
        tag = oracle.construction.mac((alpha0, x_value))
        left_table[tag] = x_value

    query_count = domain_size
    forged_message: tuple[int, int] | None = None
    tag = None
    recovered_delta = None

    for y_value in range(domain_size):
        tag = oracle.construction.mac((alpha1, y_value))
        query_count += 1
        if tag in left_table:
            x_value = left_table[tag]
            recovered_delta = x_value ^ y_value
            forged_message = (alpha1, y_value)
            queried_message = (alpha0, x_value)
            break
    else:
        queried_message = (alpha0, 0)

    success = (
        forged_message is not None
        and queried_message != forged_message
        and oracle.construction.mac(queried_message) == oracle.construction.mac(forged_message)
    )

    return AttackResult(
        attack_name="cbc_mac_forgery",
        mode="classical",
        success=success,
        query_count=query_count,
        recovered_relation=(
            None if recovered_delta is None else int_to_bitstring(recovered_delta, block_bits)
        ),
        forgery=None
        if forged_message is None or tag is None
        else {
            "queried_message": [int_to_bitstring(value, block_bits) for value in queried_message],
            "forged_message": [int_to_bitstring(value, block_bits) for value in forged_message],
            "tag": int_to_bitstring(tag, block_bits),
        },
        metadata={
            "expected_delta": int_to_bitstring(oracle.hidden_delta(), block_bits),
            "alpha0": int_to_bitstring(alpha0, block_bits),
            "alpha1": int_to_bitstring(alpha1, block_bits),
        },
    )
