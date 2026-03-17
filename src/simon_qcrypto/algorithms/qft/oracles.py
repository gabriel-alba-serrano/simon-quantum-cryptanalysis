from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.common.random_utils import make_rng


@dataclass(frozen=True, slots=True)
class QFTProblem:
    num_qubits: int
    basis_state: int
    seed: int | None = None


def generate_problem(
    num_qubits: int = 3,
    basis_state: int | None = None,
    seed: int | None = None,
) -> QFTProblem:
    if num_qubits < 1:
        raise ValueError("QFT requires at least one qubit.")

    rng = make_rng(seed)
    chosen_basis_state = (
        basis_state if basis_state is not None else int(rng.integers(0, 1 << num_qubits))
    )
    return QFTProblem(num_qubits=num_qubits, basis_state=chosen_basis_state, seed=seed)
