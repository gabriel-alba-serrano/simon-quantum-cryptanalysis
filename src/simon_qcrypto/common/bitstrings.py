from __future__ import annotations

from typing import Iterable


def int_to_bits(value: int, width: int) -> list[int]:
    return [(value >> offset) & 1 for offset in range(width)]


def bits_to_int(bits: Iterable[int]) -> int:
    value = 0
    for offset, bit in enumerate(bits):
        value |= (int(bit) & 1) << offset
    return value


def int_to_bitstring(value: int, width: int) -> str:
    return format(value, f"0{width}b")


def bitstring_to_int(bitstring: str) -> int:
    return int(bitstring, 2)


def xor_ints(left: int, right: int) -> int:
    return left ^ right


def dot_mod2(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def hamming_weight(value: int) -> int:
    return value.bit_count()


def all_bitstrings(width: int) -> list[int]:
    return list(range(1 << width))
