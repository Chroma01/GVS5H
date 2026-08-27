
## ideation
The problem requires finding, for each element $A_i$, the largest divisor $g$ such that there are at least $K$ multiples of $g$ in the entire sequence $A$. The core difficulty is efficiently computing the multiplicity counts for all candidate divisors and propagating the maximum valid divisor to each position without exceeding time limits in Python.

Candidate approaches:
1. **Frequency + Harmonic Summation**: Build a frequency array `cnt` for values up to $M = \max(A)$. For each $g \in [1, M]$, compute `total_multiples[g] = sum(cnt[g::g])`. This leverages Python's optimized C-level slicing and summation, running in $O(M \log M)$ time.
2. **Increasing-Order Propagation**: Initialize an answer array `res` with 0. Iterate $g$ from 1 to $M$. If `total_multiples[g] >= K`, assign `res[g::g] = [g] * len(res[g::g])`. Processing in increasing order ensures that larger valid divisors overwrite smaller ones, naturally leaving the maximum valid divisor at each index. Slice assignment is highly optimized in Python.
3. **Reverse-Order Propagation**: Iterate $g$ from $M$ down to 1 and only write to `res` if it's still 0. This avoids overwrites but requires conditional checks per element, which is significantly slower in Python due to interpreter overhead.

Pitfalls:
- **TLE from Python Loops**: Nested `for` loops for counting multiples or updating answers will likely TLE. Array slicing must be used for vectorized operations.
- **Memory Allocation**: Creating temporary lists via slicing (`cnt[g::g]`) repeatedly consumes memory. Total allocated memory is $O(M \log M)$, which fits within limits for $M=10^6$, but GC pressure should be monitored.
- **Edge Cases**: $K=1$ implies the answer is always $A_i$ itself. The logic naturally handles this since `total_multiples[A_i] >= 1` and slice assignment will propagate correctly. Initialization to 0 is safe because $g=1$ is always valid ($N \ge K$).

## worker: Parse input values $N$, $K$, and sequence $A$. Com
The problem reduces to finding, for each $A_i$, the largest divisor $g$ of $A_i$ such that there are at least $K$ multiples of $g$ in the entire sequence $A$. 
1. We compute the frequency of each number up to $\max(A)$ using a counting array `cnt`.
2. For each candidate divisor $g \in [1, \max(A)]$, we count its multiples in $A$ using the efficient Python slice summation `sum(cnt[g::g])`, which runs in $O(M/g)$ time. Summing over all $g$ gives $O(M \log M)$ total time.
3. We initialize an answer array `res` and iterate $g$ from 1 to $\max(A)$. If `count(g) >= K`, we assign `res[g::g] = [g] * (max_val // g)`. Because we process $g$ in increasing order, any later (larger) valid divisor will overwrite earlier assignments, naturally leaving each index with the maximum possible valid GCD.
4. Finally, we map the precomputed `res` values back to the original sequence $A$ and print them.
This approach leverages Python's optimized C-level operations for slicing and summation, keeping the constant factor low enough to pass within typical time limits for $N, M \le 1.2 \times 10^6$.
