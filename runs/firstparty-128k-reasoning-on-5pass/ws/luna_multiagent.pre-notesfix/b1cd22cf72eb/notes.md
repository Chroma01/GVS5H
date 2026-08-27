
## ideation
The core difficulty is choosing a common final sum \(H\) while preserving the adjacent upper-tooth difference constraint after only decreasing lengths. For a fixed \(H\), each final upper length \(u_i\) must lie in the interval \([\max(0,H-D_i),\min(U_i,H)]\), and consecutive choices must differ by at most \(X\). If any feasible \(H\) is found, the grinding cost is the initial total length minus \(NH\), so maximizing feasible \(H\) is sufficient.

Feasibility is downward-monotone: from a solution for \(H\), decreasing all upper lengths by clipping them at a smaller height and decreasing lower lengths appropriately preserves the Lipschitz constraint. Thus binary search on \(H\) is valid. The interval propagation must use 64-bit arithmetic, and the upper search bound can be \(\min_i(U_i+D_i)\). A common pitfall is to test only pairwise interval nonemptiness; compatibility with neighboring upper teeth must also be propagated.

## worker: Implement the \(O(N\log V)\) binary search solutio
For a fixed common height `H`, the final upper length at position `i` must lie in:

`[max(0, H - D[i]), min(U[i], H)]`.

The reachable interval of upper lengths is propagated from left to right. If the previous reachable interval is `[L, R]`, the current length must additionally belong to `[L-X, R+X]`.

Feasibility is monotone in `H`: from any valid configuration, reducing every upper tooth by the same amount and clipping at zero yields a valid configuration for any smaller height. Therefore, binary search finds the maximum feasible `H`.

The total grinding cost is:

`sum(U[i] + D[i]) - N * H`.

The algorithm runs in `O(N log V)` time and uses `O(N)` memory.

The implementation matches the expected outputs for all provided samples.
