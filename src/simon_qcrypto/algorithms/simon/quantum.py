from __future__ import annotations

from qiskit import QuantumCircuit

from simon_qcrypto.algorithms.simon.oracles import SimonProblem
from simon_qcrypto.common.bitstrings import bitstring_to_int, int_to_bitstring
from simon_qcrypto.common.gf2 import recover_hidden_xor
from simon_qcrypto.common.qiskit_runner import get_counts, get_statevector, marginal_probabilities


def _apply_oracle(circuit: QuantumCircuit, problem: SimonProblem) -> None:
    controls = list(range(problem.input_bits))
    for input_value, output_value in problem.truth_table.items():
        zero_controls = [index for index in controls if ((input_value >> index) & 1) == 0]
        for index in zero_controls:
            circuit.x(index)
        for output_bit in range(problem.output_bits):
            if (output_value >> output_bit) & 1:
                target = problem.input_bits + output_bit
                if len(controls) == 1:
                    circuit.cx(controls[0], target)
                else:
                    circuit.mcx(controls, target)
        for index in reversed(zero_controls):
            circuit.x(index)


def build_circuit(problem: SimonProblem, measure: bool = False) -> QuantumCircuit:
    classical_bits = problem.input_bits if measure else 0
    circuit = QuantumCircuit(problem.input_bits + problem.output_bits, classical_bits)
    circuit.h(range(problem.input_bits))
    _apply_oracle(circuit, problem)
    circuit.h(range(problem.input_bits))
    if measure:
        circuit.measure(range(problem.input_bits), range(problem.input_bits))
    return circuit


def _recover_from_equations(samples: list[int], width: int) -> int | None:
    non_zero_samples = [sample for sample in samples if sample != 0]
    return recover_hidden_xor(non_zero_samples, width)


def run_quantum(
    problem: SimonProblem,
    mode: str = "statevector",
    shots: int = 1024,
    seed: int | None = None,
) -> dict[str, object]:
    if mode == "statevector":
        statevector = get_statevector(build_circuit(problem, measure=False))
        probabilities = marginal_probabilities(statevector, list(range(problem.input_bits)))
        equations = [
            bitstring_to_int(bitstring)
            for bitstring in probabilities
            if bitstring != "0" * problem.input_bits
        ]
        recovered_secret = _recover_from_equations(equations, problem.input_bits)
        return {
            "secret": int_to_bitstring(recovered_secret or 0, problem.input_bits),
            "probabilities": probabilities,
            "equations": [int_to_bitstring(value, problem.input_bits) for value in equations],
            "query_count": 1,
            "recovered": recovered_secret is not None,
        }

    if mode == "shots":
        total_counts: dict[str, int] = {}
        total_shots = 0
        recovered_secret = None
        attempt = 0
        max_shots = 4 * shots
        while recovered_secret is None and total_shots < max_shots:
            attempt_shots = shots
            counts = get_counts(
                build_circuit(problem, measure=True),
                shots=attempt_shots,
                seed=None if seed is None else seed + attempt,
            )
            total_shots += attempt_shots
            attempt += 1
            for bitstring, count in counts.items():
                total_counts[bitstring] = total_counts.get(bitstring, 0) + count
            equations = [
                bitstring_to_int(bitstring)
                for bitstring in total_counts
                if bitstring != "0" * problem.input_bits
            ]
            recovered_secret = _recover_from_equations(equations, problem.input_bits)

        return {
            "secret": int_to_bitstring(recovered_secret or 0, problem.input_bits),
            "counts": total_counts,
            "equations": [
                bitstring
                for bitstring in total_counts
                if bitstring != "0" * problem.input_bits
            ],
            "query_count": total_shots,
            "recovered": recovered_secret is not None,
        }

    raise ValueError("mode must be 'statevector' or 'shots'.")
