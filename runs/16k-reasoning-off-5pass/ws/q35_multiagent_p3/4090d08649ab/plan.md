1.  **Understand $f(L, R)$**: The operation allows erasing all occurrences of a set of values if their indices in the current blackboard form a contiguous range. This is equivalent to finding the minimum number of "blocks" of values that can be erased. A key insight is that $f(L, R)$ is equal to the number of "connected components" of values in the subarray if we consider values connected if they appear in the same contiguous segment of the original array or are adjacent in value? No, let's look closer.
    Actually, let's re-read carefully. "Choose integers $l, r$ such that every integer from $l$ through $r$ appears at least once on the blackboard." This means we can erase a range of *values* $[l, r]$ if all values in that range are present on the blackboard. The indices $l, r$ refer to the *values*, not the positions on the blackboard. Wait, the problem says "Choose integers $l, r$ with $l \le r$ such that every integer from $l$ through $r$ appears at least once on the blackboard. Then, erase all integers from $l$ through $r$ that are on the blackboard."
    This phrasing is slightly ambiguous. Does "integers from $l$ through $r$" refer to values or positions?
    "Write the R-L+1 integers ... on the blackboard in order."
    "Choose integers $l, r$ ... such that every integer from $l$ through $r$ appears at least once on the blackboard."
    Usually, in such problems, if $l, r$ refer to positions, it would say "indices". If they refer to values, it would say "values". The example: Blackboard has `1, 3, 1, 4`.
    Operation 1: Choose $(l, r) = (1, 1)$. Erase all occurrences of 1. Blackboard becomes `3, 4`.
    Operation 2: Choose $(l, r) = (3, 4)$. Erase all occurrences of 3 and 4. Blackboard empty.
    Here, $l=1, r=1$ refers to the value 1. $l=3, r=4$ refers to values 3 and 4.
    So, an operation erases all instances of a contiguous range of *values* $[v_{min}, v_{max}]$ provided that *all* values in that range are currently present on the blackboard.
    
    This structure implies that the values present on the blackboard form a set $S$. We can remove a subset of values $V \subseteq S$ if $V$ is a contiguous range of integers (e.g., $\{3, 4, 5\}$) and $V \subseteq S$. We want to minimize the number of such operations.
    This is equivalent to partitioning the set of distinct values present in $A[L..R]$ into the minimum number of contiguous integer intervals.
    Let $U_{L,R}$ be the set of distinct values in $A[L..R]$. Sort them: $u_1 < u_2 < \dots < u_k$.
    The minimum number of operations is the number of "gaps" in the sorted distinct values plus 1. Specifically, if $u_{i+1} > u_i + 1$, there is a gap, and we must start a new operation.
    So, $f(L, R) = 1 + \sum_{i=1}^{k-1} [u_{i+1} > u_i + 1]$.
    
