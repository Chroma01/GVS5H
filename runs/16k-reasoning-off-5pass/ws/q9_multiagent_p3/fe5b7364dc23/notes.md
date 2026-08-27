
## ideation
**Core Difficulty:**
The problem requires calculating $\sum_{1\leq l\leq r\leq N} (\sum_{i=l}^r A_i)^K$ efficiently. A naive $O(N^2)$ approach to iterate all subarrays and compute the sum is too slow given $N \le 2 \times 10^5$. The constraint $K \le 10$ is the key hint.

**Candidate Approaches:**
1.  **Multinomial Expansion (Stars and Bars / Combinatorics):**
    Expand $(\sum_{i=l}^r A_i)^K$ using the multinomial theorem:
    $$ \left(\sum_{i=l}^r A_i\right)^K = \sum_{k_1 + \dots + k_r = K} \frac{K!}{k_1! \dots k_r!} \prod_{j=l}^r A_j^{k_j} $$
    Summing this over all $1 \le l \le r \le N$ involves summing over all possible subarrays and all partitions of $K$.
    Instead of iterating subarrays, we can iterate over the *structure* of the partition of $K$.
    Let's define a state based on how many times each element is "selected" in the expansion. However, a more direct combinatorial interpretation is often used in similar problems:
    Consider the contribution of a specific term $A_{i_1}^{p_1} A_{i_2}^{p_2} \dots A_{i_m}^{p_m}$ where $i_1 < i_2 < \dots < i_m$ are distinct indices and $\sum p_j = K$.
    For this term to appear in the expansion of a subarray sum $(A_l + \dots + A_r)^K$, the subarray $[l, r]$ must contain all indices $i_1, \dots, i_m$.
    Specifically, $l \le i_1$ and $r \ge i_m$.
    The number of such subarrays is $i_1 \times (N - i_m + 1)$.
    Wait, this logic applies if we are summing products of distinct elements. But the expansion allows picking the *same* index multiple times (e.g., $A_i^2$).
    
    Let's refine the expansion approach. We are summing over all subarrays $[l, r]$.
    $$ \text{Ans} = \sum_{1\le l \le r \le N} \sum_{j_1, \dots, j_K \in [l, r]} \prod_{t=1}^K A_{j_t} $$
    We can swap the summations:
    $$ \text{Ans} = \sum_{j_1, \dots, j_K} \left( \prod_{t=1}^K A_{j_t} \right) \times (\text{number of subarrays } [l, r] \text{ such that } \forall t, l \le j_t \le r) $$
    The condition "$\forall t, l \le j_t \le r$" is equivalent to $l \le \min(j_1, \dots, j_K)$ and $r \ge \max(j_1, \dots, j_K)$.
    Let $L = \min(j_1, \dots, j_K)$ and $R = \max(j_1, \dots, j_K)$.
    The number of valid subarrays is $L \times (N - R + 1)$.
    
    So the problem reduces to:
    $$ \sum_{1 \le j_1, \dots, j_K \le N} \left( \prod_{t=1}^K A_{j_t} \right) \cdot (\min(j_1, \dots, j_K) \cdot (N - \max(j_1, \dots, j_K) + 1)) $$
    
    Since $K$ is small ($K \le 10$), we can try to compute this by iterating over the possible values of the minimum and maximum indices, or by using dynamic programming.
    
    **DP Approach:**
    Let's fix the minimum index $l$ and the maximum index $r$. Then we need to count the number of sequences $j_1, \dots, j_K$ such that $\min(j) = l$ and $\max(j) = r$.
    This seems complicated because the product depends on the specific values.
    
    **Alternative DP State:**
    Iterate $i$ from $1$ to $N$. We want to maintain information about sequences ending at or before $i$.
    Actually, let's look at the structure of the sum again.
    We are summing $A_{j_1} \dots A_{j_K} \cdot \min(j) \cdot (N - \max(j) + 1)$.
    Let's define $S = \sum_{j_1, \dots, j_K} (\prod A_{j_t}) \cdot f(\min, \max)$.
    This looks like we can iterate the "active" range $[l, r]$ and count contributions where the min is $l$ and max is $r$.
    For a fixed pair $(l, r)$ with $l \le r$:
    We need sequences of length $K$ where every element is in $[l, r]$, at least one is $l$, and at least one is $r$.
    Total sequences in $[l, r]$ is $(\sum_{x=l}^r A_x)^K$.
    Subtract sequences that don't include $l$ (all in $[l+1, r]$) and don't include $r$ (all in $[l, r-1]$).
    Add back sequences that include neither (all in $[l+1, r-1]$).
    So contribution for fixed $(l, r)$ is:
    $C(l, r) = (\sum_{x=l}^r A_x)^K - (\sum_{x=l+1}^r A_x)^K - (\sum_{x=l}^{r-1} A_x)^K + (\sum_{x=l+1}^{r-1} A_x)^K$.
    Then the answer is $\sum_{1 \le l \le r \le N} C(l, r) \cdot l \cdot (N - r + 1)$.
    
    Complexity: $O(N^2)$ is still too slow. We need $O(N \cdot K)$ or $O(N)$.
    Since $K$ is small, maybe we can use DP to compute the sum of powers of subarray sums?
    Wait, the formula derived above:
    $\sum_{l, r} l(N-r+1) [ (\sum_{l}^r A)^K - \dots ]$
    This is exactly $\sum_{l, r} l(N-r+1) (\sum_{l}^r A)^K - \text{correction terms}$.
    The correction terms are just sums over smaller ranges.
    Essentially, we need to calculate $T(l, r) = (\sum_{i=l}^r A_i)^K$ efficiently for all $l, r$? No, that's $O(N^2)$.
    
    Let's reconsider the DP state.
    We want to compute $\sum_{1 \le j_1, \dots, j_K \le N} (\prod A_{j_t}) \cdot \min(j) \cdot (N - \max(j) + 1)$.
    Let's iterate $i$ from $1$ to $N$ as the current maximum index $R$.
    Suppose we fix $R = i$. We need to sum over all sequences $j_1, \dots, j_K$ where $\max(j) = i$.
    This means all $j_t \le i$, and at least one $j_t = i$.
    Let $P_i = \prod_{t=1}^K A_{j_t}$.
    Sum over sequences with all $j_t \le i$ is $(\sum_{x=1}^i A_x)^K$.
    Sum over sequences with all $j_t \le i-1$ is $(\sum_{x=1}^{i-1} A_x)^K$.
    So sum of products where $\max(j) = i$ is $S_i^K - S_{i-1}^K$, where $S_i = \sum_{x=1}^i A_x$.
    But we also have the factor $\min(j)$.
    Let $dp[i][k]$ be the sum of $\prod_{t=1}^k A_{j_t} \cdot \min(j_1, \dots, j_k)$ for sequences where all indices are $\le i$ and $\max(j) = i$?
    This seems to require tracking the minimum.
    
    Let's try a different DP.
    Let $dp[i]$ be a vector of size $K+1$? No.
    Let's go back to the expansion:
    $\sum_{j_1, \dots, j_K} (\prod A_{j_t}) \min(j) (N - \max(j) + 1)$.
    Let's fix the minimum index $l$ and the maximum index $r$.
    We need to sum $\prod A_{j_t}$ over sequences where $\min=j=l, \max=j=r$.
    This is equivalent to: (sequences in $[l, r]$) - (sequences in $[l+1, r]$) - (sequences in $[l, r-1]$) + (sequences in $[l+1, r-1]$).
    Let $F(l, r) = (\sum_{x=l}^r A_x)^K$.
    Contribution = $l(N-r+1) [ F(l, r) - F(l+1, r) - F(l, r-1) + F(l+1, r-1) ]$.
    Sum over $1 \le l \le r \le N$.
    This can be rewritten as:
    $\sum_{l=1}^N \sum_{r=l}^N l(N-r+1) F(l, r) - \sum_{l=1}^N \sum_{r=l+1}^N l(N-r+1) F(l+1, r) - \dots$
    This looks like we can shift indices.
    Let $S(l, r) = (\sum_{x=l}^r A_x)^K$.
    We need $\sum_{l, r} l(N-r+1) S(l, r)$.
    Can we compute this in $O(N)$?
    $S(l, r)$ is the K-th power of a subarray sum.
    If we expand $S(l, r)$ using multinomial theorem:
    $S(l, r) = \sum_{c_1 + \dots + c_r = K} \frac{K!}{c_1! \dots c_r!} \prod_{i=l}^r A_i^{c_i}$.
    Then $\sum_{l, r} l(N-r+1) S(l, r) = \sum_{l, r} l(N-r+1) \sum_{\mathbf{c}} \text{coeff} \prod A_i^{c_i}$.
    Swap sums: $\sum_{\mathbf{c}} \text{coeff} \sum_{l, r} l(N-r+1) \prod_{i=l}^r A_i^{c_i}$.
    The inner sum is over subarrays containing the support of $\mathbf{c}$.
    Let the indices present in $\mathbf{c}$ (where $c_i > 0$) be $idx_1 < idx_2 < \dots < idx_m$.
    Then $l \le idx_1$ and $r \ge idx_m$.
    The term $\prod A_i^{c_i}$ is constant for these $l, r$.
    Sum over $l \in [1, idx_1]$ and $r \in [idx_m, N]$ of $l(N-r+1)$.
    $\sum_{l=1}^{idx_1} l \times \sum_{r=idx_m}^N (N-r+1) = \frac{idx_1(idx_1+1)}{2} \times \frac{(N-idx_m+1)(N-idx_m+2)}{2}$.
    So the algorithm would be:
    1. Iterate over all compositions of $K$ into $N$ parts (or rather, all ways to assign counts $c_1, \dots, c_N$ summing to $K$).
    2. For each composition, identify the first non-zero index $L$ and last non-zero index $R$.
    3. Calculate the product term and the combinatorial coefficient.
    4. Add $coeff \times \text{product} \times \frac{L(L+1)}{2} \times \frac{(N-R+1)(N-R+2)}{2}$ to the total.
    
    How many compositions? This is equivalent to distributing $K$ items into $N$ bins. Stars and bars: $\binom{N+K-1}{K}$.
    With $N=2 \cdot 10^5, K=10$, this is huge. We cannot iterate all compositions.
    
    **Backtrack to DP:**
    We need to compute $\sum_{\mathbf{c}} \binom{K}{\mathbf{c}} (\prod A_i^{c_i}) \times \text{Weight}(L(\mathbf{c}), R(\mathbf{c}))$.
    Where $L(\mathbf{c}) = \min \{ i : c_i > 0 \}$ and $R(\mathbf{c}) = \max \{ i : c_i > 0 \}$.
    Let's process from left to right.
    State: $dp[i][k]$ = sum of terms for sequences using indices $1 \dots i$ with total count $k$.
    But we need to know the *first* non-zero index to calculate the weight.
    Let's define:
    $dp[i][k]$: Sum of $(\prod_{j=1}^i A_j^{c_j}) \times (\text{something})$ for sequences of length $k$ using indices from $1 \dots i$.
    Actually, let's separate the "first" and "last" logic.
    The weight is $W(L, R) = \frac{L(L+1)}{2} \frac{(N-R+1)(N-R+2)}{2}$.
    Note that $W(L, R) = (\sum_{x=1}^L x) \times (\sum_{y=R}^N (N-y+1))$.
    Let $Pre[x] = x(x+1)/2$ and $Suf[x] = (N-x+1)(N-x+2)/2$.
    We need $\sum_{\mathbf{c}} \binom{K}{\mathbf{c}} (\prod A_i^{c_i}) Pre[L(\mathbf{c})] Suf[R(\mathbf{c})]$.
    
    Let's iterate $i$ from $1$ to $N$.
    We maintain a DP state that tracks the sum of products for sequences of length $k$ ending at or before $i$, but we need to handle the $L$ and $R$ constraints.
    Actually, we can iterate $i$ as the current position, and decide whether $i$ is the last non-zero index ($R=i$) or not.
    Similarly for $L$.
    
    Let's try to compute $Ans = \sum_{L=1}^N Pre[L] \sum_{R=L}^N Suf[R] \times (\text{Sum of products where } \min=L, \max=R)$.
    Let $G(L, R) = \sum_{\mathbf{c}: \min=L, \max=R} \binom{K}{\mathbf{c}} \prod A_i^{c_i}$.
    We know $G(L, R) = (\sum_{x=L}^R A_x)^K - (\sum_{x=L+1}^R A_x)^K - (\sum_{x=L}^{R-1} A_x)^K + (\sum_{x=L+1}^{R-1} A_x)^K$.
    So $Ans = \sum_{L=1}^N Pre[L] \sum_{R=L}^N Suf[R] [ S(L, R)^K - S(L+1, R)^K - S(L, R-1)^K + S(L+1, R-1)^K ]$.
    This can be rearranged:
    $Ans = \sum_{L, R} Pre[L] Suf[R] S(L, R)^K - \sum_{L, R} Pre[L] Suf[R] S(L+1, R)^K - \dots$
    Let's analyze the first term: $T_1 = \sum_{L=1}^N \sum_{R=L}^N Pre[L] Suf[R] S(L, R)^K$.
    This is $\sum_{L, R} Pre[L] Suf[R] (\sum_{x=L}^R A_x)^K$.
    Can we compute this efficiently?
    Expand $(\sum_{x=L}^R A_x)^K$ using DP.
    Let $dp[i][k]$ be the sum of $(\sum_{x=1}^i A_x)^k$? No.
    We need to sum over all subarrays.
    Let's use the property that $(\sum_{x=L}^R A_x)^K = \sum_{j_1, \dots, j_K \in [L, R]} \prod A_{j_t}$.
    Then $T_1 = \sum_{L, R} Pre[L] Suf[R] \sum_{j_1, \dots, j_K \in [L, R]} \prod A_{j_t}$.
    Swap sums: $\sum_{j_1, \dots, j_K} (\prod A_{j_t}) \sum_{L=1}^{\min(j)} \sum_{R=\max(j)}^N Pre[L] Suf[R]$.
    The inner sum is $Pre[\min(j)] \times Suf[\max(j)]$.
    This brings us back to the original formulation: $\sum_{\mathbf{j}} (\prod A_{j_t}) Pre[\min(\mathbf{j})] Suf[\max(\mathbf{j})]$.
    
    So the problem is strictly: Compute $\sum_{j_1, \dots, j_K} (\prod A_{j_t}) Pre[\min(j)] Suf[\max(j)]$.
    Let's use DP.
    Iterate $i$ from $1$ to $N$.
    We want to maintain the sum of products for sequences of length $k$ ($1 \le k \le K$) formed by indices $\le i$.
    However, we need to distinguish between sequences where the current index $i$ is the *first* non-zero (for $Pre$) and the *last* non-zero (for $Suf$).
    
    Let's define:
    $dp[k]$: Sum of $\prod A_{j_t}$ for sequences of length $k$ using indices from $1 \dots i$, where we track the minimum index encountered so far?
    Actually, we can process the "first" index separately.
    Let's iterate $L$ from $1$ to $N$. Assume $L$ is the minimum index.
    Then we consider sequences where all indices are $\ge L$, and at least one is $L$.
    Let $Q(L, R) = \sum_{\mathbf{j}: \min=L, \max=R} (\prod A_{j_t})$.
    We need $\sum_{L, R} Q(L, R) Pre[L] Suf[R]$.
    We can compute $Q(L, R)$ efficiently?
    $Q(L, R) = (\sum_{x=L}^R A_x)^K - (\sum_{x=L+1}^R A_x)^K - (\sum_{x=L}^{R-1} A_x)^K + (\sum_{x=L+1}^{R-1} A_x)^K$.
    So $Ans = \sum_{L=1}^N Pre[L] \sum_{R=L}^N Suf[R] [ (\sum_{x=L}^R A_x)^K - (\sum_{x=L+1}^R A_x)^K - (\sum_{x=L}^{R-1} A_x)^K + (\sum_{x=L+1}^{R-1} A_x)^K ]$.
    Let $S_i = \sum_{x=1}^i A_x$. Then $\sum_{x=L}^R A_x = S_R - S_{L-1}$.
    Term becomes $(S_R - S_{L-1})^K$.
    $Ans = \sum_{L=1}^N Pre[L] \sum_{R=L}^N Suf[R] [ (S_R - S_{L-1})^K - (S_R - S_L)^K - (S_{R-1} - S_{L-1})^K + (S_{R-1} - S_L)^K ]$.
    This looks like $O(N^2)$ if computed naively.
    But notice the structure:
    $\sum_{L, R} Pre[L] Suf[R] (S_R - S_{L-1})^K$.
    Let $f(L, R) = (S_R - S_{L-1})^K$.
    We need $\sum_{L, R} Pre[L] Suf[R] f(L, R)$.
    Can we compute this in $O(N \cdot K)$?
    Expand $(S_R - S_{L-1})^K = \sum_{t=0}^K \binom{K}{t} S_R^t (-S_{L-1})^{K-t}$.
    Then sum becomes:
    $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} \left( \sum_{L=1}^N Pre[L] S_{L-1}^{K-t} \right) \left( \sum_{R=L}^N Suf[R] S_R^t \right)$.
    Wait, the second sum depends on $L$ ($R \ge L$). This dependency prevents simple separation.
    However, we can rewrite the double sum:
    $\sum_{L=1}^N Pre[L] \sum_{R=L}^N Suf[R] \sum_{t=0}^K \binom{K}{t} S_R^t (-S_{L-1})^{K-t}$.
    $= \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} \sum_{L=1}^N Pre[L] S_{L-1}^{K-t} \left( \sum_{R=L}^N Suf[R] S_R^t \right)$.
    Let $Inner(t, L) = \sum_{R=L}^N Suf[R] S_R^t$.
    We can precompute $Inner(t, L)$ for all $L, t$ in $O(N \cdot K)$ by iterating $L$ from $N$ down to $1$.
    $Inner(t, L) = Suf[L] S_L^t + Inner(t, L+1)$.
    Base case: $Inner(t, N+1) = 0$.
    Then the total complexity is $O(N \cdot K)$.
    This is perfect! $N=2 \cdot 10^5, K=10 \implies 2 \cdot 10^6$ operations.
    
    We need to handle the four terms in the bracket separately or combine them?
    The bracket was: $(S_R - S_{L-1})^K - (S_R - S_L)^K - (S_{R-1} - S_{L-1})^K + (S_{R-1} - S_L)^K$.
    This corresponds to:
    1. $L' = L, R' = R$
    2. $L' = L+1, R' = R$
    3. $L' = L, R' = R-1$
    4. $L' = L+1, R' = R-1$
    
    Actually, let's just compute the contribution of $(S_R - S_{L-1})^K$ for all $1 \le L \le R \le N$.
    Let $Term1 = \sum_{L=1}^N \sum_{R=L}^N Pre[L] Suf[R] (S_R - S_{L-1})^K$.
    Similarly for the other three terms, but note the ranges:
    - Term 2: $L$ goes $1 \dots N$, $R$ goes $L+1 \dots N$. (Since $L+1 \le R$).
    - Term 3: $L$ goes $1 \dots N$, $R$ goes $L \dots N-1$. (Since $L \le R-1$).
    - Term 4: $L$ goes $1 \dots N$, $R$ goes $L+1 \dots N-1$.
    
    Wait, the formula for $Q(L, R)$ is valid only if $L \le R$.
    If $L > R$, the range is empty, sum is 0.
    So:
    $Ans = \sum_{L=1}^N \sum_{R=L}^N Pre[L] Suf[R] (S_R - S_{L-1})^K$
          $- \sum_{L=1}^N \sum_{R=L+1}^N Pre[L] Suf[R] (S_R - S_L)^K$
          $- \sum_{L=1}^N \sum_{R=L}^{N-1} Pre[L] Suf[R] (S_{R-1} - S_{L-1})^K$
          $+ \sum_{L=1}^N \sum_{R=L+1}^{N-1} Pre[L] Suf[R] (S_{R-1} - S_L)^K$.
    
    We can define a helper function `calc(offset_L, offset_R)` which computes $\sum_{L=1}^N \sum_{R=L+offset_L}^{N+offset_R} Pre[L] Suf[R] (S_{R-offset_R} - S_{L-offset_L})^K$.
    Actually, simpler:
    Define a function `solve(l_start, r_end, shift_L, shift_R)`:
    Sum over $L \in [1, N], R \in [l\_start, r\_end]$ such that $L \le R$.
    Wait, the bounds are specific.
    Let's just implement 4 loops or a generalized loop.
    General form: $\sum_{L=1}^N Pre[L] \sum_{R=\max(L, A)}^B Suf[R] (S_R - S_{L+C})^K$.
    Actually, let's just hardcode the 4 cases to avoid confusion.
    
    Case 1: $1 \le L \le R \le N$. Term: $(S_R - S_{L-1})^K$.
    Case 2: $1 \le L < R \le N$. Term: $(S_R - S_L)^K$. (Subtract this)
    Case 3: $1 \le L \le R < N$. Term: $(S_{R-1} - S_{L-1})^K$. (Subtract this)
    Case 4: $1 \le L < R < N$. Term: $(S_{R-1} - S_L)^K$. (Add this)
    
    Algorithm:
    1. Precompute prefix sums $S_i$.
    2. Precompute $Pre[i] = i(i+1)/2$ and $Suf[i] = (N-i+1)(N-i+2)/2$.
    3. Precompute powers of $S_i$: $P_{i, t} = S_i^t$ for $t \in [0, K]$.
    4. For a fixed $t$, we need $\sum_{L} Pre[L] S_{L+C}^{K-t} \sum_{R} Suf[R] S_R^t$.
       But the inner sum depends on $L$ (range $R \ge L$).
       Let $Inner[t][L] = \sum_{R=L}^N Suf[R] S_R^t$.
       Compute this for all $L \in [1, N+1]$ and $t \in [0, K]$ in $O(NK)$.
       Iterate $L$ from $N$ down to $1$.
       $Inner[t][L] = (Suf[L] * S_L^t + Inner[t][L+1]) \% MOD$.
    5. Define a function `compute(l_min, r_max, shift_L, shift_R)`:
       We want $\sum_{L=1}^N Pre[L] \sum_{R=\max(L, l\_min)}^{r\_max} Suf[R] (S_R - S_{L+shift\_L})^K$.
       Wait, the shifts in the terms are:
       Term 1: $S_R - S_{L-1}$. Here $L$ is original $L$. $R$ is original $R$. Range $L \le R$.
       Term 2: $S_R - S_L$. Here $L$ is original $L$. $R$ is original $R$. Range $L < R$.
       Term 3: $S_{R-1} - S_{L-1}$. Here $L$ is original $L$. $R$ is original $R$. Range $L \le R-1 \implies L+1 \le R$.
       Term 4: $S_{R-1} - S_L$. Range $L < R-1 \implies L+2 \le R$.
       
       Let's unify.
       We need to compute $\sum_{L} Pre[L] \sum_{R} Suf[R] (S_R - S_{L+C})^K$ where the sum is over $R \in [\max(L, A), B]$.
       Actually, let's just implement the expansion for each term individually.
       
       For Term 1: $C = -1$. Range $R \in [L, N]$.
       Sum = $\sum_{L=1}^N Pre[L] \sum_{R=L}^N Suf[R] (S_R - S_{L-1})^K$.
       Expand: $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} S_{L-1}^{K-t} \sum_{R=L}^N Suf[R] S_R^t$.
       The inner sum is exactly $Inner[t][L]$.
       So Term 1 = $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} \sum_{L=1}^N Pre[L] S_{L-1}^{K-t} Inner[t][L]$.
       
       For Term 2: $C = 0$. Range $R \in [L+1, N]$.
       Sum = $\sum_{L=1}^N Pre[L] \sum_{R=L+1}^N Suf[R] (S_R - S_L)^K$.
       Inner sum is $\sum_{R=L+1}^N Suf[R] S_R^t = Inner[t][L+1]$.
       Term 2 = $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} \sum_{L=1}^N Pre[L] S_L^{K-t} Inner[t][L+1]$.
       
       For Term 3: $C = -1$. Range $R \in [L, N-1]$.
       Sum = $\sum_{L=1}^N Pre[L] \sum_{R=L}^{N-1} Suf[R] (S_{R-1} - S_{L-1})^K$.
       Let $R' = R-1$. Range $R' \in [L-1, N-2]$. But $Suf[R]$ becomes $Suf[R'+1]$.
       This changes the structure.
       Maybe it's better to stick to the original $S_R$ form and adjust indices.
       Term 3: $(S_{R-1} - S_{L-1})^K$. Let $j = R-1$. Then $R = j+1$.
       Sum over $L \le j+1 \implies L \le j+1$. And $R \le N-1 \implies j \le N-2$.
       Also $R \ge L \implies j+1 \ge L$.
       So $j$ ranges from $L-1$ to $N-2$.
       Sum = $\sum_{L=1}^N Pre[L] \sum_{j=L-1}^{N-2} Suf[j+1] (S_j - S_{L-1})^K$.
       Expand: $\sum_{t} \binom{K}{t} (-1)^{K-t} S_{L-1}^{K-t} \sum_{j=L-1}^{N-2} Suf[j+1] S_j^t$.
       Let $Inner2[t][L] = \sum_{j=L-1}^{N-2} Suf[j+1] S_j^t$.
       We can precompute this similarly.
       
       This is getting slightly messy with indices.
       Alternative: Just run the $O(NK)$ logic 4 times with adjusted arrays.
       Define a function `calc(A, B, C, D)` which computes $\sum_{L=1}^N Pre[L] \sum_{R=\max(L, A)}^B Suf[R] (S_R - S_{L+C})^K$.
       Wait, $S_{L+C}$ might be out of bounds if $L+C < 1$ or $L+C > N$.
       In our cases:
       1. $C=-1$. $L \ge 1 \implies L-1 \ge 0$. $S_0 = 0$. OK. $R \ge L$. $B=N$. $A=L$.
       2. $C=0$. $L \ge 1$. $R \ge L+1$. $B=N$. $A=L+1$.
       3. $C=-1$. $S_{R-1}$. Let $R' = R-1$. $Suf[R] = Suf[R'+1]$.
          Sum over $L \le R' + 1 \implies L-1 \le R'$. $R' \le N-2$.
          $R' \ge L-1$.
          So sum over $R' \in [\max(L-1, -\infty), N-2]$.
          Term: $Pre[L] Suf[R'+1] (S_{R'} - S_{L-1})^K$.
          This is $\sum_{L} Pre[L] \sum_{R'=L-1}^{N-2} Suf[R'+1] (S_{R'} - S_{L-1})^K$.
          We can precompute $Inner3[t][L] = \sum_{j=L-1}^{N-2} Suf[j+1] S_j^t$.
       4. $C=0$ (for $S_{R-1} - S_L$). $R' = R-1$. $Suf[R'+1]$.
          Sum over $L < R' + 1 \implies L \le R'$. $R' \le N-2$.
          $R' \ge L$.
          Sum over $R' \in [L, N-2]$.
          Term: $Pre[L] Suf[R'+1] (S_{R'} - S_L)^K$.
          Precompute $Inner4[t][L] = \sum_{j=L}^{N-2} Suf[j+1] S_j^t$.
    
    So we need 4 sets of precomputed inner sums.
    Actually, we can just write a generic precomputation function that takes a list of $Suf$ values and a list of $S$ values (shifted) and computes the inner sums.
    
    Steps:
    1. Read N, K, A.
    2. Compute S[0..N].
    3. Compute Pre[1..N], Suf[1..N].
    4. Precompute powers of S[i] for i in 0..N, t in 0..K.
    5. Define a function `get_inner(S_list, Suf_list, start_index)` that returns a 2D array `inner[t][L]` for $L$ from 1 to N.
       `inner[t][L] = sum_{j=start_index}^{N} Suf_list[j] * (S_list[j])^t`.
       Actually, we need to handle the specific ranges.
       Let's just implement the 4 calculations explicitly.
    
    Complexity: $O(NK)$. Space $O(NK)$.
    Constraints: $N=2e5, K=10$. $2e6$ ints. Fine.

