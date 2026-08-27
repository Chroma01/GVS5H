
## ideation
**Core Difficulty**: The problem asks for the maximum XOR sum of exactly $K$ distinct elements from an array $A$ of size $N$. The constraints on $N$ and $K$ are up to $2 \times 10^5$, which normally makes $O(2^N)$ or $O(N^K)$ approaches impossible. However, the critical constraint is $\binom{N}{K} \le 10^6$. This explicitly allows an algorithm with complexity proportional to the number of combinations.

**Candidate Approaches**:
1.  **Brute Force with `itertools.combinations`**: Since the total number of valid subsets is at most $10^6$, we can iterate through every possible subset of size $K$, compute the XOR sum for each, and keep track of the maximum.
    *   *Complexity*: $O(\binom{N}{K} \cdot K)$. Given $\binom{N}{K} \le 10^6$ and $K \le 2 \times 10^5$, the worst-case operations would be roughly $10^6 \times \text{small constant}$ (since if $\binom{N}{K}$ is large, $K$ must be close to $N/2$, but actually the product $\binom{N}{K} \cdot K$ is bounded because if $K$ is large, $\binom{N}{K}$ is small unless $K \approx N/2$). Wait, let's re-evaluate the worst case.
    *   If $N=200,000$ and $K=1$, $\binom{N}{K} = 200,000$. Cost: $200,000 \times 1$.
    *   If $N=1000, K=500$, $\binom{1000}{500}$ is huge, but the constraint says $\binom{N}{K} \le 10^6$. So we only care about cases where the combination count is small.
    *   The maximum value of $K \cdot \binom{N}{K}$ under the constraint $\binom{N}{K} \le 10^6$:
        *   If $\binom{N}{K} = 10^6$, then $K$ could be around $20$ (if $N$ is large) or $N$ could be small.
        *   Actually, the maximum number of operations is roughly $10^6 \times \max(K)$. But if $K$ is large (e.g., $10^5$), then $\binom{N}{K}$ would be huge unless $N$ is also large and $K$ is very close to $N$ or $0$.
        *   Let's check the constraint logic: If $K \approx N/2$, $\binom{N}{K}$ explodes. So for $\binom{N}{K} \le 10^6$, $K$ cannot be too large relative to $N$ unless $N$ is small.
        *   Example: $N=200,000$. Max $\binom{N}{K} \le 10^6$. This happens when $K=1$ ($2 \cdot 10^5$), $K=2$ ($\approx 2 \cdot 10^{10}$ - too big), so $K$ must be 1. Cost $2 \cdot 10^5$.
        *   Example: $N=1000$. $\binom{1000}{500}$ is huge. We need small $K$ or $K$ near $N$. If $K=5$, $\binom{1000}{5} \approx 8 \cdot 10^{12}$ (too big).
        *   Basically, the constraint ensures that the loop runs at most $10^6$ times. Inside the loop, we do $K$ XOR operations. Is $K \cdot 10^6$ acceptable?
        *   Worst case analysis: We need to maximize $K \cdot \binom{N}{K}$ subject to $\binom{N}{K} \le 10^6$.
        *   If $\binom{N}{K} = 10^6$, what is the max $K$?
            *   If $N$ is large, $K$ must be small (e.g., $K=1 \implies N \le 10^6$).
            *   If $N$ is small, say $N=20$, $\binom{20}{10} \approx 184,756$. Here $K=10$. $10 \times 1.8 \cdot 10^5 \approx 1.8 \cdot 10^6$.
            *   If $N=22$, $\binom{22}{11} \approx 7 \cdot 10^5$. $K=11$. $11 \times 7 \cdot 10^5 \approx 7.7 \cdot 10^6$.
            *   If $N=23$, $\binom{23}{11} \approx 1.3 \cdot 10^6$ (exceeds).
            *   So the worst case is around $N=22, K=11$, giving $\approx 8 \cdot 10^6$ operations. This is well within the time limit (typically $10^8$ ops/sec).
    *   Therefore, the brute force approach is valid.

2.  **Linear Basis / Gaussian Elimination**: This is used for "maximum XOR subset of *any* size" or "maximum XOR with *at most* K elements" (which is harder). For *exactly* K elements, linear basis doesn't directly apply without complex modifications (like tracking parity or using dynamic programming on basis states), which is overkill and likely slower given the specific constraint here.

3.  **Meet-in-the-middle**: Not needed since the constraint already limits the search space.

## worker: Implement the solution using `sys.stdin` for fast 
The problem asks for the maximum XOR sum of exactly $K$ distinct elements from an array $A$ of size $N$. The key constraint provided is that the binomial coefficient $\binom{N}{K}$ is at most $10^6$. This constraint is crucial because it limits the search space significantly.

Normally, iterating through all subsets of size $K$ would be $O(\binom{N}{K} \cdot K)$. While $N$ can be up to $2 \times 10^5$, the condition $\binom{N}{K} \le 10^6$ implies that either $K$ is very small (e.g., $K=1$ or $K=2$) or $N$ is relatively small (e.g., $N \approx 22$ and $K \approx 11$). In the worst-case scenario where $\binom{N}{K} \approx 10^6$, the value of $K$ is small enough (around 10-15) such that the total number of operations ($\approx 10^6 \times 15$) is well within the typical time limit of 2 seconds for competitive programming (usually allowing $\sim 10^8$ operations).

Therefore, a brute-force approach using `itertools.combinations` is the most straightforward and efficient solution given the specific constraints. We iterate through every combination of $K$ elements, compute their XOR sum, and maintain the maximum value found.

## worker: Run the code against the provided sample inputs to
The code implements the brute-force approach using `itertools.combinations` as planned. The constraint $\binom{N}{K} \le 10^6$ guarantees that the number of iterations is manageable. The inner loop computes the XOR sum for each combination. The logic handles the input parsing correctly and updates the maximum XOR value found.
