
## ideation
The problem asks for the sum of scores of all "good" sequences $S$ satisfying local conditions $f(S_i/S_{i+1}) = A_i$ and a global condition $\gcd(S_1, \dots, S_N) = 1$.

1.  **Multiplicativity**: The function $f$ and the score product are multiplicative with respect to prime factors. We can decompose the problem by prime. For each prime $p$, let $k_i = v_p(A_i)$. We need to find the sum of $p^{\sum e_i}$ over all integer sequences $e_1, \dots, e_N$ such that $|e_i - e_{i+1}| = k_i$ and $\min(e_1, \dots, e_N) = 0$. The total answer is the product of these sums over all primes $p$ modulo 998244353.

2.  **Handling the Global GCD**: The condition $\gcd(S)=1$ translates to $\min_i v_p(S_i) = 0$ for every prime $p$. This allows us to solve the problem independently for each prime $p$ by enforcing the minimum exponent to be exactly 0.

3.  **DP Formulation for a Fixed Prime**:
    For a fixed prime $p$ and exponents $k_1, \dots, k_{N-1}$:
    - Let $e_i$ be the exponent of $p$ in $S_i$.
    - The condition is $|e_i - e_{i+1}| = k_i$.
    - We can express $e_i$ relative to $e_1$: $e_i = e_1 + \text{offset}_i$, where $\text{offset}_1 = 0$ and $\text{offset}_{i+1} = \text{offset}_i \pm k_i$.
    - The condition $\min_i e_i = 0$ implies $e_1 = -\min_i \text{offset}_i$.
    - The contribution to the score for a specific sign pattern (choice of $\pm$) is $p^{\sum e_i} = p^{N e_1 + \sum \text{offset}_i} = p^{-N \min_i \text{offset}_i + \sum \text{offset}_i}$.
    - We need to sum this value over all $2^{N-1}$ sign patterns.

4.  **Efficient Calculation**:
    - Since $N$ is up to 1000, we cannot iterate $2^{N-1}$.
    - We use Dynamic Programming. The state at step $i$ can be defined by the pair `(current_min_offset, current_offset)`.
    - `dp[min_off][curr_off]` stores the sum of $p^{\sum_{j=1}^i \text{offset}_j}$ for all partial paths ending at `curr_off` with minimum offset `min_off`.
    - Transitions: From state `(min_off, curr_off)` at step $i$, we go to step $i+1$ with two choices:
        - `next_off = curr_off + k_i`: `new_min = min(min_off, next_off)`. Add `dp[min_off][curr_off] * p^{next_off}` to `new_dp[new_min][next_off]`.
        - `next_off = curr_off - k_i`: `new_min = min(min_off, next_off)`. Add `dp[min_off][curr_off] * p^{next_off}` to `new_dp[new_min][next_off]`.
    - To manage the large range of offsets (which can be up to $N \times \max(k_i) \approx 10^6$), we use a hash map (dictionary) for the DP states at each step. The number of reachable states is often much smaller than the theoretical maximum due to merging of paths with same `(min, curr)`.
    - We only process primes that divide at least one $A_i$. For primes not dividing any $A_i$, the only valid sequence with min exponent 0 is all zeros, contributing a factor of 1.

5.  **Complexity**:
    - For each prime, the DP runs in $O(N \cdot |\text{States}|)$. The number of states is bounded by the number of distinct `(min, curr)` pairs. In practice, this is manageable.
    - The number of relevant primes is small (at most the number of distinct prime factors in all $A_i$, which is small since $A_i \le 1000$).

## worker: Parse input $N$ and $A$.
The solution decomposes the problem by prime factors due to the multiplicative nature of the score and the condition $f(S_i/S_{i+1}) = A_i$. For each prime $p$, we determine the possible valuations $v_p(S_i)$ such that $|v_p(S_i) - v_p(S_{i+1})| = v_p(A_i)$ and $\min_i v_p(S_i) = 0$. This is solved using dynamic programming where the state tracks the minimum offset and current offset relative to the first element. The global GCD condition $\gcd(S)=1$ is handled by enforcing the minimum valuation for each prime to be exactly 0. The results for each prime are multiplied together modulo 998244353.