## worker: Implement the $O(NK)$ solution using the derived f
The solution implements the derived $O(NK)$ algorithm.
1.  **Mathematical Derivation**: The problem is transformed into computing $\sum_{L, R} Pre[L] Suf[R] Q(L, R)$ where $Q(L, R)$ is the sum of products of $K$ elements chosen from the range $[L, R]$ such that the minimum index is $L$ and the maximum is $R$. This is expanded using inclusion-exclusion on the subarray sums: $Q(L, R) = S(L, R)^K - S(L+1, R)^K - S(L, R-1)^K + S(L+1, R-1)^K$.
2.  **Efficient Calculation**: The term $\sum_{L, R} Pre[L] Suf[R] (S_R - S_{L+C})^K$ is expanded using the binomial theorem: $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} S_{L+C}^{K-t} \sum_{R} Suf[R] S_R^t$.
3.  **Precomputation**:
    *   Prefix sums $S$ of $A$.
    *   $Pre[L]$ and $Suf[R]$ arrays.
    *   Powers of $S[i]$ for $t \in [0, K]$.
    *   Binomial coefficients.
    *   For each of the 4 terms, we compute the inner sums $\sum_{R} Suf[R] S_R^t$ (or equivalent shifted versions) in $O(N)$ by iterating backwards, resulting in $O(NK)$ total time.
