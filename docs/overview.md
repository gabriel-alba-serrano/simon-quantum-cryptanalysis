# Overview

This repository is organized as a compact study path for quantum query algorithms and small cryptographic case studies.

## Learning path

1. Start with Deutsch-Jozsa for a first separation between classical and quantum query models.
2. Move to Bernstein-Vazirani to see how hidden linear structure is recovered in one quantum query.
3. Use QFT as the main transform primitive behind many quantum algorithms.
4. Study Simon's algorithm as the main bridge toward the cryptographic applications.
5. Reuse Simon on two toy constructions:
   - a 3-round Feistel distinguisher
   - a 2-block CBC-MAC forgery

## Code organization

- `src/simon_qcrypto/common/`: shared bitstring, GF(2), and Qiskit helpers
- `src/simon_qcrypto/algorithms/`: algorithm implementations
- `src/simon_qcrypto/crypto/`: toy constructions
- `src/simon_qcrypto/attacks/`: attack modules built on top of the constructions
- `scripts/`: thin entrypoints
- `notebooks/`: guided walkthroughs
- `tests/`: correctness and smoke tests

## Design choices

- Classical implementations are exact on small instances and use NumPy when linear algebra is helpful.
- Quantum implementations use Qiskit and support both exact statevector simulation and shot-based simulation.
- Cryptographic examples are intentionally small so the hidden-period structure can be inspected and tested locally.
