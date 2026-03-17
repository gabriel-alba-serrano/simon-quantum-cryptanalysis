from __future__ import annotations

from simon_qcrypto.algorithms.simon.experiments import run_experiment as run_simon_experiment
from simon_qcrypto.attacks.feistel3.oracle import build_oracle
from simon_qcrypto.common.bitstrings import int_to_bitstring
from simon_qcrypto.common.results import AttackResult


def run(
    half_bits: int = 3,
    seed: int | None = None,
    alpha0: int = 0,
    alpha1: int = 1,
    mode: str = "statevector",
    shots: int = 1024,
) -> AttackResult:
    oracle = build_oracle(half_bits=half_bits, seed=seed, alpha0=alpha0, alpha1=alpha1)
    simon_result = run_simon_experiment(
        problem=oracle.as_simon_problem(),
        mode=mode,
        shots=shots,
        seed=seed,
    )
    expected_period = int_to_bitstring(oracle.hidden_period(), half_bits + 1)
    recovered_period = str(simon_result.quantum_result["secret"])

    return AttackResult(
        attack_name="feistel3_distinguisher",
        mode=mode,
        success=recovered_period == expected_period,
        query_count=int(simon_result.quantum_result["query_count"]),
        recovered_relation=recovered_period,
        metadata={
            "expected_period": expected_period,
            "alpha0": int_to_bitstring(alpha0, half_bits),
            "alpha1": int_to_bitstring(alpha1, half_bits),
            "simon_recovered": bool(simon_result.quantum_result.get("recovered", True)),
        },
    )