4.  **Complexity**: Time $O(NK)$, Space $O(NK)$. Given $N=2 \cdot 10^5, K=10$, this is well within limits.

## worker: Implement the Python solution based on the $O(NK)$
The solution implements the $O(NK)$ algorithm derived in the ideation phase.
1.  **Mathematical Derivation**: The problem is transformed into computing $\sum_{L, R} Pre[L] Suf[R] Q(L, R)$ where $Q(L, R)$ is the sum of products of $K$ elements chosen from the range $[L, R]$ such that the minimum index is $L$ and the maximum is $R$. This is expanded using inclusion-exclusion on the subarray sums: $Q(L, R) = S(L, R)^K - S(L+1, R)^K - S(L, R-1)^K + S(L+1, R-1)^K$.
2.  **Efficient Calculation**: The term $\sum_{L, R} Pre[L] Suf[R] (S_R - S_{L+C})^K$ is expanded using the binomial theorem: $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} S_{L+C}^{K-t} \sum_{R} Suf[R] S_R^t$.
3.  **Precomputation**:
    *   Prefix sums $S$ of $A$.
    *   $Pre[L]$ and $Suf[R]$ arrays.
    *   Powers of $S[i]$ for $t \in [0, K]$.
    *   Binomial coefficients.
    *   For each of the 4 terms, we compute the inner sums $\sum_{R} Suf[R] S_R^t$ (or equivalent shifted versions) in $O(N)$ by iterating backwards, resulting in $O(NK)$ total time.
