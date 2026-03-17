# Simon Attack on 3-Round Feistel

For a toy 3-round Feistel network with round functions `F1`, `F2`, and `F3`, define the derived function

`W(b, x) = L(E(x, alpha_b)) xor alpha_b`

where `alpha_0` and `alpha_1` are two distinct fixed right-half constants and `L` denotes the left half of the ciphertext.

With the round convention used in this repository, the left ciphertext half is

`alpha_b xor F2(x xor F1(alpha_b))`

so

`W(b, x) = F2(x xor F1(alpha_b))`.

This implies the Simon period

`(1, F1(alpha_0) xor F1(alpha_1))`.

The classical baseline exhaustively inspects the derived oracle on toy sizes. The quantum version feeds the same derived oracle into Simon's algorithm to recover the hidden relation efficiently.
