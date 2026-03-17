# Deutsch-Jozsa

Deutsch-Jozsa studies a promise problem: the oracle is either constant or balanced. Classically, exact resolution may require exponentially many queries in the number of input bits. Quantumly, the promise can be resolved with a single oracle call.

The implementation in this repository uses an explicit truth table for toy sizes and builds the standard phase-kickback circuit:

1. Prepare the ancilla in `|- >`.
2. Put the input register into a uniform superposition.
3. Apply the oracle.
4. Apply Hadamards again and measure the input register.

If the result is `0...0`, the oracle is constant. Any other outcome indicates a balanced oracle.
