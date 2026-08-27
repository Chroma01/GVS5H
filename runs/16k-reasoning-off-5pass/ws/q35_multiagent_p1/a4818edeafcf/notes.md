
## ideation
The problem requires splitting an array of length $N$ into three non-empty contiguous subarrays to maximize the sum of distinct elements in each subarray. A naive $O(N^2)$ solution checking all split points $(i, j)$ is too slow for $N \le 3 \times 10^5$.

Key observations:
1. Let the split points be $i$ and $j$ with $1 \le i < j \le N-1$ (1-indexed). The subarrays are $A[1..i]$, $A[i+1..j]$, and $A[j+1..N]$.
2. We can precompute prefix distinct counts `pre[k]` (distinct in $A[1..k]$) and suffix distinct counts `suf[k]` (distinct in $A[k..N]$).
3. The total score is `pre[i] + distinct(A[i+1..j]) + suf[j+1]`.
4. We can iterate over the right split point $j$ (from $2$ to $N-1$). For a fixed $j$, we need to maximize `pre[i] + distinct(A[i+1..j])` for $1 \le i \le j-1$.
5. Let $f_j(i) = \text{pre}[i] + \text{distinct}(A[i+1..j])$. When moving from $j$ to $j+1$, the element $A[j+1]$ is added to the middle segment for all $i$. The distinct count increases by 1 for all $i$ such that $A[j+1]$ is not present in $A[i+1..j]$. This condition is equivalent to $i < \text{last\_pos}[A[j+1]]$, where $\text{last\_pos}[x]$ is the last occurrence of $x$ before index $j+1$.
6. Specifically, if the last occurrence of $A[j+1]$ is at index $p$, then for all $i$ such that $i+1 \le p$ (i.e., $i \le p-1$), the element $A[j+1]$ is already in the segment $A[i+1..j]$, so the distinct count doesn't change. For $i \ge p$, the element $A[j+1]$ is new, so the distinct count increases by 1.
7. We can maintain an array `val[i] = pre[i] + distinct(A[i+1..current_j])` using a Segment Tree with lazy propagation. Initially, for $j=1$, the middle segment is empty, but we start iterating $j$ from 2.
   - Initialize `val[i] = pre[i]` for all $i$. This corresponds to the state where the middle segment is empty (or just before adding the first element of the middle segment). Actually, it's easier to start with $j=1$ conceptually, but the middle segment must be non-empty.
   - Let's refine: Iterate $j$ from $2$ to $N-1$. The middle segment is $A[i+1..j]$.
   - Before processing $j$, we have values for middle segment ending at $j-1$. When we move to $j$, we add $A[j]$ to the middle segment.
   - Let $p$ be the last position of $A[j]$ in $A[1..j-1]$. If $A[j]$ hasn't appeared, $p=0$.
   - For $i$ such that $i+1 \le p \iff i \le p-1$, the distinct count doesn't change.
   - For $i$ such that $i+1 > p \iff i \ge p$, the distinct count increases by 1.
   - So, we perform a range add of 1 on indices $[p, j-1]$ in our segment tree. Note that $i$ can go up to $j-1$.
   - After updating, we query the maximum value in range $[1, j-1]$. Let this max be $M_j$.
   - The answer candidate for this $j$ is $M_j + \text{suf}[j+1]$.
8. The segment tree needs to support range add and range max query. Size $N$. Complexity $O(N \log N)$.

Pitfalls:
- Indexing: Be careful with 0-indexed vs 1-indexed arrays.
- The range for update: The middle segment starts at $i+1$. If the last occurrence of $A[j]$ is at $p$, then for start indices $s \le p$, $A[j]$ is already in $A[s..j-1]$. The start index $s = i+1$. So $i+1 \le p \implies i \le p-1$. Thus, for $i \in [1, p-1]$, no change. For $i \in [p, j-1]$, add 1. If $p=0$, then all $i \in [1, j-1]$ get +1.
- Initial state: Before any $j$, we can consider the "middle segment" as empty. But we need to start the loop.
  - Let's initialize the segment tree with `pre[i]` for $i=1..N-2$. This represents `pre[i] + distinct(empty)`. But distinct(empty) is 0. However, the middle segment must be non-empty.
  - We iterate $j$ from $2$ to $N-1$.
  - At step $j$, we add $A[j]$ to the middle segment. The middle segment becomes $A[i+1..j]$.
  - Before adding $A[j]$, the segment was $A[i+1..j-1]$.
  - So, we update the values based on adding $A[j]$.
  - Initial values in segtree: `val[i] = pre[i]`. This corresponds to distinct count 0 for an empty middle segment.
  - When $j=2$, we add $A[2]$. Last pos of $A[2]$ in $A[1..1]$ is $p$. Update range $[p, 1]$ (since $j-1=1$). Query max in $[1, 1]$. Add `suf[3]`.
  - This works.

## worker: Implement the Segment Tree with lazy propagation f
The solution uses a segment tree with lazy propagation to efficiently compute the maximum sum of distinct elements across three subarrays.
1. **Precomputation**: We compute prefix distinct counts (`pre`) and suffix distinct counts (`suf`) in $O(N)$ time.
2. **Segment Tree**: We maintain an array `val[i] = pre[i] + distinct(A[i...j-1])` in a segment tree. Initially, for $j=1$, the middle segment is empty, so `val[i] = pre[i]`.
3. **Iteration**: We iterate $j$ from 2 to $N-1$. For each $j$, we add $A[j-1]$ to the middle segment. The distinct count for a middle segment starting at $i$ increases by 1 if $A[j-1]$ was not present in $A[i...j-2]$. This happens if the last occurrence of $A[j-1]$ was at an index $p < i$. Thus, we perform a range add of 1 on indices $i \in [\max(1, p+1), j-1]$.
4. **Query**: After updating, we query the maximum value in the range $[1, j-1]$ and add `suf[j]` to get the candidate answer for split point $j$.
5. **Complexity**: Each update and query takes $O(\log N)$ time, leading to an overall time complexity of $O(N \log N)$, which fits within the constraints for $N \le 3 \times 10^5$.
