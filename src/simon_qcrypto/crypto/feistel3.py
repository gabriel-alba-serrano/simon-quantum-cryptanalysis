from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.common.random_utils import make_rng, random_function_table


@dataclass(frozen=True, slots=True)
class Feistel3:
    half_bits: int
    round_functions: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
    seed: int | None = None

    @property
    def mask(self) -> int:
        return (1 << self.half_bits) - 1

    def round_function(self, round_index: int, value: int) -> int:
        return self.round_functions[round_index][value & self.mask]

    def encrypt(self, left: int, right: int) -> tuple[int, int]:
        current_left = left & self.mask
        current_right = right & self.mask
        for round_index in range(3):
            next_left = current_right
            next_right = current_left ^ self.round_function(round_index, current_right)
            current_left, current_right = next_left & self.mask, next_right & self.mask
        return current_left, current_right


def generate_feistel3(half_bits: int = 3, seed: int | None = None) -> Feistel3:
    if half_bits < 1:
        raise ValueError("half_bits must be positive.")

    rng = make_rng(seed)
    round_functions = tuple(random_function_table(half_bits, rng) for _ in range(3))
    return Feistel3(half_bits=half_bits, round_functions=round_functions, seed=seed)
