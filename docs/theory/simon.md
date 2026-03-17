# Simon

Simon's problem asks for the hidden XOR period `s` of a function satisfying

`f(x) = f(x xor s)`

with `s != 0` and with no other collisions.

The quantum algorithm samples vectors `y` such that

`y · s = 0 mod 2`

and then solves the resulting linear system over GF(2). This creates an exponential separation between the classical and quantum query complexity of the problem.

The repository implements:

- random two-to-one Simon oracles
- classical collision search
- quantum circuit generation for arbitrary small truth tables
- GF(2) post-processing to recover the secret from measurement equations
