from __future__ import annotations

from qiskit import QuantumCircuit

from simon_qcrypto.algorithms.bernstein_vazirani.oracles import BernsteinVaziraniProblem
from simon_qcrypto.common.qiskit_runner import get_counts, get_statevector, marginal_probabilities


def build_circuit(problem: BernsteinVaziraniProblem, measure: bool = False) -> QuantumCircuit:
    classical_bits = problem.num_qubits if measure else 0
    circuit = QuantumCircuit(problem.num_qubits + 1, classical_bits)
    ancilla = problem.num_qubits

    circuit.x(ancilla)
    circuit.h(ancilla)
    circuit.h(range(problem.num_qubits))

    if problem.bias:
        circuit.x(ancilla)
    for bit in range(problem.num_qubits):
        if (problem.secret >> bit) & 1:
            circuit.cx(bit, ancilla)

    circuit.h(range(problem.num_qubits))
    if measure:
        circuit.measure(range(problem.num_qubits), range(problem.num_qubits))
    return circuit


def run_quantum(
    problem: BernsteinVaziraniProblem,
    mode: str = "statevector",
    shots: int = 1024,
    seed: int | None = None,
) -> dict[str, object]:
    if mode == "statevector":
        statevector = get_statevector(build_circuit(problem, measure=False))
        probabilities = marginal_probabilities(statevector, list(range(problem.num_qubits)))
        recovered = max(probabilities, key=probabilities.get)
        return {
            "secret": recovered,
            "probabilities": probabilities,
            "query_count": 1,
        }

    if mode == "shots":
        counts = get_counts(build_circuit(problem, measure=True), shots=shots, seed=seed)
        recovered = max(counts, key=counts.get)
        return {
            "secret": recovered,
            "counts": counts,
            "query_count": shots,
        }

    raise ValueError("mode must be 'statevector' or 'shots'.")
