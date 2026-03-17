# Bernstein-Vazirani

Bernstein-Vazirani encodes a hidden bit string `s` in the linear Boolean function

`f(x) = s · x xor b`.

Classically, recovering `s` exactly requires one query per input bit plus one query for the bias. Quantumly, the secret string appears after a single oracle call and a final layer of Hadamards.

In this repository:

- the classical solver queries the zero vector and the standard basis vectors
- the quantum solver recovers `s` directly
- the bias term is tracked separately because it only contributes a global phase in the standard quantum construction
