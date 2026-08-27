
## ideation
The problem requires splitting an array $A$ of length $N$ into three non-empty contiguous subarrays by choosing two split points $i$ and $j$ ($1 \le i < j \le N-1$). We need to maximize the sum of the number of distinct elements in each subarray: $A[0..i-1]$, $A[i..j-1]$, and $A[j..N-1]$.

A naive $O(N^2)$ solution checking all pairs $(i, j)$ is too slow for $N \le 3 \times 10^5$. We need an $O(N \log N)$ or $O(N)$ approach.

Let $pre[k]$ be the number of distinct elements in $A[0..k-1]$.
Let $suf[k]$ be the number of distinct elements in $A[k..N-1]$.
The total score for a split $(i, j)$ is $pre[i] + \text{distinct}(A[i..j-1]) + suf[j]$.

The term $\text{distinct}(A[i..j-1])$ depends on both $i$ and $j$. We can iterate over the second split point $j$ (from $2$ to $N-1$) and maintain the value $pre[i] + \text{distinct}(A[i..j-1])$ for all valid $i$ ($1 \le i \le j-1$).

Let $D_i(j) = \text{distinct}(A[i..j-1])$.
When we move from $j$ to $j+1$, we include $A[j]$ into the middle part for all $i \le j$.
$D_i(j+1) = D_i(j) + 1$ if $A[j]$ is not present in $A[i..j-1]$.
$A[j]$ is not present in $A[i..j-1]$ if the previous occurrence of $A[j]$, say at index $p = \text{prev\_occ}[j]$, satisfies $p < i$.
So, for all $i$ in the range $(\text{prev\_occ}[j], j]$, $D_i$ increases by 1.

We can use a Segment Tree to maintain the values $V_i = pre[i] + D_i$.
1. Initialize the segment tree with $V_i = pre[i]$ for $i \in [1, N-2]$. Initially, $D_i=0$.
2. Iterate $j$ from $2$ to $N-1$:
   a. Identify $p = \text{prev\_occ}[j]$. If $A[j]$ hasn't appeared before, $p = -1$.
   b. Update the segment tree: add 1 to the range $[\max(1, p+1), j]$. Note that we only care about $i \le j-1$ for the query, but updating up to $j$ is harmless as long as we query correctly. Specifically, the range of $i$ affected is $p+1 \le i \le j$. Since we query for $i \in [1, j-1]$, the update affects indices up to $j-1$ (if $j-1 \ge p+1$).
   c. Query the maximum value in the range $[1, j-1]$ from the segment tree. Let this be $M_j$.
   d. The candidate answer for this $j$ is $M_j + suf[j]$.
   e. Update the global maximum.

Complexity:
- Precomputing `pre`, `suf`, and `prev_occ` takes $O(N)$.
- Building the segment tree takes $O(N)$.
- The loop runs $N$ times, each iteration involves a range update and a range max query on the segment tree, taking $O(\log N)$.
- Total time complexity: $O(N \log N)$.
- Space complexity: $O(N)$.

This fits within the constraints.

Pitfalls:
- Indexing: Be careful with 0-based vs 1-based indexing. The problem uses 1-based indexing for description, but Python uses 0-based.
- The segment tree should cover indices $1$ to $N-2$ for $i$.
- When updating the range, ensure indices are within bounds.
- The middle part must be non-empty, so $i \le j-1$. The third part must be non-empty, so $j \le N-1$. The first part must be non-empty, so $i \ge 1$. Thus $1 \le i \le j-1$ and $2 \le j \le N-1$.

## worker: (none)
The solution uses a segment tree to efficiently compute the maximum sum of distinct counts for three subarrays.
1. **Precomputation**:
   - `pre[i]` stores the number of distinct elements in `A[0...i-1]`.
   - `suf[j]` stores the number of distinct elements in `A[j...N-1]`.
   - `prev_occ[k]` stores the index of the previous occurrence of `A[k]`.
2. **Segment Tree**:
   - The segment tree maintains values `V[i] = pre[i] + distinct(A[i...j-1])` for each possible first split point `i`.
   - Initially, `distinct(A[i...j-1])` is 0 for all `i` (conceptually, before any middle elements are added). So `V[i]` is initialized to `pre[i]`.
   - As we iterate `j` from 2 to `N-1`, we add `A[j-1]` to the middle part. This increases the distinct count for the middle part `A[i...j-1]` by 1 for all `i` such that `A[j-1]` was not present in `A[i...j-2]`. This condition is equivalent to `i > prev_occ[j-1]`.
   - Thus, we perform a range add of 1 on the segment tree for indices `i` in `[max(1, prev_occ[j-1]+1), j-1]`.
   - After the update, we query the maximum value in the range `[1, j-1]` from the segment tree. This gives us `max_i (pre[i] + distinct(A[i...j-1]))`.
   - The candidate answer for this `j` is this maximum value plus `suf[j]`.
3. **Complexity**:
   - Precomputation takes $O(N)$.
   - Building the segment tree takes $O(N)$.
   - The loop runs $N$ times, with each iteration performing $O(\log N)$ operations for range update and range query.
   - Total time complexity is $O(N \log N)$, which fits within the constraints for $N \le 3 \times 10^5$.
   - Space complexity is $O(N)$ for the arrays and segment tree.
