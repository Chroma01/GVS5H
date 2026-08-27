1.  **Analyze the Operations**:
    *   Op 1 sets $x_j=1$ for $j \in [L, R]$. This "covers" the interval $[L, R]$.
    *   Op 2 sets $x_j=1$ for $j \notin [L, R]$, i.e., $[1, L-1] \cup [R+1, N]$. This "covers" the complement of $[L, R]$.
    *   Op 0 does nothing.
    *   The goal is to have all $x_j=1$. This means every index $j \in [1, N]$ must be covered by at least one chosen Op 1 or Op 2.

2.  **Reformulate as Set Cover / Interval Cover**:
    *   Each Op 1 corresponds to covering interval $[L_i, R_i]$.
    *   Each Op 2 corresponds to covering intervals $[1, L_i-1]$ and $[R_i+1, N]$. Note that if $L_i=1$, Op 2 covers $[R_i+1, N]$. If $R_i=N$, Op 2 covers $[1, L_i-1]$. If $L_i=1$ and $R_i=N$, Op 2 covers nothing (empty set).
    *   We want to select a subset of operations (minimizing count) such that the union of their covered regions is $[1, N]$.

3.  **Dynamic Programming Approach**:
    *   Since $N$ is up to $10^6$, we need an efficient DP.
    *   Let $DP[i]$ be the minimum cost to cover the prefix $[1, i]$ completely.
    *   However, Op 2 covers non-contiguous parts (prefix and suffix). This suggests we might need to track the "rightmost uncovered point" or use a different state.
    *   Actually, let's look at the structure. We need to cover $[1, N]$.
    *   Consider the intervals. We can process operations and maintain the state of coverage.
    *   Alternative view: This is equivalent to finding a minimum weight set of intervals (from the set of all $[L_i, R_i]$ and all $[1, L_i-1] \cup [R_i+1, N]$) that cover $[1, N]$.
    *   Since Op 2 creates two intervals, it's slightly complex. But note that covering $[1, N]$ can be split into covering $[1, k]$ and $[k+1, N]$ for some split point? Not necessarily, because one Op 2 can cover parts of both.
    *   Let's use DP on the position. $DP[i]$ = min cost to cover $[1, i]$.
    *   To compute $DP[i]$, we can transition from $DP[j]$ where $j < i$.
    *   If we use an Op 1 on $[L, R]$, it covers $[L, R]$. If we are building up from left, we can say: if we have covered $[1, L-1]$ with cost $C$, and we apply Op 1 on $[L, R]$, we now cover $[1, R]$ with cost $C+1$. So $DP[R] = \min(DP[R], DP[L-1] + 1)$.
    *   If we use an Op 2 on $[L, R]$, it covers $[1, L-1]$ and $[R+1, N]$. This operation is tricky because it covers a prefix and a suffix.
    *   Let's refine the DP state. We want to cover the entire array.
    *   Let $DP[i]$ be the min cost to cover the prefix $[1, i]$.
    *   Base case: $DP[0] = 0$. All other $DP[i] = \infty$.
    *   Transitions for Op 1 $(L, R)$:
        *   If we use Op 1, it covers $[L, R]$. To use this to extend a covered prefix, we need $[1, L-1]$ to be already covered. Then the new covered prefix becomes $[1, R]$.
        *   $DP[R] = \min(DP[R], DP[L-1] + 1)$.
    *   Transitions for Op 2 $(L, R)$:
        *   Op 2 covers $[1, L-1]$ and $[R+1, N]$.
        *   If we use Op 2, it automatically covers $[1, L-1]$. So if we have covered $[1, L-1]$ (cost $DP[L-1]$), we can potentially jump to a state where we have covered $[1, R+1]$? No, Op 2 covers $[1, L-1]$ and $[R+1, N]$. It does NOT cover $[L, R]$.
        *   So, if we use Op 2, the prefix $[1, L-1]$ is covered. The "gap" is $[L, R]$. The suffix $[R+1, N]$ is covered.
        *   This suggests we might need a second DP array or a different formulation.
        *   Let $DP[i]$ = min cost to cover prefix $[1, i]$.
        *   Let $DP2[i]$ = min cost to cover the suffix $[i, N]$? Or maybe min cost to cover everything *except* a prefix?
        *   Actually, consider the final state. The union of selected intervals must be $[1, N]$.
        *   We can iterate through all possible "split points" where a single Op 2 might bridge the gap? No.
        *   Let's stick to $DP[i]$ = min cost to cover $[1, i]$.
        *   For Op 2 $(L, R)$: It covers $[1, L-1]$ and $[R+1, N]$.
            *   If we use Op 2, we cover $[1, L-1]$. So we can update $DP[L-1]$? No, $DP[L-1]$ is already computed.
            *   Using Op 2 allows us to cover $[R+1, N]$ "for free" if we have already covered $[1, L-1]$? Not quite. It covers $[R+1, N]$ regardless of what happens in $[L, R]$.
            *   So, if we use Op 2, we pay 1. We cover $[1, L-1]$ and $[R+1, N]$.
            *   This means if we have a solution for covering $[1, L-1]$ with cost $C$, we can say that with cost $C+1$, we have covered $[1, L-1]$ AND $[R+1, N]$.
            *   Let $DP[i]$ be min cost to cover $[1, i]$.
            *   Let $DP\_suffix[i]$ be min cost to cover $[i, N]$.
            *   This seems symmetric.
            *   However, we can combine them. If we use Op 2, we cover a prefix and a suffix. The middle $[L, R]$ is left uncovered. We must cover $[L, R]$ using other operations.
            *   So, a valid solution could be:
                1.  Cover $[1, L-1]$ using some ops.
                2.  Cover $[L, R]$ using some ops.
                3.  Cover $[R+1, N]$ using some ops.
                4.  Plus the Op 2 itself which covers $[1, L-1]$ and $[R+1, N]$.
            *   This implies that if we use Op 2, we can "save" the cost of covering $[1, L-1]$ and $[R+1, N]$ separately if we were to cover them independently?
            *   Actually, simpler:
                *   Calculate $DP[i]$: min cost to cover $[1, i]$ using only Op 1s? No, Op 2s can be used too.
                *   But Op 2s are special.
    
    *   **Revised Strategy**:
        1.  Compute $DP\_pre[i]$: Min cost to cover prefix $[1, i]$ using ANY combination of Op 1 and Op 2.
            *   Wait, if we use Op 2, it covers a suffix too. This makes "prefix coverage" dependent on future choices? No, the cost is additive.
            *   Let's define $DP[i]$ as min cost to cover $[1, i]$.
            *   Transitions:
                *   From $DP[i-1]$, we can try to extend coverage to $i$.
                *   Use Op 1 $(L, R)$: If $L-1 \le i$ and $R \ge i$, this op covers $i$. But we need to cover $[1, L-1]$ first.
                *   This standard interval covering DP works if we only have Op 1.
                *   With Op 2, it's more complex.

    *   **Alternative Insight**:
        *   The problem is small enough for $O(M \log M)$ or $O(M + N)$.
        *   Let's consider the complement. We want to cover $[1, N]$.
        *   Let's compute $DP[i]$ = min cost to cover $[1, i]$.
        *   Initialize $DP[0]=0$, others $\infty$.
        *   For each $i$ from 1 to $N$:
            *   $DP[i] = DP[i-1]$? No, covering $[1, i-1]$ doesn't imply $[1, i]$ is covered.
            *   We need to transition from some $j < i$ using an operation that covers $[j+1, i]$.
            *   Op 1 $(L, R)$ covers $[L, R]$. If we have covered $[1, L-1]$ (cost $DP[L-1]$), we can cover $[1, R]$ with cost $DP[L-1] + 1$. So $DP[R] = \min(DP[R], DP[L-1] + 1)$.
            *   Op 2 $(L, R)$ covers $[1, L-1]$ and $[R+1, N]$.
                *   This operation is useful if we want to cover a suffix.
                *   Let's also compute $DP\_suf[i]$ = min cost to cover suffix $[i, N]$.
                *   $DP\_suf[N+1] = 0$.
                *   Op 1 $(L, R)$ covers $[L, R]$. If we have covered $[R+1, N]$ (cost $DP\_suf[R+1]$), we can cover $[L, N]$ with cost $DP\_suf[R+1] + 1$. So $DP\_suf[L] = \min(DP\_suf[L], DP\_suf[R+1] + 1)$.
                *   Op 2 $(L, R)$ covers $[1, L-1]$ and $[R+1, N]$.
                    *   This covers the prefix $[1, L-1]$ and suffix $[R+1, N]$.
                    *   The gap is $[L, R]$.
                    *   So, if we use Op 2, we pay 1. We cover $[1, L-1]$ and $[R+1, N]$. We still need to cover $[L, R]$.
                    *   The cost to cover $[L, R]$ can be derived from $DP[R] - DP[L-1]$? No, costs aren't linear.
                    *   However, we can combine:
                        *   Total Cost = Cost to cover $[1, L-1]$ + Cost to cover $[L, R]$ + Cost to cover $[R+1, N]$ - Savings?
                        *   If we use Op 2, we cover $[1, L-1]$ and $[R+1, N]$ for free (included in the 1 cost).
                        *   So, if we use Op 2, the total cost is $1 + \text{Cost to cover } [L, R]$.
                        *   But wait, the operations covering $[1, L-1]$ and $[R+1, N]$ might overlap with the operations covering $[L, R]$? No, the intervals are disjoint.
                        *   So, if we decide to use Op 2 $(L, R)$, we MUST cover $[L, R]$ using other operations. The cost is $1 + \text{MinCostToCoverInterval}(L, R)$.
                        *   What is $\text{MinCostToCoverInterval}(L, R)$? It's the min cost to cover $[L, R]$ using Op 1 and Op 2?
                        *   If we use Op 2 inside $[L, R]$, it would cover parts outside $[L, R]$ too. This complicates things.

    *   **Simpler DP with State**:
        *   Let $DP[i]$ be the min cost to cover $[1, i]$.
        *   We also need to know if we have "pending" coverage from an Op 2? No.
        *   Let's just compute $DP[i]$ for $i=0 \dots N$.
        *   $DP[0] = 0$.
        *   For $i = 1 \dots N$:
            *   $DP[i] = \infty$.
            *   Option 1: Extend from $DP[i-1]$? No, we need an operation that ends at $i$ or covers $i$.
            *   Actually, we can iterate through all operations that *end* at $i$ or *start* before $i$ and cover $i$.
            *   Standard Interval Cover DP:
                *   Sort intervals by end point.
                *   $DP[i]$ = min cost to cover $[1, i]$.
                *   For each Op 1 $(L, R)$: $DP[R] = \min(DP[R], DP[L-1] + 1)$.
                *   For each Op 2 $(L, R)$: It covers $[1, L-1]$ and $[R+1, N]$.
                    *   This doesn't fit the "prefix" DP directly because it covers a suffix.
        
    *   **Final Plan**:
        1.  Compute $DP\_pre[i]$: Min cost to cover $[1, i]$ using Op 1 and Op 2.
            *   Initialize $DP\_pre[0]=0$, others $\infty$.
            *   Process operations. But Op 2 is tricky.
            *   Let's compute $DP\_pre$ using only Op 1 first? No.
            *   Let's compute $DP\_pre[i]$ considering all ops.
            *   $DP\_pre[i] = \min($
                *   $DP\_pre[i-1]$ if $x_i$ is covered by same ops as $i-1$? No.
                *   $\min_{\text{Op 1 } (L, R) \text{ s.t. } R=i} (DP\_pre[L-1] + 1)$
                *   $\min_{\text{Op 2 } (L, R) \text{ s.t. } L-1=i} (DP\_pre[0] + 1 + \text{Cost to cover } [L, R] \text{ using remaining ops?})$ -> This is circular.
        
        2.  **Correct Approach**:
            *   The problem can be modeled as: Select a set of intervals (from Op 1s and Op 2s) to cover $[1, N]$.
            *   Op 1 gives interval $[L, R]$.
            *   Op 2 gives intervals $[1, L-1]$ and $[R+1, N]$.
            *   We want to cover $[1, N]$.
            *   Let's compute $DP[i]$ = min cost to cover $[1, i]$.
            *   Let's compute $DP\_suf[i]$ = min cost to cover $[i, N]$.
            *   These can be computed independently using only Op 1? No, Op 2 can be used in both.
            *   However, if we use Op 2, it covers a prefix and a suffix.
            *   Let's assume we don't use Op 2 for the "main" coverage and handle Op 2 as a special "bridge".
            *   Actually, Op 2 is just two intervals. We can treat Op 2 as providing two intervals: $I_{2a} = [1, L-1]$ and $I_{2b} = [R+1, N]$.
            *   We want to cover $[1, N]$ with minimum cost.
            *   This is a weighted set cover on intervals. Since intervals are special, we can use DP.
            *   Let $DP[i]$ be min cost to cover $[1, i]$.
            *   Transitions:
                *   For each Op 1 $(L, R)$: $DP[R] = \min(DP[R], DP[L-1] + 1)$.
                *   For each Op 2 $(L, R)$:
                    *   It covers $[1, L-1]$ and $[R+1, N]$.
                    *   If we use Op 2, we cover $[1, L-1]$ and $[R+1, N]$.
                    *   We still need to cover $[L, R]$.
                    *   So, if we use Op 2, the total cost is $1 + \text{Cost to cover } [L, R]$.
                    *   But "Cost to cover $[L, R]$" might use Op 2s itself?
                    *   If we use another Op 2 inside, it gets complex.
            
            *   **Key Insight**: We can iterate over all possible "last" operation that covers the rightmost part?
            *   Or, simply:
                *   Compute $DP[i]$ = min cost to cover $[1, i]$ using ONLY Op 1.
                *   Compute $DP\_suf[i]$ = min cost to cover $[i, N]$ using ONLY Op 1.
                *   Then, consider using Op 2. If we use Op 2 $(L, R)$, we cover $[1, L-1]$ and $[R+1, N]$. We need to cover $[L, R]$.
                *   The cost to cover $[L, R]$ using Op 1 is $DP\_gap[L][R]$?
                *   Actually, we can just run the DP for Op 1 to get $DP\_pre$ and $DP\_suf$.
                *   Then, for each Op 2 $(L, R)$, the cost to cover the whole array if we use this Op 2 is $1 + DP\_pre\_only\_op1[L-1 \text{ to } L-1?] + DP\_suf\_only\_op1[R+1 \text{ to } R+1?] + \text{Cost to cover } [L, R]$.
                *   This is getting messy.

    *   **Robust Solution**:
        1.  Create a list of all "atomic" intervals provided by Op 1 and Op 2.
            *   Op 1: $[L, R]$ cost 1.
            *   Op 2: $[1, L-1]$ cost 1, $[R+1, N]$ cost 1. Note: These two intervals come from the SAME operation. We cannot pick one without the other.
        2.  This is a "constrained" interval cover.
        3.  Given the constraints ($N=10^6, M=2 \cdot 10^5$), we can use a segment tree or sparse table for DP optimization.
        4.  Let $DP[i]$ be min cost to cover $[1, i]$.
        5.  $DP[0] = 0$.
        6.  For $i = 1 \dots N$:
            *   $DP[i] = \min($
                *   $\min_{\text{Op 1 } (L, R) \text{ s.t. } R=i} (DP[L-1] + 1)$,
                *   $\min_{\text{Op 2 } (L, R) \text{ s.t. } L-1=i} (1 + \text{Cost to cover } [L, N] \text{ given } [1, L-1] \text{ and } [R+1, N] \text{ are covered})$
            *   The second term is hard because it depends on the suffix.

    *   **Let's try a different DP state**:
        *   $DP[i]$ = min cost to cover $[1, i]$.
        *   We process operations.
        *   We can also compute $BestSuffix[i]$ = min cost to cover $[i, N]$.
        *   Then, the answer is $\min($
            *   $DP[N]$ (using only Op 1 and Op 2 treated as prefix-coverers? No),
            *   $\min_{\text{Op 2 } (L, R)} (1 + DP[L-1] + BestSuffix[R+1] + \text{Cost to cover } [L, R] \text{ with remaining ops?})$
        
    *   **Simplest Correct Logic**:
        1.  Compute $DP[i]$ = min cost to cover $[1, i]$ using ANY operations.
        2.  To handle Op 2, notice that Op 2 $(L, R)$ covers $[1, L-1]$ and $[R+1, N]$.
        3.  If we use Op 2, we effectively "skip" covering $[1, L-1]$ and $[R+1, N]$ with other ops.
        4.  So, $DP[i]$ can be updated by Op 2 if $i \ge R+1$? No.
        
        Let's just implement the standard "Minimum Weight Interval Cover" DP.
        $DP[i]$ = min cost to cover $[1, i]$.
        Initialize $DP[0]=0$, others $\infty$.
        
        For each operation:
        - If Op 1 $(L, R)$:
          $DP[R] = \min(DP[R], DP[L-1] + 1)$.
        - If Op 2 $(L, R)$:
          This op covers $[1, L-1]$ and $[R+1, N]$.
          It can update $DP[L-1]$? No, $DP[L-1]$ is cost to cover $[1, L-1]$. Op 2 covers it for cost 1.
          So $DP[L-1] = \min(DP[L-1], 1)$.
          But it also covers $[R+1, N]$. This part is not in the prefix DP.
          
        So, we need $DP\_suf[i]$ = min cost to cover $[i, N]$.
        $DP\_suf[N+1] = 0$.
        
        For Op 1 $(L, R)$:
        $DP\_suf[L] = \min(DP\_suf[L], DP\_suf[R+1] + 1)$.
        
        For Op 2 $(L, R)$:
        It covers $[1, L-1]$ and $[R+1, N]$.
        So it can update $DP\_suf[R+1]$?
        $DP\_suf[R+1] = \min(DP\_suf[R+1], 1)$.
        And it can update $DP[L-1]$?
        $DP[L-1] = \min(DP[L-1], 1)$.
        
        But these are independent. We need to combine them.
        The total cost to cover $[1, N]$ is:
        $\min($
           $DP[N]$,  // Covered entirely by prefix logic? No, Op 2 doesn't fit well.
           $DP\_suf[1]$, // Covered entirely by suffix logic?
           $\min_{\text{Op 2 } (L, R)} (1 + \text{Cost to cover } [L, R] \text{ using other ops})$
        $)$
        
        Actually, if we use Op 2, we cover $[1, L-1]$ and $[R+1, N]$. We need to cover $[L, R]$.
        The cost to cover $[L, R]$ can be computed by a separate DP on the subarray?
        Or, we can just say:
        Total Cost = $1 + DP\_sub[L][R]$.
        Where $DP\_sub[L][R]$ is min cost to cover $[L, R]$ using Op 1 and Op 2?
        
        Given time, I will implement a solution that:
        1. Computes $DP[i]$ for prefix $[1, i]$ using Op 1 and Op 2 (treating Op 2 as covering $[1, L-1]$).
        2. Computes $DP\_suf[i]$ for suffix $[i, N]$ using Op 1 and Op 2 (treating Op 2 as covering $[R+1, N]$).
        3. Iterates all Op 2s and calculates $1 + DP[L-1] + DP\_suf[R+1]$.
        4. Also considers solutions using only Op 1 (which is covered by $DP[N]$ if we allow Op 2 to just cover prefix? No).
        
        Actually, the safest bet is:
        Answer = $\min($
           $DP[N]$ computed with Op 1 and Op 2 (where Op 2 updates $DP[L-1]$),
           $\min_{\text{Op 2 } (L, R)} (1 + DP[L-1] + DP\_suf[R+1])$
        $)$
        
        Wait, if we use Op 2, we cover $[1, L-1]$ and $[R+1, N]$.
        $DP[L-1]$ is cost to cover $[1, L-1]$.
        $DP\_suf[R+1]$ is cost to cover $[R+1, N]$.
        But if we use Op 2, we pay 1. Do we need to pay for $DP[L-1]$ and $DP\_suf[R+1]$?
        No! Op 2 covers them.
        So if we use Op 2, the cost is $1 + \text{Cost to cover } [L, R]$.
        
        So we need $CostToCover[L][R]$.
        
        I will write a solution that computes $DP[i]$ for $[1, i]$ using Op 1 only, and $DP\_suf[i]$ using Op 1 only.
        Then for Op 2, we need to cover $[L, R]$.
        
        This is too complex for a short plan. I will provide a solution that uses a segment tree to optimize the DP.