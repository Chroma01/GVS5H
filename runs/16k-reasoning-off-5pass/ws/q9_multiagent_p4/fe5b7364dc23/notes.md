
## ideation
**Core Difficulty**:
The problem asks for $\sum_{1\leq l\leq r\leq N} (\sum_{i=l}^r A_i)^K$. A naive $O(N^2)$ approach to iterate all subarrays is too slow given $N \le 2 \times 10^5$. The constraint $K \le 10$ is the key.

**Candidate Approaches**:
1.  **Multinomial Expansion**: Expand $(\sum_{i=l}^r A_i)^K = \sum_{i_1, \dots, i_K \in [l, r]} A_{i_1} A_{i_2} \dots A_{i_K}$.
    The total sum becomes $\sum_{l \le r} \sum_{i_1, \dots, i_K \in [l, r]} \prod_{j=1}^K A_{i_j}$.
    We can swap the summations: $\sum_{1 \le i_1, \dots, i_K \le N} (\prod_{j=1}^K A_{i_j}) \times (\text{number of subarrays } [l, r] \text{ containing all } i_j)$.
    For a fixed tuple $(i_1, \dots, i_K)$, let $L = \min(i_j)$ and $R = \max(i_j)$. The subarray $[l, r]$ must satisfy $l \le L$ and $R \le r$.
    The number of such subarrays is $L \times (N - R + 1)$.
    So the answer is $\sum_{i_1, \dots, i_K} (\prod A_{i_j}) \cdot (\min(i_j) \cdot (N - \max(i_j) + 1))$.

2.  **Optimization of Approach 1**:
    Directly iterating $N^K$ tuples is $O(N^{10})$, which is too slow. We need to group terms.
    Notice that the term depends on $\min(i_1, \dots, i_K)$ and $\max(i_1, \dots, i_K)$.
    Let's fix the minimum index $p$ and the maximum index $q$ (where $p \le q$).
    We need to sum $\prod A_{i_j}$ over all tuples where $\min = p$ and $\max = q$.
    This looks like inclusion-exclusion or dynamic programming.
    Alternatively, we can iterate over the position of the "first" element and "last" element in the sorted order of indices, but since indices are not necessarily sorted in the tuple, we can define:
    Let $S$ be the set of indices $\{i_1, \dots, i_K\}$. Let $p = \min(S)$ and $q = \max(S)$.
    We need to count tuples where all indices are in $[p, q]$, at least one is $p$, and at least one is $q$.
    Let $F(p, q) = \sum_{p \le i_1, \dots, i_K \le q} \prod A_{i_j} = (\sum_{i=p}^q A_i)^K$.
    Then the sum for fixed $p, q$ with exactly min $p$ and max $q$ is:
    $Term(p, q) = F(p, q) - F(p+1, q) - F(p, q-1) + F(p+1, q-1)$.
    (Standard inclusion-exclusion to enforce presence of $p$ and $q$).
    The total answer is $\sum_{1 \le p \le q \le N} Term(p, q) \cdot p \cdot (N - q + 1)$.

3.  **Complexity Analysis**:
    Calculating $F(p, q) = (\sum_{i=p}^q A_i)^K$ for all pairs $(p, q)$ takes $O(N^2)$ if we precompute prefix sums.
    $N=2 \times 10^5 \implies N^2 = 4 \times 10^{10}$, which is TLE.
    We need a faster way to compute $\sum_{p \le q} (S_q - S_{p-1})^K \cdot p \cdot (N - q + 1)$, where $S$ is the prefix sum array.
    Let $X = S_q - S_{p-1}$. We need $\sum_{p \le q} (S_q - S_{p-1})^K \cdot p \cdot (N - q + 1)$.
    This still looks like $O(N^2)$. Is there a way to do it in $O(N \cdot K)$ or $O(N \log N)$?
    
    Wait, the constraints say $K \le 10$. Maybe we can expand $(S_q - S_{p-1})^K$ using binomial theorem?
    $(S_q - S_{p-1})^K = \sum_{j=0}^K \binom{K}{j} S_q^j (-S_{p-1})^{K-j}$.
    Substitute this back:
    Sum $= \sum_{p \le q} \sum_{j=0}^K \binom{K}{j} S_q^j (-1)^{K-j} S_{p-1}^{K-j} \cdot p \cdot (N - q + 1)$.
    Swap sums:
    $= \sum_{j=0}^K \binom{K}{j} (-1)^{K-j} \left[ \sum_{q=1}^N S_q^j (N - q + 1) \sum_{p=1}^q p S_{p-1}^{K-j} \right]$.
    
    Now the inner part is $\sum_{q=1}^N S_q^j (N - q + 1) \left( \sum_{p=1}^q p S_{p-1}^{K-j} \right)$.
    Let $T_{k} = \sum_{p=1}^q p S_{p-1}^{k}$. This can be computed incrementally as we iterate $q$ from $1$ to $N$.
    For each $q$, we update $T_0, T_1, \dots, T_K$.
    Then we compute the contribution for this $q$ to the total sum.
    Total complexity: $O(N \cdot K)$.
    Given $N=2 \times 10^5$ and $K=10$, operations $\approx 2 \times 10^6$, which is well within the time limit (usually $\sim 10^8$ ops/sec).

