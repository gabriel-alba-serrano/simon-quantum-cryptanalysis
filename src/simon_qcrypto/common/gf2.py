from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from simon_qcrypto.common.bitstrings import bits_to_int, int_to_bits, int_to_bitstring


def ints_to_matrix(values: Iterable[int], width: int) -> np.ndarray:
    rows = [int_to_bits(value, width) for value in values]
    if not rows:
        return np.zeros((0, width), dtype=np.uint8)
    return np.array(rows, dtype=np.uint8)


def rref_mod2(matrix: np.ndarray) -> tuple[np.ndarray, list[int]]:
    reduced = np.array(matrix, dtype=np.uint8, copy=True) % 2
    rows, cols = reduced.shape
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(cols):
        pivot = None
        for row in range(pivot_row, rows):
            if reduced[row, column]:
                pivot = row
                break
        if pivot is None:
            continue

        if pivot != pivot_row:
            reduced[[pivot_row, pivot]] = reduced[[pivot, pivot_row]]

        for row in range(rows):
            if row != pivot_row and reduced[row, column]:
                reduced[row] ^= reduced[pivot_row]

        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break

    return reduced, pivot_columns


def matrix_rank_mod2(matrix: np.ndarray) -> int:
    _, pivots = rref_mod2(matrix)
    return len(pivots)


def nullspace_basis(matrix: np.ndarray) -> list[np.ndarray]:
    rows, cols = matrix.shape
    if cols == 0:
        return []

    reduced, pivots = rref_mod2(matrix)
    free_columns = [column for column in range(cols) if column not in pivots]
    if not free_columns:
        return []

    basis: list[np.ndarray] = []
    for free_column in free_columns:
        vector = np.zeros(cols, dtype=np.uint8)
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            if reduced[row, free_column]:
                vector[pivot_column] = 1
        basis.append(vector)
    return basis


def recover_hidden_xor(samples: Iterable[int], width: int) -> int | None:
    matrix = ints_to_matrix(samples, width)
    basis = nullspace_basis(matrix)
    non_zero = [vector for vector in basis if np.any(vector)]
    if len(non_zero) != 1:
        return None
    return bits_to_int(non_zero[0].tolist())


def format_basis(basis: Iterable[np.ndarray]) -> list[str]:
    return [int_to_bitstring(bits_to_int(vector.tolist()), len(vector)) for vector in basis]
