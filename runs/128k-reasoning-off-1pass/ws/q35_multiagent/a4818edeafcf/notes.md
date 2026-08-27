
## ideation
The core difficulty lies in efficiently computing the maximum sum of distinct counts for three subarrays without checking all $O(N^2)$ split points. A naive approach is too slow for $N=3 \times 10^5$.

The key insight is to iterate over the second cut position $j$ (from $2$ to $N-2$). For a fixed $j$, the third subarray is $A[j+1 \dots N]$, and its distinct count `suff[j+1]` can be precomputed. The problem reduces to maximizing `pref[i] + distinct(A[i+1 \dots j])` for $1 \le i < j$, where `pref[i]` is the distinct count of $A[1 \dots i]$.

Let $M_i^{(j)} = \text{distinct}(A[i+1 \dots j])$. When we move from $j-1$ to $j$, we add $A[j]$ to the end of all middle subarrays ending at $j-1$. The distinct count $M_i^{(j)}$ increases by 1 if and only if $A[j]$ does not appear in $A[i+1 \dots j-1]$. This condition is equivalent to $i \ge \text{last\_pos}[A[j]]$, where $\text{last\_pos}[v]$ is the index of the last occurrence of value $v$ before $j$. If $A[j]$ hasn't appeared before, $\text{last\_pos}[A[j]] = 0$.

Thus, for a fixed $j$, we need to:
1. Update $M_i$ for all $i \in [\text{last\_pos}[A[j]], j-1]$ by adding 1.
2. Query $\max_{1 \le i < j} (\text{pref}[i] + M_i)$.

We can maintain the values $V_i = \text{pref}[i] + M_i$ in a Segment Tree that supports range add updates and range maximum queries. Since $i$ ranges up to $N$, a segment tree of size $N$ is feasible.

Algorithm steps:
1. Precompute `pref[i]` for all $i$.
2. Precompute `suff[i]` for all $i$.
3. Initialize a segment tree with values `pref[i]` (since initially $M_i=0$ for all $i$, but effectively we start building from $j=2$). Actually, it's easier to initialize the segment tree with `pref[i]` and treat $M_i$ as 0 initially. As we iterate $j$, we update the range.
4. Iterate $j$ from $2$ to $N-2$:
   a. Determine $p = \text{last\_pos}[A[j]]$.
   b. Update segment tree: add 1 to range $[p, j-1]$. Note: if $p=0$, range is $[0, j-1]$, but indices are 1-based, so $[1, j-1]$. If $p \ge j$, no update needed (shouldn't happen).
   c. Query max in range $[1, j-1]$. Let this be `max_mid`.
   d. Candidate answer: `max_mid + suff[j+1]`.
   e. Update `last_pos[A[j]] = j`.
5. The overall maximum candidate answer is the result.

Pitfalls:
- Indexing: Ensure 1-based indexing is handled correctly in the segment tree.
- Range updates: The range $[p, j-1]$ might be invalid if $p > j-1$ (e.g., if $A[j]$ appeared at $j-1$, then $p=j-1$, range is $[j-1, j-1]$). If $p=0$, range is $[1, j-1]$.
- Base case: For $j=2$, the first subarray is $A[1\dots1]$, second is $A[2\dots2]$. `pref[1]` is 1. `last_pos[A[2]]` might be 0 or 1. If 0, update range $[1,1]$ by 1. Then query max in $[1,1]$.

## worker: none
The problem requires maximizing the sum of distinct counts of three contiguous subarrays formed by two cuts. A naive $O(N^2)$ approach is too slow for $N=3 \times 10^5$.

The efficient approach involves:
1.  **Precomputation**: Calculate `pref[i]` (distinct count in $A[0 \dots i-1]$) and `suff[i]` (distinct count in $A[i \dots N-1]$) for all valid indices. This takes $O(N)$.
2.  **Iterating on the second cut `j`**: We iterate `j` from 2 to $N-2$ (1-based index for the cut). The third subarray is fixed as $A[j \dots N-1]$, with distinct count `suff[j]`.
3.  **Dynamic Maintenance of Middle Subarray**: For a fixed `j`, we need to maximize `pref[i] + distinct(A[i \dots j-1])` for $1 \le i < j$. Let $M_i^{(j)} = \text{distinct}(A[i \dots j-1])$.
    *   When moving from `j-1` to `j`, we add element $A[j-1]$ to the end of all middle subarrays ending at `j-1`.
    *   $M_i^{(j)}$ increases by 1 if and only if $A[j-1]$ was not present in $A[i \dots j-2]$. This happens if the last occurrence of $A[j-1]$ before `j-1` was at an index $p < i$.
    *   Let $p$ be the last position of $A[j-1]$ (0-based). If $A[j-1]$ hasn't appeared, $p=-1$.
    *   For all $i$ such that $i > p$, the new element $A[j-1]$ is distinct in the subarray $A[i \dots j-1]$. In 1-based cut indexing, if the last occurrence was at 0-based index $p$, it corresponds to cut position $p+1$. So for cuts $i \in [p+1, j-1]$, the distinct count increases.
    *   We maintain values $V_i = \text{pref}[i] + M_i$ in a Segment Tree. Initially $M_i=0$, so $V_i = \text{pref}[i]$.
    *   For each `j`, we perform a range add of 1 on the segment tree for indices $[\max(1, p+1), j-1]$.
    *   Then we query the maximum value in the range $[1, j-1]$.
    *   The candidate answer is `query_result + suff[j]`.
4.  **Segment Tree**: We use a segment tree with lazy propagation to support range add and range max queries in $O(\log N)$ time.
5.  **Complexity**: Precomputation is $O(N)$. The loop runs $O(N)$ times, each with $O(\log N)$ segment tree operations. Total time complexity is $O(N \log N)$, which fits within the time limit for $N=3 \times 10^5$.
