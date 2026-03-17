# Simon Attack on CBC-MAC

For the toy 2-block CBC-MAC

`Tag(m1, m2) = E(E(m1) xor m2)`

choose two distinct first blocks `alpha_0` and `alpha_1` and define

`W(b, x) = Tag(alpha_b, x)`.

Then

`W(0, x) = E(E(alpha_0) xor x)`

and

`W(1, x xor delta) = E(E(alpha_1) xor x xor delta)`

where

`delta = E(alpha_0) xor E(alpha_1)`.

Hence `W(0, x) = W(1, x xor delta)`, so the hidden Simon period is `(1, delta)`.

Once `delta` is recovered, a valid forgery follows immediately:

- query the tag of `(alpha_0, x)`
- output the untouched tag for `(alpha_1, x xor delta)`

The repository includes both a classical toy-size baseline and a Simon-based quantum version.
