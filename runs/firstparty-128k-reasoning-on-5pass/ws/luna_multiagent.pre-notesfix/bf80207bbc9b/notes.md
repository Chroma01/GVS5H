
## ideation
The core difficulty is that row flips can be optimized independently only after fixing the subset of columns that are flipped. For a column mask \(m\), a row with bitmask \(r\) contributes the smaller of the Hamming distance between \(r\) and \(m\), and its complement. Thus the target is the minimum, over all \(2^W\) column masks, of a sum over all rows.

A naive enumeration of every column mask and every row costs \(O(H2^W)\), which is too large when \(H\) is \(2\times 10^5\). The small width \(W\leq18\) should instead be exploited by aggregating equal row masks and by computing all mask answers together.

Repeated operations only matter by parity: flipping the same row or column twice has no effect. It is therefore sufficient to consider each row and column mask exactly once.

## worker: Implement the frequency-array XOR convolution usin
For a fixed set of flipped columns represented by mask `m`, a row represented by mask `r` becomes `r XOR m`. The row may then either remain unchanged or be flipped entirely, so its minimum contribution is:

`min(popcount(r XOR m), W - popcount(r XOR m))`.

Define `f[r]` as the frequency of rows equal to `r`, and define the kernel `k[z]` by:

`k[z] = min(popcount(z), W - popcount(z))`.

The total value for column mask `m` is the XOR convolution:

`g[m] = sum_r f[r] * k[r XOR m]`.

This convolution is computed using the Walsh–Hadamard transform. The inverse transform is the same transform followed by division by `2^W`. The complexity is `O((H + W) + W * 2^W)` time and `O(2^W)` memory.