4.  **Complexity**: Time $O(NK)$, Space $O(NK)$. Given $N=2 \cdot 10^5, K=10$, this is well within limits.

## worker: Implement the Python solution based on the $O(NK)$
The solution implements the $O(NK)$ algorithm derived in the ideation phase.
1.  **Mathematical Derivation**: The problem is transformed into computing $\sum_{L, R} Pre[L] Suf[R] Q(L, R)$ where $Q(L, R)$ is the sum of products of $K$ elements chosen from the range $[L, R]$ such that the minimum index is $L$ and the maximum is $R$. This is expanded using inclusion-exclusion on the subarray sums: $Q(L, R) = S(L, R)^K - S(L+1, R)^K - S(L, R-1)^K + S(L+1, R-1)^K$.
2.  **Efficient Calculation**: The term $\sum_{L, R} Pre[L] Suf[R] (S_R - S_{L+C})^K$ is expanded using the binomial theorem: $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} S_{L+C}^{K-t} \sum_{R} Suf[R] S_R^t$.
3.  **Precomputation**:
    *   Prefix sums $S$ of $A$.
    *   $Pre[L]$ and $Suf[R]$ arrays.
    *   Powers of $S[i]$ for $t \in [0, K]$.
    *   Binomial coefficients.
    *   For each of the 4 terms, we compute the inner sums $\sum_{R} Suf[R] S_R^t$ (or equivalent shifted versions) in $O(N)$ by iterating backwards, resulting in $O(NK)$ total time.
