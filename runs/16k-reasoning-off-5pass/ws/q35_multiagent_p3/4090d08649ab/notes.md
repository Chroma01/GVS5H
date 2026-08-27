
## ideation
The problem asks for the sum of $f(L, R)$ over all subarrays.
1.  **Analyze $f(L, R)$**: The operation allows erasing a contiguous range of *values* $[l, r]$ if all values in that range are present on the blackboard. This is equivalent to partitioning the set of distinct values in the subarray into the minimum number of contiguous integer intervals.
    Let $U_{L,R}$ be the set of distinct values in $A[L..R]$. If we sort $U_{L,R}$ as $u_1 < u_2 < \dots < u_k$, then $f(L, R)$ is the number of "gaps" plus 1. A gap exists between $u_i$ and $u_{i+1}$ if $u_{i+1} > u_i + 1$.
    Mathematically, $f(L, R) = |U_{L,R}| - \sum_{v \in U_{L,R}} [v+1 \in U_{L,R}]$.
    Here, $[v+1 \in U_{L,R}]$ is 1 if both $v$ and $v+1$ are in the subarray, and 0 otherwise.

2.  **Decompose the Sum**:
    We need to compute $\sum_{L=1}^N \sum_{R=L}^N f(L, R)$.
    $$ \sum_{L,R} f(L, R) = \sum_{L,R} |U_{L,R}| - \sum_{L,R} \sum_{v=1}^{N-1} [v \in U_{L,R} \land v+1 \in U_{L,R}] $$
    Let $S_1 = \sum_{L,R} |U_{L,R}|$ and $S_2 = \sum_{L,R} \sum_{v=1}^{N-1} [v \in U_{L,R} \land v+1 \in U_{L,R}]$.
    The answer is $S_1 - S_2$.

3.  **Compute $S_1$**:
    $S_1$ is the sum of the number of distinct elements in all subarrays.
    For each element $A_i$ at index $i$, it contributes to the distinct count of a subarray $[L, R]$ if and only if it is the *first* occurrence of the value $A_i$ in that subarray.
    Let $prev[i]$ be the index of the previous occurrence of value $A_i$ (0 if none).
    The valid $L$ values are $prev[i] < L \le i$, and valid $R$ values are $i \le R \le N$.
    The number of such subarrays is $(i - prev[i]) \times (N - i + 1)$.
    $S_1 = \sum_{i=1}^N (i - prev[i]) \times (N - i + 1)$.

4.  **Compute $S_2$**:
    $S_2 = \sum_{v=1}^{N-1} C(v, v+1)$, where $C(v, v+1)$ is the number of subarrays containing both value $v$ and value $v+1$.
    Using inclusion-exclusion principle on the set of all subarrays (total $M = N(N+1)/2$):
    $C(v, v+1) = M - (\text{subarrays missing } v) - (\text{subarrays missing } v+1) + (\text{subarrays missing both } v \text{ and } v+1)$.
    
    To compute "subarrays missing value $x$":
    Let the positions of $x$ be $p_1, p_2, \dots, p_k$.
    The subarrays missing $x$ are those completely contained within the gaps between these positions: $[1, p_1-1], [p_1+1, p_2-1], \dots, [p_k+1, N]$.
    The number of subarrays in a segment of length $len$ is $len(len+1)/2$.
    
    To compute "subarrays missing both $v$ and $v+1$":
    Combine the positions of $v$ and $v+1$, sort them, and compute the sum of subarrays in the resulting gaps.
    
    Since the sum of occurrences of all values is $N$, iterating through all $v$ and processing their positions takes $O(N)$ total time.

5.  **Pitfalls**:
    - Integer overflow: The answer can be large, so use 64-bit integers. Python handles this automatically.
    - Edge cases: $N=1$, values not present, etc. The logic holds generally.
    - Efficiency: Ensure $O(N)$ or $O(N \log N)$ complexity. The proposed approach is $O(N)$.

## worker: Implement a function to calculate the number of su
The solution relies on decomposing the function $f(L, R)$ into a sum of distinct element counts minus the number of adjacent value pairs present in the subarray.
1.  **Formula Derivation**: $f(L, R)$ is the number of contiguous integer intervals needed to cover the set of distinct values in $A[L..R]$. This equals $|U_{L,R}| - \sum_{v} [v \in U_{L,R} \land v+1 \in U_{L,R}]$.
2.  **Summation**: The total answer is $\sum_{L,R} |U_{L,R}| - \sum_{L,R} \sum_{v} [v, v+1 \in U_{L,R}]$.
3.  **$S_1$ Calculation**: $\sum_{L,R} |U_{L,R}|$ is computed by summing the contribution of each element being the *first* occurrence of its value in a subarray. This is done in $O(N)$ using the previous occurrence index.
4.  **$S_2$ Calculation**: For each value $v$, we count subarrays containing both $v$ and $v+1$ using inclusion-exclusion on the complement (subarrays missing $v$, missing $v+1$, or missing both). The number of subarrays missing a set of values is calculated by summing $len(len+1)/2$ for all gaps between the occurrences of those values. Since the total number of occurrences across all values is $N$, this step is also $O(N)$.
5.  **Complexity**: The overall time complexity is $O(N)$ and space complexity is $O(N)$, which fits well within the constraints $N \le 3 \times 10^5$.
