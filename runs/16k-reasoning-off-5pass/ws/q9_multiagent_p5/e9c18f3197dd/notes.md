
## ideation
**Core Difficulty**:
The problem asks for the minimum total operations to ensure every element in `target` has at least one multiple in `nums`. An operation consists of incrementing an element in `nums` by 1.
The key insight is that for a specific `t` in `target`, we need to find an element `n` in `nums` such that we can increment `n` to some value `n'` where `n'` is a multiple of `t`, and the cost `(n' - n)` is minimized. Since we want `n'` to be a multiple of `t`, `n'` must be of the form `k * t`. The smallest such `n'` greater than or equal to `n` is `ceil(n / t) * t`. The cost for this specific pair `(n, t)` is `(ceil(n / t) * t) - n`.

**Candidate Approaches**:
1.  **Brute Force per Target**: Iterate through each `t` in `target`. For each `t`, iterate through all `n` in `nums`. Calculate the cost to make `n` a multiple of `t`. Track the minimum cost for `t`. Sum these minimum costs.
    *   Complexity: $O(|target| \times |nums|)$. Given constraints ($|target| \le 4$, $|nums| \le 5 \times 10^4$), this is roughly $2 \times 10^5$ operations, which is well within time limits.
2.  **Optimization (Modulo Grouping)**: Since `target` is very small, we could pre-process `nums` by their remainders modulo each `t` in `target`, but given the small size of `target`, direct iteration is simpler and likely faster due to lower constant factors and no overhead of building hash maps/lists for small `k`.
3.  **Mathematical Shortcut**: For a fixed `t`, the cost for a specific `n` is `(t - (n % t)) % t`. We just need to find `n` in `nums` that minimizes this value.

## worker: Implement the $O(|target| \times |nums|)$ solution
The solution iterates through each element `t` in the `target` array. For each `t`, it iterates through all elements `n` in the `nums` array. For every pair `(n, t)`, it calculates the cost to increment `n` to the nearest multiple of `t`. The cost is calculated as `(t - (n % t)) % t`. This handles the case where `n` is already a multiple of `t` (cost 0) and the case where it needs incrementing. The minimum cost across all `n` for a specific `t` is added to the total operations. Given the constraints (`target` length <= 4, `nums` length <= 50,000), the time complexity is $O(|target| \times |nums|)$, which is efficient enough.