4.  **Complexity**: Time $O(NK)$, Space $O(NK)$. Given $N=2 \cdot 10^5, K=10$, this is well within limits.

## worker: finalize
The solution implements the $O(NK)$ algorithm derived in the ideation phase.
1.  **Mathematical Derivation**: The problem is transformed into computing $\sum_{L, R} Pre[L] Suf[R] Q(L, R)$ where $Q(L, R)$ is the sum of products of $K$ elements chosen from the range $[L, R]$ such that the minimum index is $L$ and the maximum is $R$. This is expanded using inclusion-exclusion on the subarray sums: $Q(L, R) = S(L, R)^K - S(L+1, R)^K - S(L, R-1)^K + S(L+1, R-1)^K$.
2.  **Efficient Calculation**: The term $\sum_{L, R} Pre[L] Suf[R] (S_R - S_{L+C})^K$ is expanded using the binomial theorem: $\sum_{t=0}^K \binom{K}{t} (-1)^{K-t} S_{L+C}^{K-t} \sum_{R} Suf[R] S_R^t$.
3.  **Precomputation**:
    *   Prefix sums $S$ of $A$.
    *   $Pre[L]$ and $Suf[R]$ arrays.
    *   Powers of $S[i]$ for $t \in [0, K]$.
    *   Binomial coefficients.
    *   For each of the 4 terms, we compute the inner sums $\sum_{R} Suf[R] S_R^t$ (or equivalent shifted versions) in $O(N)$ by iterating backwards, resulting in $O(NK)$ total time.
4.  **Complexity**: Time $O(NK)$, Space $O(NK)$. Given $N=2 \cdot 10^5, K=10$, this is well within limits.
