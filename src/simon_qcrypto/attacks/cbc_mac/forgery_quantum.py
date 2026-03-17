from __future__ import annotations

from simon_qcrypto.algorithms.simon.experiments import run_experiment as run_simon_experiment
from simon_qcrypto.attacks.cbc_mac.oracle import build_oracle
from simon_qcrypto.common.bitstrings import bitstring_to_int, int_to_bitstring
from simon_qcrypto.common.results import AttackResult


def run(
    block_bits: int = 3,
    seed: int | None = None,
    alpha0: int = 0,
    alpha1: int = 1,
    mode: str = "statevector",
    shots: int = 1024,
) -> AttackResult:
    oracle = build_oracle(block_bits=block_bits, seed=seed, alpha0=alpha0, alpha1=alpha1)
    simon_result = run_simon_experiment(
        problem=oracle.as_simon_problem(),
        mode=mode,
        shots=shots,
        seed=seed,
    )
    recovered_period = str(simon_result.quantum_result["secret"])
    recovered_period_value = bitstring_to_int(recovered_period)
    recovered_delta = recovered_period_value & oracle.mask

    queried_message = (alpha0, 0)
    forged_message = (alpha1, recovered_delta)
    tag = oracle.construction.mac(queried_message)
    success = queried_message != forged_message and oracle.construction.mac(forged_message) == tag

    return AttackResult(
        attack_name="cbc_mac_forgery",
        mode=mode,
        success=success,
        query_count=int(simon_result.quantum_result["query_count"]) + 1,
        recovered_relation=int_to_bitstring(recovered_delta, block_bits),
        forgery={
            "queried_message": [int_to_bitstring(value, block_bits) for value in queried_message],
            "forged_message": [int_to_bitstring(value, block_bits) for value in forged_message],
            "tag": int_to_bitstring(tag, block_bits),
        },
        metadata={
            "expected_delta": int_to_bitstring(oracle.hidden_delta(), block_bits),
            "expected_period": int_to_bitstring(oracle.hidden_period(), block_bits + 1),
            "recovered_period": recovered_period,
        },
    )
