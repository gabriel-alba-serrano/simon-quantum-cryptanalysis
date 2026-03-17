from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.algorithms.simon.oracles import SimonProblem
from simon_qcrypto.crypto.cbc_mac import CBCMAC, generate_cbc_mac


@dataclass(frozen=True, slots=True)
class CBCMACSimonOracle:
    construction: CBCMAC
    alpha0: int
    alpha1: int

    @property
    def mask(self) -> int:
        return (1 << self.construction.block_bits) - 1

    def hidden_delta(self) -> int:
        return self.construction.encrypt_block(
            self.alpha0
        ) ^ self.construction.encrypt_block(self.alpha1)

    def hidden_period(self) -> int:
        return (1 << self.construction.block_bits) | self.hidden_delta()

    def evaluate(self, value: int) -> int:
        selector = (value >> self.construction.block_bits) & 1
        x_value = value & self.mask
        prefix = self.alpha1 if selector else self.alpha0
        return self.construction.mac((prefix, x_value))

    def as_simon_problem(self) -> SimonProblem:
        input_bits = self.construction.block_bits + 1
        truth_table = {
            value: self.evaluate(value)
            for value in range(1 << input_bits)
        }
        return SimonProblem(
            input_bits=input_bits,
            output_bits=self.construction.block_bits,
            secret=self.hidden_period(),
            truth_table=truth_table,
            seed=self.construction.seed,
            label="cbc_mac",
        )


def build_oracle(
    block_bits: int = 3,
    seed: int | None = None,
    alpha0: int = 0,
    alpha1: int = 1,
) -> CBCMACSimonOracle:
    if alpha0 == alpha1:
        raise ValueError("alpha0 and alpha1 must be distinct.")
    construction = generate_cbc_mac(block_bits=block_bits, seed=seed)
    return CBCMACSimonOracle(construction=construction, alpha0=alpha0, alpha1=alpha1)
