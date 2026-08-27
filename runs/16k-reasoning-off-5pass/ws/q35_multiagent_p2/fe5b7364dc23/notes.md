
## ideation
The problem asks for the sum of the $K$-th power of all contiguous subarray sums.
Let $S_i$ be the prefix sum $A_1 + \dots + A_i$, with $S_0 = 0$.
The sum of the subarray $A[l..r]$ is $S_r - S_{l-1}$.
The total sum is $\sum_{1 \le l \le r \le N} (S_r - S_{l-1})^K$.
Let $j = l-1$. Then $0 \le j < r \le N$.
The expression becomes $\sum_{0 \le j < r \le N} (S_r - S_j)^K$.
Using the binomial theorem: $(S_r - S_j)^K = \sum_{k=0}^K \binom{K}{k} S_r^{K-k} (-S_j)^k = \sum_{k=0}^K \binom{K}{k} (-1)^k S_r^{K-k} S_j^k$.
Substituting this back:
$$ \sum_{0 \le j < r \le N} \sum_{k=0}^K \binom{K}{k} (-1)^k S_r^{K-k} S_j^k $$
Swap the summations:
$$ \sum_{k=0}^K \binom{K}{k} (-1)^k \sum_{0 \le j < r \le N} S_r^{K-k} S_j^k $$
For a fixed $k$, the inner sum is:
$$ \sum_{r=1}^N S_r^{K-k} \left( \sum_{j=0}^{r-1} S_j^k \right) $$
We can compute this efficiently by iterating $r$ from 1 to $N$. For each $r$, we maintain a running sum of $S_j^k$ for $j < r$. Let $P_k[r] = \sum_{j=0}^{r-1} S_j^k$. Then the term for $r$ is $S_r^{K-k} \cdot P_k[r]$.
We can precompute powers of $S_i$ or compute them on the fly. Since $K$ is small ($K \le 10$), we can maintain $K+1$ running sums for $S_j^0, S_j^1, \dots, S_j^K$.
Specifically, for each $k \in [0, K]$, we maintain `sum_Sk` which accumulates $S_j^k$.
When we process $r$, we add $S_r^{K-k} \cdot \text{sum\_Sk}$ to the total answer for term $k$, then update `sum_Sk` by adding $S_r^k$.
Wait, the inner sum is $\sum_{j=0}^{r-1} S_j^k$. So when we are at $r$, `sum_Sk` should contain $\sum_{j=0}^{r-1} S_j^k$.
Algorithm:
1. Compute prefix sums $S_0, S_1, \dots, S_N$.
2. Initialize `ans = 0`.
3. For each $k$ from 0 to $K$:
   a. Compute binomial coefficient $\binom{K}{k}$.
   b. Initialize `current_sum = 0` (this will store $\sum_{j=0}^{r-1} S_j^k$).
   c. Iterate $r$ from 1 to $N$:
      i. Add $S_r^{K-k} \cdot \text{current\_sum}$ to `ans` (multiplied by $\binom{K}{k} (-1)^k$).
      ii. Update `current_sum += S_r^k`.
   d. Multiply the accumulated sum for this $k$ by $\binom{K}{k} (-1)^k$ and add to total answer.
Actually, it's better to accumulate the total answer directly.
Total Answer = $\sum_{k=0}^K \binom{K}{k} (-1)^k \left( \sum_{r=1}^N S_r^{K-k} \left( \sum_{j=0}^{r-1} S_j^k \right) \right)$.

We can compute this in $O(NK)$ time.
Constraints: $N \le 2 \cdot 10^5$, $K \le 10$. $O(NK)$ is roughly $2 \cdot 10^6$ operations, which is very fast.

Pitfalls:
- Modulo arithmetic for negative numbers: $(-1)^k$ means we subtract if $k$ is odd.
- $S_0 = 0$ must be included in the prefix sums.
- Powers can be large, so compute modulo 998244353.
- Binomial coefficients should be computed modulo 998244353.

## worker: Implement the solution in Python.
The solution uses the binomial theorem to expand $(S_r - S_j)^K$ and swaps summations to compute the answer in $O(NK)$ time. 

Key steps:
1. Compute prefix sums $S_0, S_1, \dots, S_N$ where $S_0 = 0$.
2. For each $k \in [0, K]$, compute $\binom{K}{k} (-1)^k \sum_{r=1}^N S_r^{K-k} \left(\sum_{j=0}^{r-1} S_j^k\right)$.
3. The inner sum $\sum_{j=0}^{r-1} S_j^k$ is maintained incrementally as we iterate $r$ from 1 to $N$.
4. All arithmetic is done modulo 998244353.
5. The time complexity is $O(NK)$ which is efficient given $N \le 2 \cdot 10^5$ and $K \le 10$.