## worker: Implement the $O(N \cdot K)$ solution using the bi
1.  **Problem Analysis**: The problem asks for the sum of the $K$-th power of all contiguous subarray sums. The constraints are $N \le 2 \times 10^5$ and $K \le 10$. A naive $O(N^2)$ solution is too slow.
2.  **Mathematical Transformation**:
    *   Let $S$ be the prefix sum array of $A$. The sum of a subarray $A[l \dots r]$ is $S[r] - S[l-1]$.
    *   We need to compute $\sum_{1 \le l \le r \le N} (S[r] - S[l-1])^K$.
    *   Let $p = l$ and $q = r$. The range is $1 \le p \le q \le N$.
    *   The term becomes $(S[q] - S[p-1])^K$.
    *   Using the Binomial Theorem: $(S[q] - S[p-1])^K = \sum_{j=0}^K \binom{K}{j} S[q]^j (-S[p-1])^{K-j}$.
    *   Substituting this into the total sum:
        $$ \sum_{q=1}^N \sum_{p=1}^q \left( \sum_{j=0}^K \binom{K}{j} S[q]^j (-1)^{K-j} S[p-1]^{K-j} \right) $$
    *   Rearranging the summations:
        $$ \sum_{q=1}^N \sum_{j=0}^K \binom{K}{j} (-1)^{K-j} S[q]^j \left( \sum_{p=1}^q S[p-1]^{K-j} \right) $$
    *   Wait, the original problem includes the weight $p \cdot (N - q + 1)$? No, looking back at the derivation in the thought process:
        The problem is $\sum_{l \le r} (\sum_{i=l}^r A_i)^K$.
        My initial thought process had a detour involving counting subarrays containing specific indices, which led to the formula $\sum_{p \le q} (\sum_{i=p}^q A_i)^K \cdot p \cdot (N-q+1)$?
        **Correction**: The problem is simply $\sum_{1 \le l \le r \le N} (\text{sum}(l, r))^K$. There is no extra weight $p \cdot (N-q+1)$.
        Let's re-verify the sample.
        Sample 1: N=3, K=2, A=[3, 1, 2].
        Subarrays:
        [3] -> 3^2 = 9
        [1] -> 1^2 = 1
        [2] -> 2^2 = 4
        [3, 1] -> 4^2 = 16
        [1, 2] -> 3^2 = 9
        [3, 1, 2] -> 6^2 = 36
        Total = 9+1+4+16+9+36 = 75. Correct.
        
        So the formula is simply $\sum_{1 \le p \le q \le N} (S[q] - S[p-1])^K$.
        There is no $p \cdot (N-q+1)$ factor. That factor appeared in a different problem variant (counting occurrences of index tuples).
        
        So the correct expansion is:
        $$ \text{Ans} = \sum_{q=1}^N \sum_{p=1}^q (S[q] - S[p-1])^K $$
        $$ = \sum_{q=1}^N \sum_{j=0}^K \binom{K}{j} S[q]^j (-1)^{K-j} \left( \sum_{p=1}^q S[p-1]^{K-j} \right) $$
        
        Let $Inner[k] = \sum_{p=1}^q S[p-1]^k$.
        As we iterate $q$ from 1 to $N$:
        1. Update $Inner[k]$ for all $k \in [0, K]$ by adding $S[q-1]^k$.
        2. Compute contribution for current $q$: $\sum_{j=0}^K \binom{K}{j} S[q]^j (-1)^{K-j} Inner[K-j]$.
        3. Add to total answer.
        
        Complexity: $O(N \cdot K)$. With $N=2 \cdot 10^5, K=10$, operations $\approx 2 \cdot 10^6$, which is very fast.

3.  **Implementation Details**:
    *   Read input efficiently.
    *   Compute prefix sums modulo 998244353.
    *   Precompute binomial coefficients $\binom{K}{j}$.
    *   Loop $q$ from 1 to $N$.
    *   Maintain `inner_sum` array where `inner_sum[k]` holds $\sum_{p=1}^q S[p-1]^k$.
    *   In each step, update `inner_sum` by adding powers of $S[q-1]$.
    *   Calculate the term for $q$ using the expanded binomial sum.
    *   Accumulate result modulo 998244353.

4.  **Edge Cases**:
    *   $K=1$: Linear sum of subarrays.
    *   $A_i = 0$: Handled correctly by modulo arithmetic.
    *   $N=1$: Single element.

The code implements this logic. I will correct the code to remove the erroneous weight factor $p \cdot (N-q+1)$ and the complex inclusion-exclusion logic that was based on a misinterpretation of the problem statement (confusing it with a "counting tuples" problem). The problem is a direct summation of powers of subarray sums.

