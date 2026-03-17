from __future__ import annotations

from qiskit import QuantumCircuit

from simon_qcrypto.algorithms.deutsch_jozsa.oracles import DeutschJozsaProblem
from simon_qcrypto.common.qiskit_runner import get_counts, get_statevector, marginal_probabilities


def _apply_oracle(circuit: QuantumCircuit, problem: DeutschJozsaProblem) -> None:
    ancilla = problem.num_qubits
    controls = list(range(problem.num_qubits))
    for input_value, output_value in problem.truth_table.items():
        if output_value == 0:
            continue
        zero_controls = [index for index in controls if ((input_value >> index) & 1) == 0]
        for index in zero_controls:
            circuit.x(index)
        if len(controls) == 1:
            circuit.cx(controls[0], ancilla)
        else:
            circuit.mcx(controls, ancilla)
        for index in reversed(zero_controls):
            circuit.x(index)


def build_circuit(problem: DeutschJozsaProblem, measure: bool = False) -> QuantumCircuit:
    classical_bits = problem.num_qubits if measure else 0
    circuit = QuantumCircuit(problem.num_qubits + 1, classical_bits)
    ancilla = problem.num_qubits

    circuit.x(ancilla)
    circuit.h(ancilla)
    circuit.h(range(problem.num_qubits))
    _apply_oracle(circuit, problem)
    circuit.h(range(problem.num_qubits))

    if measure:
        circuit.measure(range(problem.num_qubits), range(problem.num_qubits))
    return circuit


def run_quantum(
    problem: DeutschJozsaProblem,
    mode: str = "statevector",
    shots: int = 1024,
    seed: int | None = None,
) -> dict[str, object]:
    if mode == "statevector":
        statevector = get_statevector(build_circuit(problem, measure=False))
        probabilities = marginal_probabilities(statevector, list(range(problem.num_qubits)))
        zero_state = "0" * problem.num_qubits
        classification = (
            "constant" if probabilities.get(zero_state, 0.0) > 1.0 - 1e-9 else "balanced"
        )
        return {
            "classification": classification,
            "probabilities": probabilities,
            "query_count": 1,
        }

    if mode == "shots":
        counts = get_counts(build_circuit(problem, measure=True), shots=shots, seed=seed)
        zero_state = "0" * problem.num_qubits
        classification = "constant" if set(counts) == {zero_state} else "balanced"
        return {
            "classification": classification,
            "counts": counts,
            "query_count": shots,
        }

    raise ValueError("mode must be 'statevector' or 'shots'.")
