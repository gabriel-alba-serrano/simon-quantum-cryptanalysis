# Quantum Fourier Transform

The Quantum Fourier Transform is the unitary transform

`|x> -> (1 / sqrt(N)) * sum_k exp(2 pi i x k / N) |k>`

for `N = 2^n`.

In this repository:

- the classical implementation computes the exact amplitude vector with NumPy
- the quantum implementation builds the QFT gate pattern from Hadamards, controlled phases, and final swaps
- statevector mode is used to compare amplitudes directly
- shot mode is used to inspect the induced measurement distribution
