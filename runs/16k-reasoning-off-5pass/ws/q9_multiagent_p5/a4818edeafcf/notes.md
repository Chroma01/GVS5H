
## ideation
The problem asks us to split an array $A$ of length $N$ into three non-empty contiguous subarrays at indices $i$ and $j$ ($1 \le i < j \le N-1$) such that the sum of the number of distinct elements in each subarray is maximized.

**Core Difficulty:**
The naive solution iterating over all pairs $(i, j)$ takes $O(N^2)$ time, which is too slow for $N \le 3 \times 10^5$. We need an $O(N \log N)$ or $O(N)$ approach. The challenge lies in efficiently updating the "distinct count" of the middle segment as we iterate through possible split points.

**Candidate Approaches:**
1.  **Iterate the middle split point $j$:**
    Fix $j$ (the end of the second subarray). The third subarray is $A[j+1 \dots N]$. Let $Suf[j] = \text{distinct}(A[j+1 \dots N])$. This is a static value for a fixed $j$.
    We need to maximize $D_1(i) + D_2(i, j)$ where $D_1(i) = \text{distinct}(A[1 \dots i])$ and $D_2(i, j) = \text{distinct}(A[i+1 \dots j])$.
    Note that $D_1(i) + D_2(i, j)$ is not simply $D_{total}(j)$ because of overlaps. However, we can rewrite the objective as:
    $\max_{1 \le i < j} (\text{distinct}(A[1 \dots i]) + \text{distinct}(A[i+1 \dots j])) + Suf[j]$.
    As we iterate $j$ from $2$ to $N-1$, we add $A[j]$ to the middle segment. But the split $i$ can be anywhere before $j$. This direction is slightly tricky because the "middle segment" grows on the right, but the split $i$ is variable.

2.  **Iterate the first split point $i$:**
    Fix $i$ (the end of the first subarray). We need to maximize $\text{distinct}(A[i+1 \dots j]) + \text{distinct}(A[j+1 \dots N])$ for $j \in [i+1, N-1]$.
    Let $f(j) = \text{distinct}(A[j+1 \dots N])$. This can be precomputed for all $j$ in $O(N)$.
    We need $\max_{j > i} (\text{distinct}(A[i+1 \dots j]) + f(j))$.
    Let $g(i, j) = \text{distinct}(A[i+1 \dots j])$.
    As we move $i$ from $1$ to $N-2$:
    - The range $(i+1 \dots j)$ shrinks from the left (element $A_{i+1}$ is removed).
    - For a fixed $j$, if $A_{i+1}$ appears again in $(i+2 \dots j)$, removing it doesn't change the distinct count.
    - If $A_{i+1}$ does *not* appear in $(i+2 \dots j)$, the distinct count decreases by 1.
    - The condition "$A_{i+1}$ does not appear in $(i+2 \dots j)$" is equivalent to $j < \text{next\_occurrence}(A_{i+1})$.
    - So, when moving from $i$ to $i+1$, we need to subtract 1 from the value stored at index $j$ in our data structure for all $j$ in the range $[i+2, \text{next\_occurrence}(A_{i+1}) - 1]$.
    - We can use a **Segment Tree** (or Fenwick Tree if we only needed sums, but we need range updates and global max) to maintain the values $V_j = \text{distinct}(A[i+1 \dots j]) + f(j)$.
    - The segment tree supports:
        1. Range Add: Subtract 1 from $[L, R]$.
        2. Global Max: Query the maximum value in the current range.
    - Algorithm steps:
        1. Precompute `next_occurrence` array for all elements.
        2. Precompute suffix distinct counts $Suf[j]$.
        3. Initialize a Segment Tree with base values corresponding to $i=1$. Specifically, for each $j \in [2, N-1]$, the initial distinct count of $(2 \dots j)$ plus $Suf[j]$.
        4. Iterate $i$ from $1$ to $N-2$.
           - Calculate current max from Segment Tree. Update global answer with $max + Suf[i+1]$? Wait, the split is at $i$ and $j$. The first part is $1..i$. The term we maximize is $\text{distinct}(1..i) + \max_{j}(\dots)$.
           - Actually, let's refine the loop.
           - Let's iterate $i$ from $1$ to $N-2$.
           - We need $\max_{j \in [i+1, N-1]} (\text{distinct}(A[i+1 \dots j]) + Suf[j])$.
           - Let $Val(j) = \text{distinct}(A[i+1 \dots j]) + Suf[j]$.
           - When moving from $i$ to $i+1$:
             - The first part $A[1 \dots i]$ becomes $A[1 \dots i+1]$. The distinct count of the first part increases (or stays same). We can precompute prefix distinct counts $Pre[i]$.
             - The middle part changes from $A[i+1 \dots j]$ to $A[i+2 \dots j]$.
             - We need to update $Val(j)$ for all $j$.
             - If $A_{i+1}$ is the *last* occurrence of that value in the range $(i+1 \dots j)$, then removing it reduces the distinct count by 1.
             - Wait, the logic "if it doesn't appear in $i+2 \dots j$" means $j < \text{next\_occurrence}(A_{i+1})$.
             - Let $R = \text{next\_occurrence}(A_{i+1})$. If $R$ exists and $R \le N$, then for all $j \in [i+2, R-1]$, the element $A_{i+1}$ is unique in the range $(i+1 \dots j)$. Removing it decreases the distinct count by 1.
             - So we perform `RangeAdd(i+2, R-1, -1)` on the segment tree.
             - The value at leaf $j$ is now $\text{distinct}(A[i+2 \dots j]) + Suf[j]$.
             - The answer for split $i+1$ is $Pre[i+1] + \text{QueryMax}()$.
           - Base case: Initialize for $i=1$. Compute distinct counts for ranges $(2 \dots j)$ for all $j$. Build tree.
           - Then loop $i$ from $1$ to $N-2$. Update tree, compute answer.

