
## ideation
The problem asks us to split an array $A$ of length $N$ into three non-empty contiguous subarrays such that the sum of the counts of distinct integers in these subarrays is maximized. The constraints are $N \le 3 \times 10^5$, which requires an $O(N)$ or $O(N \log N)$ solution.

**Core Difficulty:**
Naively iterating over all pairs of split points $(i, j)$ takes $O(N^2)$, which is too slow. We need to optimize the search for the second split point $j$ for each first split point $i$.

**Candidate Approaches:**
1.  **Prefix/Suffix Arrays + Optimization:**
    *   Precompute `pref[i]` (distinct count in $A[1..i]$) and `suff[j]` (distinct count in $A[j..N]$).
    *   The problem becomes maximizing `pref[i] + distinct(i+1, j) + suff[j+1]`.
    *   For a fixed $i$, we need $\max_{j} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
    *   Let $f_i(j) = \text{distinct}(i+1, j) + \text{suff}[j+1]$. As $i$ decreases, the set of elements in the prefix $A[1..i]$ changes. Specifically, when moving from $i+1$ to $i$, the element $A[i]$ is added to the "left" part, which effectively means for the range of $j$ where $A[i]$ does not appear in $A[i+1..j]$, the term $\text{distinct}(i+1, j)$ increases by 1.
    *   This suggests a Segment Tree approach where we maintain the values of $f_i(j)$ for all valid $j$.
    *   **Algorithm:**
        1.  Compute `suff` array.
        2.  Precompute `next_occurrence[x]` for each element $x$, which gives the index of the first occurrence of $x$ after index $x$.
        3.  Initialize a Segment Tree over indices $1$ to $N-1$. The value at index $j$ will store $\text{distinct}(i+1, j) + \text{suff}[j+1]$.
        4.  Iterate $i$ from $N-2$ down to $1$.
            *   Identify the range of $j$ where $A[i]$ is "new" relative to $A[i+1..j]$. This is the range $[i+1, \text{next\_occurrence}[A[i]] - 1]$.
            *   Update the Segment Tree: Add 1 to the range $[i+1, \text{next\_occurrence}[A[i]] - 1]$. (If the end of the range is less than start, do nothing).
            *   Query the maximum value in the range $[i+1, N-1]$. Let this be $M_i$.
            *   The answer candidate is `pref[i] + M_i`.
        5.  Track the maximum candidate.

2.  **Two Pointers / Monotonic Stack:**
    *   Sometimes distinct count problems can be solved with two pointers, but the "max of sum of distincts" usually doesn't have the monotonicity required for simple two pointers because adding an element to the left can increase the distinct count non-monotonically with respect to the right split point in a way that isn't easily traversable without a data structure. The Segment Tree approach is more robust here.

**Pitfalls:**
*   **1-based vs 0-based indexing:** Careful with array bounds. The split points $i$ and $j$ are 1-based in the problem statement ($1 \le i < j \le N-1$).
*   **Empty Ranges:** Ensure the ranges passed to the Segment Tree update/query are valid (start $\le$ end).
*   **Precomputation:** `next_occurrence` array needs to be computed efficiently (e.g., by iterating backwards and storing the last seen position).
*   **Segment Tree Implementation:** Needs to support Range Add and Range Max Query. Lazy propagation is necessary.

**Complexity:**
*   Precomputing `suff`: $O(N)$.
*   Precomputing `next_occurrence`: $O(N)$.
*   Segment Tree operations: $N$ updates and $N$ queries, each $O(\log N)$. Total $O(N \log N)$.
*   Space: $O(N)$.

This fits within the time limits.

## worker: Implement the solution using a Segment Tree with L
The solution uses a Segment Tree with Lazy Propagation to efficiently handle range updates and range maximum queries.
1.  **Precomputation**:
    *   `suff[k]`: Stores the number of distinct integers in the suffix $A[k \dots N-1]$.
    *   `next_occ[k]`: Stores the index of the first occurrence of $A[k]$ after index $k$.
    *   `pref[i]`: Stores the number of distinct integers in the prefix $A[0 \dots i]$.
