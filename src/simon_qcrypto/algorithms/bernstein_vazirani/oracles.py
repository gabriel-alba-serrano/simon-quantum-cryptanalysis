from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.common.bitstrings import dot_mod2
from simon_qcrypto.common.random_utils import make_rng


@dataclass(frozen=True, slots=True)
class BernsteinVaziraniProblem:
    num_qubits: int
    secret: int
    bias: int
    seed: int | None = None


def generate_problem(
    num_qubits: int = 4,
    secret: int | None = None,
    bias: int | None = None,
    seed: int | None = None,
) -> BernsteinVaziraniProblem:
    if num_qubits < 1:
        raise ValueError("Bernstein-Vazirani requires at least one input qubit.")

    rng = make_rng(seed)
    chosen_secret = secret if secret is not None else int(rng.integers(0, 1 << num_qubits))
    chosen_bias = bias if bias is not None else int(rng.integers(0, 2))
    return BernsteinVaziraniProblem(
        num_qubits=num_qubits,
        secret=chosen_secret,
        bias=chosen_bias,
        seed=seed,
    )


def evaluate(problem: BernsteinVaziraniProblem, value: int) -> int:
    return dot_mod2(problem.secret, value) ^ problem.bias
