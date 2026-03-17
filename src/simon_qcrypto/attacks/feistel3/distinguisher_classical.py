from __future__ import annotations

from simon_qcrypto.attacks.feistel3.oracle import build_oracle
from simon_qcrypto.common.bitstrings import int_to_bitstring
from simon_qcrypto.common.results import AttackResult


def run(
    half_bits: int = 3,
    seed: int | None = None,
    alpha0: int = 0,
    alpha1: int = 1,
) -> AttackResult:
    oracle = build_oracle(half_bits=half_bits, seed=seed, alpha0=alpha0, alpha1=alpha1)
    input_bits = half_bits + 1
    domain_size = 1 << input_bits
    outputs = {value: oracle.evaluate(value) for value in range(domain_size)}

    seen: dict[int, int] = {}
    recovered_period = None
    collision_count = 0
    for input_value in range(domain_size):
        output_value = outputs[input_value]
        if output_value in seen:
            collision_count += 1
            candidate = input_value ^ seen[output_value]
            if candidate != 0 and all(
                outputs[value] == outputs[value ^ candidate] for value in range(domain_size)
            ):
                recovered_period = candidate
                break
        else:
            seen[output_value] = input_value

    expected_period = oracle.hidden_period()
    return AttackResult(
        attack_name="feistel3_distinguisher",
        mode="classical",
        success=recovered_period == expected_period,
        query_count=domain_size,
        recovered_relation=(
            None if recovered_period is None else int_to_bitstring(recovered_period, input_bits)
        ),
        metadata={
            "expected_period": int_to_bitstring(expected_period, input_bits),
            "collision_count": collision_count,
            "alpha0": int_to_bitstring(alpha0, half_bits),
            "alpha1": int_to_bitstring(alpha1, half_bits),
        },
    )
