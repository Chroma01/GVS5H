
## ideation
**Core Difficulty**: The problem requires finding the maximum number of pairs $(a, b)$ such that $a \le b/2$ within a subarray $A[L \dots R]$, where $A$ is sorted. This is a classic greedy problem where we pair the smallest available "top" with the largest available "base" that satisfies the condition. However, with $Q$ queries on different ranges, a naive simulation for each query is $O(N)$, leading to $O(NQ)$ total time, which is too slow ($N, Q \le 2 \times 10^5$).

**Candidate Approaches**:
1.  **Segment Tree with Merge Logic**:
    *   **State**: Each node in the segment tree represents a range $[l, r]$ and stores a tuple `(count, next_start_index)`. `count` is the max pairs formed within that range, and `next_start_index` is the index of the first element in $[l, r]$ that was *not* used as a "top" (i.e., it remains available to be a top for a base from a larger range).
    *   **Merge Logic**: When merging a left child (smaller values) and a right child (larger values):
        *   We already have `left.count` and `right.count` pairs formed internally.
        *   We need to find how many *additional* pairs can be formed by pairing unused tops from the left part with bases from the right part.
        *   The unused tops from the left start at `left.next_start_index`. The bases from the right are processed from the largest (`right.end`) downwards.
        *   We greedily match the smallest available top with the largest available base.
        *   Since the array is sorted, the condition $A[top] \le A[base]/2$ is monotonic. We can use **binary search** to find the maximum number of such pairs $k$ efficiently. Specifically, we check if the $i$-th smallest unused top can pair with the $i$-th largest available base in the right part.
    *   **Query Processing**: For a query $[L, R]$, decompose the range into $O(\log N)$ canonical segment tree nodes. Merge them sequentially from left to right (since the invariant "left part values $\le$ right part values" must be maintained).
    *   **Complexity**: Build $O(N \log N)$. Query $O(\log^2 N)$ (since merging involves binary search). With $N, Q = 2 \times 10^5$, $\log^2 N \approx 324$, total operations $\approx 6 \times 10^7$, which fits within typical time limits (2s) if implemented efficiently in C++ or optimized Python.

2.  **Optimization**:
    *   The binary search inside the merge can be slow. Can we optimize?
    *   Notice that for a fixed left child, `left.next_start_index` changes. But the structure of the right child is fixed.
    *   Actually, $O(\log^2 N)$ is likely the intended solution complexity for this constraint set in Python if the constant factor is small.
    *   Pitfall: Python recursion depth and overhead. Iterative segment tree or careful recursion limit management is needed.

## worker: Implement the iterative Segment Tree solution: def
1.  **Algorithm**: The solution uses a Segment Tree where each node stores `(pairs_count, next_start_index, end_index)`.
    *   `pairs_count`: Max pairs formed within the range.
    *   `next_start_index`: The index of the first element in the range that was NOT used as a "top" (smallest element).
    *   `end_index`: The index of the largest element in the range that is available to be a "base".
2.  **Merge Logic**: When merging a left child (smaller values) and a right child (larger values):
    *   We greedily pair the smallest available tops from the left with the largest available bases from the right.
    *   Since the array is sorted, the condition $A[top] \le A[base]/2$ is monotonic. We use binary search to find the maximum number of such pairs $k$.
    *   The new state is updated: `pairs` increases by $k$, `next_start` moves forward by $k$, and `end` moves backward by $k$ (since the largest $k$ bases are used).
3.  **Query Processing**:
    *   Decompose the query range $[L, R]$ into $O(\log N)$ canonical nodes.
    *   Sort these nodes by their starting index to ensure we merge from smallest to largest values (maintaining the invariant that the left part of the merge is smaller than the right part).
    *   Merge the nodes sequentially.
4.  **Complexity**:
    *   Build: $O(N \log N)$ (each merge is $O(\log N)$ due to binary search).
    *   Query: $O(\log^2 N)$ (collecting $O(\log N)$ nodes, sorting takes $O(\log N \log \log N)$, merging takes $O(\log N \cdot \log N)$).
    *   Given $N, Q \le 2 \times 10^5$, this fits within the time limit.
5.  **Edge Cases**:
    *   Empty ranges (handled by `INF` marker).
    *   Ranges where no pairs can be formed.
    *   Ranges where all elements are used.

## worker: Run the code against the provided sample inputs to
The solution implements a Segment Tree where each node stores the result of the greedy simulation for its range: `(pairs_count, next_start_index, end_index)`.
- `pairs_count`: The maximum number of pairs formed within the range.
- `next_start_index`: The index of the first element in the range that was NOT used as a "top" (i.e., it remains available to be a top for a base from a larger range).
- `end_index`: The index of the largest element in the range that is available to be a "base".

