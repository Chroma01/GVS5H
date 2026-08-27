
## ideation
The problem asks for the minimum number of adjacent swaps needed to make all 1s contiguous.  
Key observations:

- Let `p[0] < p[1] < ... < p[K-1]` be the 0‑indexed positions of the 1s in the original string, where `K` is the total number of 1s.
- If the final block of 1s occupies indices `L, L+1, ..., L+K-1`, the i‑th 1 must move to `L + i`. Because both sequences are increasing, the sum of absolute differences is simply the difference of sums:
  `cost(L) = Σ(p[i] - (L + i)) = Σp[i] - K·L - K·(K-1)/2`.
- `Σp[i]` and the quadratic term are constant, so minimizing the cost is equivalent to maximizing `L`. The largest possible `L` is `N - K` (place the block at the far right). Symmetrically, placing it at the far left would maximize the cost, so the right end is optimal.
- Hence the answer is `Σp[i] - K·(N - K) - K·(K-1)/2`.
- This can be computed in one pass over the string, keeping the running sum of indices of 1s.

Pitfalls:
- Use 0‑based indexing to match the formula.
- Use 64‑bit integers (Python `int` is unbounded) to avoid overflow, though N ≤ 5·10⁵, so 32‑bit would also work.
- Ensure the string length matches N (though not strictly necessary).

## worker: Read input N and string S, compute positions of 1s
The solution follows the derived formula:
- Let the 0‑indexed positions of all 1s be `p_0, p_1, …, p_{K-1}` where `K` is the count of 1s.
- If we place the final block of 1s starting at index `L` (so the block occupies `L, L+1, …, L+K-1`), the required adjacent swaps equal `Σ|p_i - (L+i)|`. Because both sequences are strictly increasing, the absolute values can be dropped, giving `cost(L) = Σp_i - K·L - K·(K-1)/2`.
- `Σp_i` and the quadratic term are constants, so the cost is minimized by maximizing `L`. The maximum feasible `L` is `N - K` (place the block at the right end of the string).
- Therefore the minimal number of swaps is `total - K·(N-K) - K·(K-1)/2`, where `total = Σp_i`.
- The algorithm computes `total` and `K` in one pass over `S` and then applies the formula. It runs in O(N) time and O(1) extra space, well within the limits for `N ≤ 5·10⁵`.
