Model each bit independently because XOR constraints are linear over GF(2). For each bit position `b` (0..30, since Z_i ≤ 1e9), treat the N variables as bits. Each constraint `X_i ^ Y_i = Z_i` reduces to:
- If bit `b` of `Z_i` is 1: the two bits must differ (odd parity).
- If bit `b` of `Z_i` is 0: the two bits must be equal.

This forms a graph where each vertex has a value 0/1 and edges enforce equality/inequality. That is a 2-SAT / union-find with parity problem solvable by DSU with bipartite parity (i.e., DSU storing `xor_to_parent`). We also detect contradictions (odd cycles forcing `x ^ x = 1`) and return -1.

We need to minimize `sum A_i`. Sum of integers = sum over bits of (bit value * 2^b). For each bit we must decide 0/1 assignment for each connected component, but parity constraints fix relative values. Each component has two valid global states (toggle all bits). For each bit, pick the state giving fewer 1s (ties: arbitrary). Multiply by `2^b` and add to the per-bit assignments.

The DSU needs rollback because we process bits independently, but we can just recompute per bit: O((N+M) * 30) = ~9e6 operations, fast enough. We reconstruct per-bit arrays, then assemble `A_i`.