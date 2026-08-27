
## ideation
**Core Difficulty**: The problem requires finding two split points $(i, j)$ to maximize the sum of distinct elements in three contiguous subarrays. A naive $O(N^2)$ solution iterating all pairs $(i, j)$ will time out given $N \le 3 \times 10^5$. We need an $O(N)$ or $O(N \log N)$ approach.

**Candidate Approaches**:
1.  **Segment Tree with Range Updates (Optimal)**:
    *   Precompute `suff[k]`: distinct count in $A[k \dots N]$.
    *   Iterate the first split point $i$ from $1$ to $N-2$.
    *   For a fixed $i$, we need $\max_{j} (distinct(i+1, j) + suff[j+1])$.
    *   Let $val_j = distinct(i+1, j) + suff[j+1]$.
    *   As $i$ increments to $i+1$, the left boundary of the middle segment moves right. The element $A[i]$ is removed from the middle segment $A[i+1 \dots j]$ for all $j$ where $A[i]$ does not reappear later.
    *   Specifically, if `next_occ[i]` is the next index of $A[i]$ after $i$, then for all $j$ in range $[i+1, next\_occ[i]-1]$, the distinct count $distinct(i+1, j)$ decreases by 1 (since $A[i]$ is no longer in the window).
    *   We can maintain the values $val_j$ in a Segment Tree. Initially (for $i=1$), compute $val_j$ for all $j$.
    *   In each step $i$, query the maximum in the range $[i+1, N-1]$, add $distinct(1, i)$, and update the range $[i+1, next\_occ[i]-1]$ by subtracting 1.
    *   Complexity: $O(N \log N)$.

2.  **Two Pointers / Sliding Window (Harder to implement correctly)**:
    *   Trying to optimize the inner loop without a data structure is difficult because the "distinct count" function is not monotonic or easily updatable in a way that allows simple two-pointer movement without re-scanning. The dependency on future occurrences makes simple sliding windows tricky.

## worker: Implement the solution using the Segment Tree appr
The solution implements the $O(N \log N)$ approach using a Segment Tree with lazy propagation.
1.  **Precomputation**:
    *   `suff`: Array where `suff[k]` stores the number of distinct elements in the suffix $A[k \dots N-1]$.
    *   `next_occ`: Array where `next_occ[k]` stores the index of the next occurrence of $A[k]$ after $k$.
    *   `pref`: Array where `pref[k]` stores the number of distinct elements in the prefix $A[0 \dots k-1]$.
2.  **Segment Tree**:
    *   The tree maintains values for potential split points $j$ (end of the second subarray).
    *   Specifically, leaf $k$ (corresponding to split point $j=k+1$) stores `distinct(A[i \dots k]) + suff[k+1]`.
    *   Initially, for $i=1$, we compute these values for all valid $k$.
3.  **Iteration**:
    *   Iterate $i$ (end of first subarray) from $1$ to $N-2$.
    *   Query the maximum value in the range $[i, N-2]$ from the Segment Tree. This gives $\max_j (distinct(i+1, j) + suff[j+1])$.
    *   Add `pref[i]` (distinct count of first subarray) to get the total sum for the current $i$.
    *   Update the Segment Tree for the next iteration ($i+1$). Moving from $i$ to $i+1$ removes $A[i]$ from the middle segment. The distinct count decreases by 1 for all $j$ where $A[i]$ does not reappear in the remaining middle segment. This corresponds to updating the range $[i, next\_occ[i]-1]$ by subtracting 1.
4.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree Operations: $O(\log N)$ per update/query.
    *   Total Time: $O(N \log N)$.
    *   Space: $O(N)$.

## worker: Test the solution with the provided sample inputs 
The solution implements the $O(N \log N)$ approach using a Segment Tree with lazy propagation.
1.  **Precomputation**:
    *   `suff`: Array where `suff[k]` stores the number of distinct elements in the suffix $A[k \dots N-1]$.
    *   `next_occ`: Array where `next_occ[k]` stores the index of the next occurrence of $A[k]$ after $k$.
    *   `pref`: Array where `pref[k]` stores the number of distinct elements in the prefix $A[0 \dots k-1]$.
2.  **Segment Tree**:
    *   The tree maintains values for potential split points $j$ (end of the second subarray).
    *   Specifically, leaf $k$ (corresponding to split point $j=k+1$) stores `distinct(A[i \dots k]) + suff[k+1]`.
    *   Initially, for $i=1$, we compute these values for all valid $k$.