2.  **Summation Strategy**:
    We need to compute $\sum_{L=1}^N \sum_{R=L}^N f(L, R)$.
    $f(L, R) = 1 + \text{number of gaps in distinct values of } A[L..R]$.
    The total sum is $\sum_{L,R} 1 + \sum_{L,R} \text{gaps}(L, R)$.
    The first part is simply the number of pairs, $N(N+1)/2$.
    The second part requires counting, for each pair $(L, R)$, how many adjacent pairs of distinct values $(v, v+1)$ are "missing" or rather, how many times a gap occurs.
    A gap occurs between value $v$ and $v+1$ in the set of distinct values of $A[L..R]$ if:
    - Both $v$ and $v+1$ appear in $A[L..R]$.
    - There is no other value $u$ such that $v < u < v+1$ (which is impossible for integers).
    Wait, the definition of a gap in the sorted distinct values $u_1, \dots, u_k$ is $u_{i+1} > u_i + 1$.
    This means the value $u_i + 1$ is NOT in the set of distinct values.
    So, a gap exists between $u_i$ and $u_{i+1}$ if $u_i$ is present, $u_{i+1}$ is present, but $u_i + 1$ is NOT present.
    
    Let's reformulate:
    $f(L, R) = |U_{L,R}| - \sum_{v \in U_{L,R}} [v+1 \in U_{L,R}]$.
    Why?
    If we have a contiguous block of values like $\{1, 2, 3\}$, $|U|=3$. Pairs $(v, v+1)$ present: $(1,2), (2,3)$. Sum of indicators = 2. $f = 3 - 2 = 1$. Correct.
    If we have $\{1, 3\}$, $|U|=2$. Pairs present: none. Sum = 0. $f = 2 - 0 = 2$. Correct.
    If we have $\{1, 2, 4, 5\}$, $|U|=4$. Pairs present: $(1,2), (4,5)$. Sum = 2. $f = 4 - 2 = 2$. Correct.
    
    So, $\sum_{L,R} f(L, R) = \sum_{L,R} |U_{L,R}| - \sum_{L,R} \sum_{v} [v \in U_{L,R} \land v+1 \in U_{L,R}]$.
    
    Let $S_1 = \sum_{L,R} |U_{L,R}|$. This is the sum of the number of distinct elements in all subarrays. This is a standard problem solvable in $O(N)$ or $O(N \log N)$.
    Let $S_2 = \sum_{L,R} \sum_{v=1}^{N-1} [v \in U_{L,R} \land v+1 \in U_{L,R}]$.
    We can swap sums: $S_2 = \sum_{v=1}^{N-1} \sum_{L,R} [v \in U_{L,R} \land v+1 \in U_{L,R}]$.
    For a fixed $v$, we need to count pairs $(L, R)$ such that both $v$ and $v+1$ appear in $A[L..R]$.
    Let $Pos(x)$ be the list of indices where value $x$ appears.
    The condition "$v$ appears in $A[L..R]$" means $L \le \min\_pos(v, L, R) \le R$? No, it means there is at least one occurrence of $v$ in $[L, R]$.
    Let $first(v, L, R)$ be the first occurrence of $v$ in $[L, R]$.
    Actually, it's easier to count the complement or use inclusion-exclusion?
    Count pairs $(L, R)$ where $v \in U_{L,R}$ AND $v+1 \in U_{L,R}$.
    Let $C(v)$ be the count of subarrays containing $v$.
    Let $C(v, v+1)$ be the count of subarrays containing both $v$ and $v+1$.
    
    To compute $C(v, v+1)$:
    Let the positions of $v$ be $p_1, p_2, \dots$ and $v+1$ be $q_1, q_2, \dots$.
    A subarray $[L, R]$ contains $v$ if $L \le p_i \le R$ for some $i$.
    It contains $v+1$ if $L \le q_j \le R$ for some $j$.
    This is equivalent to: $L \le \max(\min\_occ(v), \min\_occ(v+1))$? No.
    Let $min\_idx(v)$ be the smallest index of $v$ in $[L, R]$.
    The condition is: $\exists i, j$ such that $L \le p_i \le R$ and $L \le q_j \le R$.
    This is equivalent to: $L \le \max(p_i, q_j)$ and $R \ge \min(p_i, q_j)$? No.
    It is equivalent to: $L \le \max(\text{first occurrence of } v \text{ in } [L,R], \text{first occurrence of } v+1 \text{ in } [L,R])$?
    Actually, simpler:
    Let $L_{max}$ be the maximum of the leftmost occurrences? No.
    
    Standard approach for "subarray contains value $x$":
    Let $prev[x][i]$ be the previous occurrence of $x$ before $i$.
    For a fixed $v$, the subarrays containing $v$ are those $[L, R]$ where $L \in (prev\_pos(v, k), k]$ and $R \ge k$ for some occurrence $k$.
    
    For two values $v$ and $v+1$:
    We want to count $[L, R]$ such that $[L, R]$ contains at least one $v$ and at least one $v+1$.
    Let $S_v$ be the set of valid $(L, R)$ containing $v$.
    We want $|S_v \cap S_{v+1}|$.
    
    We can iterate over all pairs of occurrences $(p_i, q_j)$? No, $N$ is $3 \cdot 10^5$, total occurrences is $N$. But pairs could be $O(N^2)$.
    However, we can compute the number of subarrays containing BOTH $v$ and $v+1$ efficiently.
    Let $L_{bound}$ and $R_{bound}$?
    
    Alternative:
    Total subarrays $M = N(N+1)/2$.
    Count subarrays missing $v$: $M_v$.
    Count subarrays missing $v+1$: $M_{v+1}$.
    Count subarrays missing $v$ OR missing $v+1$: $M_v + M_{v+1} - M_{both\_missing}$.
    Then $C(v, v+1) = M - (M_v + M_{v+1} - M_{both\_missing})$.
    
    $M_v$: Subarrays not containing $v$.
    If $v$ is at indices $p_1, \dots, p_k$, then the segments between occurrences are $[1, p_1-1], [p_1+1, p_2-1], \dots, [p_k+1, N]$.
    The number of subarrays in a segment of length $len$ is $len(len+1)/2$.
    Sum these up for $M_v$.
    
    $M_{both\_missing}$: Subarrays containing neither $v$ nor $v+1$.
    Combine indices of $v$ and $v+1$, sort them: $idx_1 < idx_2 < \dots < idx_m$.
    Add $0$ and $N+1$.
    The gaps are $[1, idx_1-1], [idx_1+1, idx_2-1], \dots$.
    Sum $len(len+1)/2$ for each gap.
    
    This allows computing $C(v, v+1)$ in time proportional to the number of occurrences of $v$ and $v+1$.
    Summing over all $v$, the total time is proportional to $\sum_v (\text{count}(v) + \text{count}(v+1)) = 2N$.
    So $S_2$ can be computed in $O(N)$.
    
    Similarly, $S_1 = \sum_{L,R} |U_{L,R}|$ can be computed in $O(N)$ by summing contributions of each element.
    For each $A_i$, it contributes to $|U_{L,R}|$ if it is the first occurrence of value $A_i$ in $[L, R]$.
    Let $prev[i]$ be the previous index of value $A_i$.
    $L$ can be in $(prev[i], i]$ and $R$ can be in $[i, N]$.
    Contribution is $(i - prev[i]) \times (N - i + 1)$.
    
    So the algorithm is:
    1. Compute $S_1 = \sum_{i=1}^N (i - prev[i]) \times (N - i + 1)$.
    2. Compute $S_2 = \sum_{v=1}^{N-1} C(v, v+1)$.
       For each $v$:
       a. Calculate $M_v$ (subarrays missing $v$).
       b. Calculate $M_{v+1}$ (subarrays missing $v+1$).
       c. Calculate $M_{both}$ (subarrays missing both $v$ and $v+1$).
       d. $C(v, v+1) = M - M_v - M_{v+1} + M_{both}$.
    3. Result $= S_1 - S_2$.