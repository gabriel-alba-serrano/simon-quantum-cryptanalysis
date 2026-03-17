from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.algorithms.simon.oracles import SimonProblem
from simon_qcrypto.crypto.feistel3 import Feistel3, generate_feistel3


@dataclass(frozen=True, slots=True)
class Feistel3SimonOracle:
    construction: Feistel3
    alpha0: int
    alpha1: int

    @property
    def mask(self) -> int:
        return (1 << self.construction.half_bits) - 1

    def hidden_period(self) -> int:
        delta = self.construction.round_function(
            0,
            self.alpha0,
        ) ^ self.construction.round_function(0, self.alpha1)
        return (1 << self.construction.half_bits) | delta

    def evaluate(self, value: int) -> int:
        selector = (value >> self.construction.half_bits) & 1
        x_value = value & self.mask
        alpha = self.alpha1 if selector else self.alpha0
        left, _ = self.construction.encrypt(x_value, alpha)
        return left ^ alpha

    def as_simon_problem(self) -> SimonProblem:
        input_bits = self.construction.half_bits + 1
        truth_table = {
            value: self.evaluate(value)
            for value in range(1 << input_bits)
        }
        return SimonProblem(
            input_bits=input_bits,
            output_bits=self.construction.half_bits,
            secret=self.hidden_period(),
            truth_table=truth_table,
            seed=self.construction.seed,
            label="feistel3",
        )


def build_oracle(
    half_bits: int = 3,
    seed: int | None = None,
    alpha0: int = 0,
    alpha1: int = 1,
) -> Feistel3SimonOracle:
    if alpha0 == alpha1:
        raise ValueError("alpha0 and alpha1 must be distinct.")
    construction = generate_feistel3(half_bits=half_bits, seed=seed)
    return Feistel3SimonOracle(construction=construction, alpha0=alpha0, alpha1=alpha1)
