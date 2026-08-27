
## ideation
**Core Difficulty:**
1.  **Range Query Efficiency:** The range $[l, r]$ can be up to $10^9$, so we cannot construct the array `nums` for each query. We need an $O(1)$ or $O(\log n)$ way to compute the sum of costs for a range.
2.  **Cost Function Derivation:** We must correctly determine the minimum number of operations. The operation divides two numbers by 4, effectively reducing their "division depth" by 1. The problem reduces to calculating the sum of division depths for all numbers in the range and pairing them up optimally.
3.  **Optimization:** With $10^5$ queries, an $O(\log n)$ per query solution is required.

**Candidate Approaches:**
1.  **Prefix Sum with Blocks:** The cost function $v(x)$ is constant over intervals $[4^k, 4^{k+1}-1]$. We can compute the prefix sum $P(n) = \sum_{x=1}^n v(x)$ by iterating through these blocks. The answer for $[l, r]$ is $\lceil (P(r) - P(l-1)) / 2 \rceil$.
2.  **Direct Simulation:** Iterate from $l$ to $r$ and simulate operations. This will TLE ($O(N)$ per query).
3.  **Mathematical Formula:** Derive a closed form for $P(n)$ based on the geometric series of block counts.

**Pitfalls:**
1.  **Cost Formula:** Incorrectly assuming the cost is simply the sum of depths without considering the pairing constraint. The correct formula is $\lceil \text{Total Depth} / 2 \rceil$.
2.  **Range Boundaries:** Careful handling of the upper bound of each block ($4^k - 1$) and the intersection with $n$.
3.  **Zero Handling:** $l-1$ can be 0, so $P(0)$ must return 0.
4.  **Integer Size:** While Python handles large integers automatically, intermediate calculations (like $4^{16}$) should be checked for performance, though they are small enough here.

## worker: Implement the helper function `get_cost_sum(n)` th
The problem asks for the minimum number of operations to reduce all numbers in a range $[l, r]$ to zero. An operation divides two numbers by 4. This is equivalent to reducing the "cost" of each number, where the cost of a number $x$ is the number of divisions by 4 needed to reach 0. The cost of $x$ is $\lfloor \log_4 x \rfloor + 1$. Each operation reduces the total cost of the array by 2 (if both numbers are non-zero) or 1 (if one is zero). To minimize operations, we should always pair two non-zero numbers. The minimum operations required is $\lceil \text{Total Cost} / 2 \rceil$.
Since the range $[l, r]$ can be up to $10^9$, we cannot iterate through all numbers. Instead, we observe that the cost function is constant over intervals $[4^k, 4^{k+1}-1]$. We can compute the sum of costs for a range $[1, n]$ by iterating through these intervals (powers of 4) and summing up the costs. This allows us to compute the prefix sum of costs in $O(\log n)$ time. For each query, we compute the cost sum for $[l, r]$ as $P(r) - P(l-1)$ and apply the formula.
