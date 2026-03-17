from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from simon_qcrypto.common.random_utils import make_rng, random_permutation_table


@dataclass(frozen=True, slots=True)
class CBCMAC:
    block_bits: int
    permutation: tuple[int, ...]
    seed: int | None = None

    @property
    def mask(self) -> int:
        return (1 << self.block_bits) - 1

    def encrypt_block(self, block: int) -> int:
        return self.permutation[block & self.mask]

    def mac(self, blocks: Iterable[int]) -> int:
        chaining_value = 0
        for block in blocks:
            chaining_value = self.encrypt_block(chaining_value ^ (block & self.mask))
        return chaining_value


def generate_cbc_mac(block_bits: int = 3, seed: int | None = None) -> CBCMAC:
    if block_bits < 1:
        raise ValueError("block_bits must be positive.")

    rng = make_rng(seed)
    permutation = random_permutation_table(block_bits, rng)
    return CBCMAC(block_bits=block_bits, permutation=permutation, seed=seed)
