from __future__ import annotations

import numpy as np


def make_rng(seed: int | None) -> np.random.Generator:
    return np.random.default_rng(seed)


def random_function_table(num_bits: int, rng: np.random.Generator) -> tuple[int, ...]:
    domain_size = 1 << num_bits
    table = rng.integers(0, domain_size, size=domain_size, endpoint=False)
    return tuple(int(value) for value in table.tolist())


def random_permutation_table(num_bits: int, rng: np.random.Generator) -> tuple[int, ...]:
    values = np.arange(1 << num_bits, dtype=int)
    rng.shuffle(values)
    return tuple(int(value) for value in values.tolist())