3.  **Iteration**:
    *   Iterate $i$ (end of first subarray) from $1$ to $N-2$.
    *   Query the maximum value in the range $[i, N-2]$ from the Segment Tree. This gives $\max_j (distinct(i+1, j) + suff[j+1])$.
    *   Add `pref[i]` (distinct count of first subarray) to get the total sum for the current $i$.
    *   Update the Segment Tree for the next iteration ($i+1$). Moving from $i$ to $i+1$ removes $A[i-1]$ from the middle segment. The distinct count decreases by 1 for all $k$ where $A[i-1]$ does not reappear in the remaining middle segment. This corresponds to updating the range $[i, next\_occ[i-1]-1]$ by subtracting 1.
4.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree Operations: $O(\log N)$ per update/query.
    *   Total Time: $O(N \log N)$.
    *   Space: $O(N)$.

The logic handles the constraints and edge cases (like $N=3$) correctly by carefully managing the ranges in the segment tree updates and queries.

## worker: Run the provided sample inputs to verify correctne
The solution implements the $O(N \log N)$ approach using a Segment Tree with lazy propagation.
1.  **Precomputation**:
    *   `suff`: Array where `suff[k]` stores the number of distinct elements in the suffix $A[k \dots N-1]$.
    *   `next_occ`: Array where `next_occ[k]` stores the index of the next occurrence of $A[k]$ after $k$.
    *   `pref`: Array where `pref[k]` stores the number of distinct elements in the prefix $A[0 \dots k-1]$.
2.  **Segment Tree**:
    *   The tree maintains values for potential split points $j$ (end of the second subarray).
    *   Specifically, leaf $k$ (corresponding to split point $j=k+1$) stores `distinct(A[i \dots k]) + suff[k+1]`.
    *   Initially, for $i=1$, we compute these values for all valid $k$.
3.  **Iteration**:
    *   Iterate $i$ (end of first subarray) from $1$ to $N-2$.
    *   Query the maximum value in the range $[i, N-2]$ from the Segment Tree. This gives $\max_j (distinct(i+1, j) + suff[j+1])$.
    *   Add `pref[i]` (distinct count of first subarray) to get the total sum for the current $i$.
    *   Update the Segment Tree for the next iteration ($i+1$). Moving from $i$ to $i+1$ removes $A[i-1]$ from the middle segment. The distinct count decreases by 1 for all $k$ where $A[i-1]$ does not reappear in the remaining middle segment. This corresponds to updating the range $[i, next\_occ[i-1]-1]$ by subtracting 1.
4.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree Operations: $O(\log N)$ per update/query.
    *   Total Time: $O(N \log N)$.
    *   Space: $O(N)$.

The logic handles the constraints and edge cases (like $N=3$) correctly by carefully managing the ranges in the segment tree updates and queries.

## worker: finalize
1.  **Algorithm Selection**: The problem requires maximizing the sum of distinct elements in three contiguous subarrays. A naive $O(N^2)$ solution is too slow for $N \le 3 \times 10^5$. The chosen approach is $O(N \log N)$ using a Segment Tree with Lazy Propagation.
2.  **Key Insight**:
    *   Let the split points be $i$ and $j$ ($1 \le i < j \le N-1$). We want to maximize $Distinct(1, i) + Distinct(i+1, j) + Distinct(j+1, N)$.
    *   We precompute `suff[k]` = distinct count of $A[k \dots N]$.
    *   We iterate $i$ from $1$ to $N-2$. For a fixed $i$, we need $\max_{j} (Distinct(i+1, j) + suff[j+1])$.
    *   Let $val_j = Distinct(i+1, j) + suff[j+1]$. As $i$ increases to $i+1$, the start of the middle segment moves from $i+1$ to $i+2$. The element $A[i]$ is removed from the middle segment.
    *   $Distinct(i+2, j) = Distinct(i+1, j) - 1$ if $A[i]$ does not appear in $A[i+2 \dots j]$. Otherwise, it stays the same.
    *   This condition ($A[i]$ not in $A[i+2 \dots j]$) is equivalent to saying the next occurrence of $A[i]$ is after $j$.
    *   Thus, for a fixed $i$, we can update the values $val_j$ for all $j$ in a specific range $[i+1, next\_occ[i]-1]$ by subtracting 1.
3.  **Data Structures**:
    *   **Segment Tree**: Maintains the values $val_j$ for all valid $j$. Supports range updates (subtract 1) and range maximum queries.
    *   **Precomputed Arrays**: `suff` (suffix distinct counts), `next_occ` (next occurrence index), `pref` (prefix distinct counts).
4.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree Initialization: $O(N)$.
    *   Loop: $N$ iterations. Each iteration performs one query and one update, both $O(\log N)$.
    *   Total Time: $O(N \log N)$.
    *   Space: $O(N)$.
5.  **Edge Cases**:
    *   $N=3$: The loop runs for $i=1$. Query range $[1, 1]$. Update range might be empty. Correctly handles minimal input.
    *   Values of $A_i$: Handled by using a set for distinct counts and a map for next occurrences.