**Pitfalls:**
- **Indices:** Careful with 1-based vs 0-based indexing. The constraints say $1 \le i < j \le N-1$.
- **Segment Tree Implementation:** Needs to support range add and global max. Lazy propagation is necessary.
- **Next Occurrence:** Need to precompute this efficiently. Can be done by iterating backwards and storing the last seen index for each value.
- **Edge Cases:** $N=3$. Only one split $(1, 2)$.
- **Complexity:** $O(N \log N)$ due to segment tree operations. $N=3 \times 10^5$ fits well within time limits (usually 2s).

## worker: Implement the solution using a Segment Tree with L
The solution uses a Segment Tree with Lazy Propagation to efficiently maintain the maximum value of `distinct(i+1...j) + distinct(j+1...N)` as we iterate through possible split points `i`. 
1. **Precomputation**: We precompute `next_occurrence` for each element to quickly determine the range of `j` where removing `A[i+1]` affects the distinct count of the middle segment. We also precompute suffix distinct counts (`S`) and prefix distinct counts (`Pre`).
2. **Segment Tree**: The tree stores values `distinct(i+1...j) + S[j+1]` for all valid `j`. Initially, for `i=0`, we compute these values.
3. **Iteration**: As we move `i` from `0` to `N-3`, we:
   - Query the maximum value in the valid range of `j` (`j > i`).
   - Update the global answer using `Pre[i] + max_value`.
   - Update the Segment Tree to reflect the change in the middle segment when moving from `i` to `i+1`. Specifically, if `A[i+1]` does not appear again in the range `(i+2...j)`, the distinct count for that `j` decreases by 1. This corresponds to a range update on the Segment Tree.
4. **Complexity**: The precomputation takes $O(N)$. The loop runs $O(N)$ times, and each iteration involves $O(\log N)$ operations on the Segment Tree. Total time complexity is $O(N \log N)$, which fits within the constraints.

## worker: Verify the solution with the provided sample input
The solution implements an $O(N \log N)$ algorithm using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `next_occ`: Stores the index of the next occurrence of each element. This helps in determining the range of $j$ where removing $A[i+1]$ affects the distinct count of the middle segment.
    *   `S`: Stores the number of distinct elements in the suffix $A[j+1 \dots N-1]$.
    *   `Pre`: Stores the number of distinct elements in the prefix $A[0 \dots i]$.
2.  **Segment Tree**:
    *   The tree maintains values $V_j = \text{distinct}(A[i+1 \dots j]) + S[j+1]$ for valid $j$.
    *   It supports range updates (subtracting 1) and range maximum queries.
