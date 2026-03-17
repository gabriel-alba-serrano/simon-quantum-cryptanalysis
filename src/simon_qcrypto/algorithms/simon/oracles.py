from __future__ import annotations

from dataclasses import dataclass

from simon_qcrypto.common.random_utils import make_rng


@dataclass(frozen=True, slots=True)
class SimonProblem:
    input_bits: int
    output_bits: int
    secret: int
    truth_table: dict[int, int]
    seed: int | None = None
    label: str = "simon"


def generate_problem(
    input_bits: int = 3,
    output_bits: int | None = None,
    secret: int | None = None,
    seed: int | None = None,
) -> SimonProblem:
    if input_bits < 2:
        raise ValueError("Simon examples are more useful with at least two input qubits.")

    chosen_output_bits = output_bits or input_bits
    if chosen_output_bits < input_bits - 1:
        raise ValueError("output_bits must be large enough to assign unique pair labels.")

    rng = make_rng(seed)
    chosen_secret = secret if secret is not None else int(rng.integers(1, 1 << input_bits))
    domain = range(1 << input_bits)
    unassigned = set(domain)
    truth_table: dict[int, int] = {}
    available_outputs = list(range(1 << chosen_output_bits))
    rng.shuffle(available_outputs)
    output_index = 0

    while unassigned:
        representative = min(unassigned)
        partner = representative ^ chosen_secret
        output_value = available_outputs[output_index]
        output_index += 1
        truth_table[representative] = output_value
        truth_table[partner] = output_value
        unassigned.remove(representative)
        unassigned.remove(partner)

    return SimonProblem(
        input_bits=input_bits,
        output_bits=chosen_output_bits,
        secret=chosen_secret,
        truth_table=truth_table,
        seed=seed,
    )