**Merge Logic**:
When merging a left child (smaller values) and a right child (larger values):
1.  We already have `left.pairs` and `right.pairs` pairs formed internally.
2.  We need to find how many *additional* pairs can be formed by pairing unused tops from the left part with bases from the right part.
3.  The unused tops from the left start at `left.next_start_index`. The bases from the right are processed from the largest (`right.end_index`) downwards.
4.  Since the array is sorted, the condition $A[top] \le A[base]/2$ is monotonic. We use **binary search** to find the maximum number of such pairs $k$ efficiently. Specifically, we check if the $i$-th smallest unused top can pair with the $i$-th largest available base in the right part. The condition must hold for all $i < k$, which is guaranteed if it holds for the largest $i$ (due to LHS increasing and RHS decreasing).
5.  The new state is updated: `pairs` increases by $k$, `next_start` moves forward by $k$, and `end` moves backward by $k$ (since the largest $k$ bases are used).

**Query Processing**:
For a query $[L, R]$, we decompose the range into $O(\log N)$ canonical segment tree nodes. We collect these nodes, sort them by their starting index to ensure we merge from smallest to largest values (maintaining the invariant that the left part of the merge is smaller than the right part), and then merge them sequentially.

## worker: Run the provided sample inputs to verify correctne
The solution implements a Segment Tree where each node stores the result of a greedy simulation for its range: `(pairs_count, next_start_index, end_index)`.
- `pairs_count`: The maximum number of pairs formed within the range.
- `next_start_index`: The index of the first element in the range that was NOT used as a "top" (i.e., it remains available to be a top for a base from a larger range).
- `end_index`: The index of the largest element in the range that is available to be a "base".

**Merge Logic**:
When merging a left child (smaller values) and a right child (larger values):
1. We already have `left.pairs` and `right.pairs` pairs formed internally.
2. We need to find how many *additional* pairs can be formed by pairing unused tops from the left part with bases from the right part.
3. The unused tops from the left start at `left.next_start_index`. The bases from the right are processed from the largest (`right.end_index`) downwards.
4. Since the array is sorted, the condition $A[top] \le A[base]/2$ is monotonic. We use **binary search** to find the maximum number of such pairs $k$ efficiently. Specifically, we check if the $i$-th smallest unused top can pair with the $i$-th largest available base in the right part. The condition must hold for all $i < k$, which is guaranteed if it holds for the largest $i$ (due to LHS increasing and RHS decreasing).
5. The new state is updated: `pairs` increases by $k$, `next_start` moves forward by $k$, and `end` moves backward by $k$ (since the largest $k$ bases are used).

**Query Processing**:
For a query $[L, R]$, we decompose the range into $O(\log N)$ canonical segment tree nodes. We collect these nodes, sort them by their starting index to ensure we merge from smallest to largest values (maintaining the invariant that the left part of the merge is smaller than the right part), and then merge them sequentially.

## worker: finalize
The solution implements a Segment Tree where each node stores the result of a greedy simulation for its range: `(pairs_count, next_start_index, end_index)`.
- `pairs_count`: The maximum number of pairs formed within the range.
- `next_start_index`: The index of the first element in the range that was NOT used as a "top" (i.e., it remains available to be a top for a base from a larger range).
- `end_index`: The index of the largest element in the range that is available to be a "base".

**Merge Logic**:
When merging a left child (smaller values) and a right child (larger values):
1. We already have `left.pairs` and `right.pairs` pairs formed internally.
2. We need to find how many *additional* pairs can be formed by pairing unused tops from the left part with bases from the right part.
3. The unused tops from the left start at `left.next_start_index`. The bases from the right are processed from the largest (`right.end_index`) downwards.
4. Since the array is sorted, the condition $A[top] \le A[base]/2$ is monotonic. We use **binary search** to find the maximum number of such pairs $k$ efficiently. Specifically, we check if the $i$-th smallest unused top can pair with the $i$-th largest available base in the right part. The condition must hold for all $i < k$, which is guaranteed if it holds for the largest $i$ (due to LHS increasing and RHS decreasing).
5. The new state is updated: `pairs` increases by $k$, `next_start` moves forward by $k$, and `end` moves backward by $k$ (since the largest $k$ bases are used).

**Query Processing**:
For a query $[L, R]$, we decompose the range into $O(\log N)$ canonical segment tree nodes. We collect these nodes, sort them by their starting index to ensure we merge from smallest to largest values (maintaining the invariant that the left part of the merge is smaller than the right part), and then merge them sequentially.