2.  **Segment Tree Initialization**:
    *   The segment tree is built over indices $0$ to $N-2$ (representing possible end points of the middle subarray $j$).
    *   Initially, for the state corresponding to $i = N-3$, the value at index $j$ is set to $1 + \text{suff}[j+1]$. This represents $\text{distinct}(N-2, j) + \text{suff}[j+1]$.
3.  **Iteration**:
    *   We iterate $i$ from $N-3$ down to $0$.
    *   For each $i$, we query the maximum value in the range $[i+1, N-2]$. This gives $\max_j (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
    *   We add this to `pref[i]` to get a candidate answer.
    *   Before moving to $i-1$, we update the segment tree. The element $A[i]$ is added to the "left" of the middle part. For any $j$ where $A[i]$ does not appear in $A[i+1 \dots j]$ (i.e., $j < \text{next\_occ}[i]$), the distinct count increases by 1. We perform a range add of 1 on $[i+1, \min(\text{next\_occ}[i]-1, N-2)]$.
4.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree operations: $N$ queries and updates, each $O(\log N)$. Total $O(N \log N)$.
    *   Space: $O(N)$.

## worker: Run the code against sample inputs to verify corre
The code implements the $O(N \log N)$ solution using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `suff[k]`: Number of distinct elements in $A[k \dots N-1]$.
    *   `next_occ[k]`: Index of the first occurrence of $A[k]$ after index $k$.
    *   `pref[i]`: Number of distinct elements in $A[0 \dots i]$.
2.  **Segment Tree**:
    *   The tree maintains values $V_j = \text{distinct}(i+1, j) + \text{suff}[j+1]$ for valid split points $j$.
    *   Initially (for the conceptual state before the loop), we set $V_j = 1 + \text{suff}[j+1]$. This corresponds to the base case where the middle subarray starts at $i+1$ and contains only $A[i+1]$ (distinct count 1).
    *   We iterate $i$ from $N-3$ down to $0$.
    *   **Query**: For the current $i$, we query the maximum value in the range $[i+1, N-2]$. This gives $\max_j (\text{distinct}(i+1, j) + \text{suff}[j+1])$. We add `pref[i]` to this to get the total distinct count for the split $(i, j)$.
    *   **Update**: Before moving to $i-1$, we need to update the values in the tree to reflect that the middle subarray now starts at $i$ instead of $i+1$. The element $A[i]$ is added to the left of the middle subarray. For any $j$ such that $A[i]$ does not appear in $A[i+1 \dots j]$ (i.e., $j < \text{next\_occ}[i]$), the distinct count of the middle subarray increases by 1. We perform a range add of 1 on $[i+1, \min(\text{next\_occ}[i]-1, N-2)]$.
3.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree operations: $N$ queries and updates, each $O(\log N)$. Total $O(N \log N)$.
    *   Space: $O(N)$.

The logic handles the constraints $N \le 3 \times 10^5$ efficiently.

## worker: Run the provided code against Sample Input 1 and S
The code implements the $O(N \log N)$ solution using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `suff[k]`: Number of distinct elements in $A[k \dots N-1]$.
    *   `next_occ[k]`: Index of the first occurrence of $A[k]$ after index $k$.
    *   `pref[i]`: Number of distinct elements in $A[0 \dots i]$.
2.  **Segment Tree**:
    *   The tree maintains values $V_j = \text{distinct}(i+1, j) + \text{suff}[j+1]$ for valid split points $j$.
    *   Initially (for the conceptual state before the loop), we set $V_j = 1 + \text{suff}[j+1]$. This corresponds to the base case where the middle subarray starts at $i+1$ and contains only $A[i+1]$ (distinct count 1).
    *   We iterate $i$ from $N-3$ down to $0$.
    *   **Query**: For the current $i$, we query the maximum value in the range $[i+1, N-2]$. This gives $\max_j (\text{distinct}(i+1, j) + \text{suff}[j+1])$. We add `pref[i]` to this to get the total distinct count for the split $(i, j)$.
    *   **Update**: Before moving to $i-1$, we need to update the values in the tree to reflect that the middle subarray now starts at $i$ instead of $i+1$. The element $A[i]$ is added to the left of the middle subarray. For any $j$ such that $A[i]$ does not appear in $A[i+1 \dots j]$ (i.e., $j < \text{next\_occ}[i]$), the distinct count of the middle subarray increases by 1. We perform a range add of 1 on $[i+1, \min(\text{next\_occ}[i]-1, N-2)]$.
3.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree operations: $N$ queries and updates, each $O(\log N)$. Total $O(N \log N)$.
    *   Space: $O(N)$.

The logic handles the constraints $N \le 3 \times 10^5$ efficiently.

## worker: Run the code against Sample Input 1 and Sample Inp
The code implements the $O(N \log N)$ solution using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `suff[k]`: Number of distinct elements in $A[k \dots N-1]$.
    *   `next_occ[k]`: Index of the first occurrence of $A[k]$ after index $k$.
    *   `pref[i]`: Number of distinct elements in $A[0 \dots i]$.
2.  **Segment Tree**:
    *   The tree maintains values $V_j = \text{distinct}(i+1, j) + \text{suff}[j+1]$ for valid split points $j$.
    *   Initially (for the conceptual state before the loop), we set $V_j = 1 + \text{suff}[j+1]$. This corresponds to the base case where the middle subarray starts at $i+1$ and contains only $A[i+1]$ (distinct count 1).
    *   We iterate $i$ from $N-3$ down to $0$.
    *   **Query**: For the current $i$, we query the maximum value in the range $[i+1, N-2]$. This gives $\max_j (\text{distinct}(i+1, j) + \text{suff}[j+1])$. We add `pref[i]` to this to get the total distinct count for the split $(i, j)$.
    *   **Update**: Before moving to $i-1$, we need to update the values in the tree to reflect that the middle subarray now starts at $i$ instead of $i+1$. The element $A[i]$ is added to the left of the middle subarray. For any $j$ such that $A[i]$ does not appear in $A[i+1 \dots j]$ (i.e., $j < \text{next\_occ}[i]$), the distinct count of the middle subarray increases by 1. We perform a range add of 1 on $[i+1, \min(\text{next\_occ}[i]-1, N-2)]$.
3.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree operations: $N$ queries and updates, each $O(\log N)$. Total $O(N \log N)$.
    *   Space: $O(N)$.

The logic handles the constraints $N \le 3 \times 10^5$ efficiently.

## worker: finalize
The solution implements an $O(N \log N)$ algorithm using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `suff[k]`: Stores the number of distinct integers in the suffix $A[k \dots N-1]$.
    *   `next_occ[k]`: Stores the index of the first occurrence of $A[k]$ after index $k$.
    *   `pref[i]`: Stores the number of distinct integers in the prefix $A[0 \dots i]$.
2.  **Segment Tree Logic**:
    *   The segment tree maintains values $V_j = \text{distinct}(i+1, j) + \text{suff}[j+1]$ for valid split points $j$ (where $j$ is the end of the middle subarray).
    *   Initially (conceptually for the state before the loop starts), we set $V_j = 1 + \text{suff}[j+1]$. This corresponds to the base case where the middle subarray starts at $i+1$ and contains only $A[i+1]$ (distinct count 1).
    *   We iterate $i$ from $N-3$ down to $0$.
    *   **Query**: For the current $i$, we query the maximum value in the range $[i+1, N-2]$. This gives $\max_j (\text{distinct}(i+1, j) + \text{suff}[j+1])$. We add `pref[i]` to this to get the total distinct count for the split $(i, j)$.
    *   **Update**: Before moving to $i-1$, we need to update the values in the tree to reflect that the middle subarray now starts at $i$ instead of $i+1$. The element $A[i]$ is added to the left of the middle subarray. For any $j$ such that $A[i]$ does not appear in $A[i+1 \dots j]$ (i.e., $j < \text{next\_occ}[i]$), the distinct count of the middle subarray increases by 1. We perform a range add of 1 on $[i+1, \min(\text{next\_occ}[i]-1, N-2)]$.
3.  **Complexity**:
    *   Precomputation: $O(N)$.
    *   Segment Tree operations: $N$ queries and updates, each $O(\log N)$. Total $O(N \log N)$.
    *   Space: $O(N)$.

This approach efficiently handles the constraints $N \le 3 \times 10^5$.