## worker: Implement the corrected $O(N \cdot K)$ solution in
The problem asks for $\sum_{1\leq l\leq r\leq N} (\sum_{i=l}^r A_i)^K \pmod{998244353}$.
Let $S$ be the prefix sum array where $S[i] = \sum_{k=0}^{i-1} A_k$. Then the sum of subarray $A[l \dots r]$ is $S[r] - S[l-1]$.
The problem becomes computing $\sum_{1 \leq p \leq q \leq N} (S[q] - S[p-1])^K$.
Using the Binomial Theorem, $(S[q] - S[p-1])^K = \sum_{j=0}^K \binom{K}{j} S[q]^j (-1)^{K-j} S[p-1]^{K-j}$.
Substituting this into the total sum and swapping the order of summation:
$$ \text{Ans} = \sum_{q=1}^N \sum_{j=0}^K \binom{K}{j} (-1)^{K-j} S[q]^j \left( \sum_{p=1}^q S[p-1]^{K-j} \right) $$
Let $Inner[k] = \sum_{p=1}^q S[p-1]^k$. As we iterate $q$ from $1$ to $N$, we can maintain $Inner[k]$ by adding $S[q-1]^k$ to each $Inner[k]$.
The complexity is $O(N \cdot K)$, which fits well within the time limits for $N=2 \times 10^5$ and $K=10$.
The previous code draft had an incorrect weight factor $p \cdot (N-q+1)$ which was removed to match the problem statement.

## worker: Run the code against the provided sample inputs to
The code implements the $O(N \cdot K)$ solution derived from the binomial expansion of the subarray sum power.
1.  **Input Parsing**: Reads $N, K$ and the sequence $A$.
2.  **Prefix Sums**: Computes prefix sums $S$ modulo 998244353.
3.  **Binomial Coefficients**: Precomputes $\binom{K}{j}$ since $K$ is small.
4.  **Iterative Calculation**:
    *   Maintains `inner_sum[k]` which stores $\sum_{p=1}^q S[p-1]^k$.
    *   For each $q$ from 1 to $N$, updates `inner_sum` by adding $S[q-1]^k$.
    *   Computes the contribution of the current $q$ using the expanded binomial formula: $\sum_{j=0}^K \binom{K}{j} S[q]^j (-1)^{K-j} \text{inner\_sum}[K-j]$.
    *   Accumulates the result modulo 998244353.
5.  **Complexity**: $O(N \cdot K)$ time, $O(N + K)$ space. With $N=2 \cdot 10^5$ and $K=10$, this is efficient.

## worker: Run the provided sample inputs to verify correctne
The solution implements an $O(N \cdot K)$ algorithm based on the Binomial Theorem.
1.  **Problem Transformation**: The problem asks for $\sum_{1 \le l \le r \le N} (\sum_{i=l}^r A_i)^K$. Let $S$ be the prefix sum array. The inner sum is $S[r] - S[l-1]$.
2.  **Binomial Expansion**: We expand $(S[r] - S[l-1])^K = \sum_{j=0}^K \binom{K}{j} S[r]^j (-1)^{K-j} S[l-1]^{K-j}$.
3.  **Rearrangement**: The total sum becomes $\sum_{r=1}^N \sum_{j=0}^K \binom{K}{j} (-1)^{K-j} S[r]^j \left( \sum_{l=1}^r S[l-1]^{K-j} \right)$.
4.  **Efficient Calculation**: We iterate $r$ from $1$ to $N$. We maintain an array `inner_sum` where `inner_sum[k]` stores $\sum_{l=1}^r S[l-1]^k$. In each step, we update `inner_sum` by adding $S[r-1]^k$ for all $k$, and then compute the contribution of the current $r$ using the precomputed `inner_sum` values and powers of $S[r]$.
5.  **Complexity**: With $N \le 2 \times 10^5$ and $K \le 10$, the total operations are roughly $2 \times 10^6$, which is well within the time limit.

## worker: finalize
The solution implements an $O(N \cdot K)$ algorithm based on the Binomial Theorem.
1.  **Problem Transformation**: The problem asks for $\sum_{1 \le l \le r \le N} (\sum_{i=l}^r A_i)^K$. Let $S$ be the prefix sum array where $S[i] = \sum_{k=0}^{i-1} A_k$. The inner sum is $S[r] - S[l-1]$.
2.  **Binomial Expansion**: We expand $(S[r] - S[l-1])^K = \sum_{j=0}^K \binom{K}{j} S[r]^j (-1)^{K-j} S[l-1]^{K-j}$.
3.  **Rearrangement**: The total sum becomes $\sum_{r=1}^N \sum_{j=0}^K \binom{K}{j} (-1)^{K-j} S[r]^j \left( \sum_{l=1}^r S[l-1]^{K-j} \right)$.
4.  **Efficient Calculation**: We iterate $r$ from $1$ to $N$. We maintain an array `inner_sum` where `inner_sum[k]` stores $\sum_{l=1}^r S[l-1]^k$. In each step, we update `inner_sum` by adding $S[r-1]^k$ for all $k$, and then compute the contribution of the current $r$ using the precomputed `inner_sum` values and powers of $S[r]$.
5.  **Complexity**: With $N \le 2 \times 10^5$ and $K \le 10$, the total operations are roughly $2 \times 10^6$, which is well within the time limit.
