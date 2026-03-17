from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.common.random_utils import make_rng


@dataclass(frozen=True, slots=True)
class DeutschJozsaProblem:
    num_qubits: int
    oracle_type: str
    truth_table: dict[int, int]
    seed: int | None = None


def generate_problem(
    num_qubits: int = 3,
    oracle_type: str | None = None,
    seed: int | None = None,
) -> DeutschJozsaProblem:
    if num_qubits < 1:
        raise ValueError("Deutsch-Jozsa requires at least one input qubit.")

    rng = make_rng(seed)
    chosen_type = oracle_type or ("constant" if int(rng.integers(0, 2)) == 0 else "balanced")
    domain = list(range(1 << num_qubits))

    if chosen_type == "constant":
        constant_value = int(rng.integers(0, 2))
        truth_table = {value: constant_value for value in domain}
    elif chosen_type == "balanced":
        outputs = [0] * (len(domain) // 2) + [1] * (len(domain) // 2)
        rng.shuffle(outputs)
        truth_table = dict(zip(domain, outputs, strict=True))
    else:
        raise ValueError("oracle_type must be 'constant', 'balanced', or None.")

    return DeutschJozsaProblem(
        num_qubits=num_qubits,
        oracle_type=chosen_type,
        truth_table=truth_table,
        seed=seed,
    )


def evaluate(problem: DeutschJozsaProblem, value: int) -> int:
    return problem.truth_table[value]
