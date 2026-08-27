
## ideation
Core difficulty is that the operation is defined using the current ascending order, so a direct simulation/state search is hopeless. The key structural insight is to rewrite the operation in terms of consecutive gaps `g[k] = X[k+1] - X[k]`. For four consecutive points with gaps `(g[i], g[i+1], g[i+2])`, reflecting the middle two around the midpoint of the outer two reverses the triple to `(g[i+2], g[i+1], g[i])`. Thus the operation only swaps `g[i]` and `g[i+2]`; the middle gap is unchanged. Therefore gap-index parity is invariant, and within each parity class the allowed moves are adjacent transpositions, so any permutation of odd-indexed gaps among odd positions and even-indexed gaps among even positions is reachable.

The objective becomes linear in gaps: `sum = N*X[0] + Σ_{k=1}^{N-1} (N-k)*g[k]`. `X[0]` and `X[N-1]` are invariant, and weights `(N-k)` decrease left to right. By rearrangement inequality, each parity class should independently place smaller gaps on larger weights, i.e. sort each parity class ascending and assign left-to-right within that parity.

Pitfalls: assuming total sum is invariant; assuming all gaps can be freely permuted; off-by-one in gap indices/weights; overflow from `N * X` and weighted gap sums; worrying about half-integer midpoints even though reflected coordinates remain integers; trying to simulate operations.

## worker: Implement the O(N log N) solution: read input, bui
Implemented the gap-parity rearrangement solution. The operation reverses each length-3 gap triple `(a,b,c)` to `(c,b,a)`, which is just swapping `g[i]` and `g[i+2]`; hence odd/even gap-index classes are invariant but freely permutable within themselves. The objective is linear with decreasing weights `(N-k)`, so sorting each parity class ascending and placing it left-to-right is optimal by rearrangement inequality. Uses Python integers, so no overflow concerns.