3.  **Iteration**:
    *   We iterate $i$ from $0$ to $N-3$.
    *   For each $i$, we query the maximum value in the valid range of $j$ ($i+1 \le j \le N-2$) from the Segment Tree.
    *   The answer for the current $i$ is $\text{Pre}[i] + \max(V_j)$.
    *   Before moving to $i+1$, we update the Segment Tree. When moving from $i$ to $i+1$, the element $A[i+1]$ is removed from the start of the middle segment. If $A[i+1]$ does not appear again in the range $(i+2 \dots j)$, the distinct count for that $j$ decreases by 1. This corresponds to a range update on the Segment Tree.
4.  **Edge Cases**:
    *   $N < 3$: Handled by printing 0.
    *   Ranges for Segment Tree updates are carefully bounded to ensure they stay within valid indices.

## worker: Run the provided sample inputs to verify correctne
The provided solution implements the $O(N \log N)$ algorithm using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `next_occ`: Stores the index of the next occurrence of each element. This helps in determining the range of $j$ where removing $A[i+1]$ affects the distinct count of the middle segment.
    *   `S`: Stores the number of distinct elements in the suffix $A[j+1 \dots N-1]$.
    *   `Pre`: Stores the number of distinct elements in the prefix $A[0 \dots i]$.
2.  **Segment Tree**:
    *   The tree maintains values $V_j = \text{distinct}(A[i+1 \dots j]) + S[j+1]$ for valid $j$.
    *   It supports range updates (subtracting 1) and range maximum queries.
3.  **Iteration**:
    *   We iterate $i$ from $0$ to $N-3$.
    *   For each $i$, we query the maximum value in the valid range of $j$ ($i+1 \le j \le N-2$) from the Segment Tree.
    *   The answer for the current $i$ is $\text{Pre}[i] + \max(V_j)$.
    *   Before moving to $i+1$, we update the Segment Tree. When moving from $i$ to $i+1$, the element $A[i+1]$ is removed from the start of the middle segment. If $A[i+1]$ does not appear again in the range $(i+2 \dots j)$, the distinct count for that $j$ decreases by 1. This corresponds to a range update on the Segment Tree.
4.  **Edge Cases**:
    *   $N < 3$: Handled by printing 0.
    *   Ranges for Segment Tree updates are carefully bounded to ensure they stay within valid indices.

The logic correctly handles the transition from split point $i$ to $i+1$ by identifying exactly which $j$ values lose a distinct element in the middle segment (those where $A[i+1]$ was the last occurrence in the current middle segment range).

## worker: finalize
The solution implements an $O(N \log N)$ algorithm using a Segment Tree with Lazy Propagation.
1.  **Precomputation**:
    *   `next_occ`: Stores the index of the next occurrence of each element. This helps in determining the range of $j$ where removing $A[i+1]$ affects the distinct count of the middle segment.
    *   `S`: Stores the number of distinct elements in the suffix $A[j+1 \dots N-1]$.
    *   `Pre`: Stores the number of distinct elements in the prefix $A[0 \dots i]$.
2.  **Segment Tree**:
    *   The tree maintains values $V_j = \text{distinct}(A[i+1 \dots j]) + S[j+1]$ for valid $j$.
    *   It supports range updates (subtracting 1) and range maximum queries.
3.  **Iteration**:
    *   We iterate $i$ from $0$ to $N-3$.
    *   For each $i$, we query the maximum value in the valid range of $j$ ($i+1 \le j \le N-2$) from the Segment Tree.
    *   The answer for the current $i$ is $\text{Pre}[i] + \max(V_j)$.
    *   Before moving to $i+1$, we update the Segment Tree. When moving from $i$ to $i+1$, the element $A[i+1]$ is removed from the start of the middle segment. If $A[i+1]$ does not appear again in the range $(i+2 \dots j)$, the distinct count for that $j$ decreases by 1. This corresponds to a range update on the Segment Tree.
4.  **Edge Cases**:
    *   $N < 3$: Handled by printing 0.
    *   Ranges for Segment Tree updates are carefully bounded to ensure they stay within valid indices.

The logic correctly handles the transition from split point $i$ to $i+1$ by identifying exactly which $j$ values lose a distinct element in the middle segment (those where $A[i+1]$ was the last occurrence in the current middle segment range).
