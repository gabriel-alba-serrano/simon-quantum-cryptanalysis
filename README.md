# simon-quantum-cryptanalysis

`simon-quantum-cryptanalysis` is an educational repository on quantum query algorithms and their use in symmetric cryptanalysis. Its main focus is Simon’s algorithm, together with small, reproducible implementations of Simon-style attacks on toy cryptographic constructions.

The project is designed as a compact study path: it starts with foundational algorithms such as Deutsch-Jozsa, Bernstein-Vazirani, and the Quantum Fourier Transform, and then builds toward Simon’s algorithm and its cryptographic applications. Each topic includes a classical reference implementation, a Qiskit-based quantum implementation, runnable scripts, tests, and short theory notes.

The cryptographic examples in this repository are intentionally small and parameterized so they can be simulated locally and inspected in detail. The goal is not to claim practical attacks on real-world systems, but to provide a clear code-level bridge between the underlying theory and concrete experimental demonstrations.

Educational repository for studying quantum query algorithms and their cryptographic applications, with a focus on Simon's algorithm and Simon-style attacks.

## Included topics

- Deutsch-Jozsa
- Bernstein-Vazirani
- Quantum Fourier Transform
- Simon's algorithm
- Simon-style distinguisher for a 3-round Feistel construction
- Simon-style forgery attack for a toy 2-block CBC-MAC

Every topic includes:

- a classical reference implementation
- a Qiskit implementation
- runnable scripts
- tests on toy instances
- theory notes in `docs/`

## Repository layout

```text
src/simon_qcrypto/
  common/      Shared utilities, GF(2) helpers, result types, Qiskit runners
  algorithms/  Deutsch-Jozsa, Bernstein-Vazirani, QFT, Simon
  crypto/      Toy Feistel-3 and CBC-MAC constructions
  attacks/     Feistel-3 distinguisher and CBC-MAC forgery demos
docs/          Overview and short theory notes
notebooks/     Walkthrough notebooks for each algorithm and attack
scripts/       Thin runnable entrypoints
examples/      Small demo programs
tests/         Unit and smoke tests
```

## Quick start

```bash
python -m pip install -e .[dev]
pytest
```

Run a demo:

```bash
python scripts/run_simon.py --mode statevector --input-bits 3
python scripts/run_feistel3_distinguisher.py --mode quantum --half-bits 3
python scripts/run_cbc_mac_forgery.py --mode quantum --block-bits 3
```

## Notes on scope

This repository uses small parameterized toy constructions so the algorithms and attacks remain locally simulable. The cryptographic examples are educational demonstrations, not claims about practical attacks on production systems.
