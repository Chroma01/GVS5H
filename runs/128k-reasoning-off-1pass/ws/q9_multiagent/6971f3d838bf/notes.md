
## ideation
The problem asks us to find the maximum subarray sum after optionally removing all occurrences of a single integer $x$. The constraints are $N \le 10^5$, which rules out $O(N^2)$ solutions where we iterate over each unique number and run Kadane's algorithm on the modified array.

**Core Difficulty:**
We need to efficiently calculate the maximum subarray sum for the array $nums \setminus \{x\}$ for every unique $x$ in $nums$. A naive simulation is too slow. The key observation is that removing $x$ splits the original array into several contiguous segments. The maximum subarray sum of the new array is simply the maximum of the maximum subarray sums of these individual segments.

**Candidate Approaches:**
1.  **Segment Tree with Range Queries:**
    *   Build a Segment Tree where each node stores the `max_subarray`, `max_prefix`, `max_suffix`, and `total_sum` for its range. This allows us to query the max subarray sum of any arbitrary range $[L, R]$ in $O(\log N)$ time.
    *   Group indices by value to quickly find all occurrences of each $x$.
    *   For each unique $x$, identify the segments formed by removing $x$ (prefix before first $x$, suffix after last $x$, and gaps between consecutive $x$'s).
    *   Query the Segment Tree for each segment and take the maximum.
    *   **Complexity:** $O(N \log N)$ to build and query. This fits the time limits.

2.  **Two-Pass Prefix/Suffix Arrays (Optimization):**
    *   While a full segment tree is robust, we can optimize. We only need the max subarray sum of segments defined by removing $x$.
    *   However, the segments are arbitrary subarrays, not just prefixes/suffixes. A simple prefix/suffix array `pref_max[i]` (max subarray in `nums[0...i]`) doesn't directly give the max subarray of `nums[i...j]`.
    *   We could potentially use a sparse table or similar structure, but the Segment Tree approach is standard and sufficiently efficient for $10^5$.

**Pitfalls:**
*   **Empty Segments:** If removing $x$ leaves an empty array (e.g., `nums = [-3]`), that operation is invalid. We must ensure we consider the "do nothing" case (global max) as the baseline.
*   **Negative Numbers:** The max subarray sum could be negative. Initialize answers with $-\infty$.
*   **Segment Tree Implementation:** Correctly handling the merge logic (`max_sub`, `max_pref`, `max_suff`, `total`) is crucial. Padding the tree to a power of 2 size simplifies indexing.
*   **Range Queries:** Ensure the query function handles ranges that are completely outside the current node's range or partially overlapping correctly.

## worker: Implement the Segment Tree class/functions to stor
The solution implements a Segment Tree to efficiently handle range queries for the maximum subarray sum.
1.  **Segment Tree Structure**: Each node stores four values: `total` (sum of the range), `max_pref` (maximum prefix sum), `max_suff` (maximum suffix sum), and `max_sub` (maximum subarray sum within the range). These values allow merging two child nodes to compute the parent's values in $O(1)$.
2.  **Initialization**: The tree is built over an array padded to the nearest power of 2 to simplify indexing. Leaves corresponding to indices $\ge n$ are initialized with `total=0` and `max_*` values set to $-\infty$ to represent empty segments correctly.
3.  **Query Logic**: The `query` function retrieves the merged node statistics for any arbitrary range $[L, R]$. This allows us to find the max subarray sum of any contiguous segment in $O(\log N)$.
4.  **Algorithm**:
    *   We first calculate the global maximum subarray sum (the case where we perform no operation).
    *   We group the indices of each unique number $x$.
    *   For each unique $x$, we identify the contiguous segments formed by removing all occurrences of $x$. These segments are: the prefix before the first $x$, the suffix after the last $x$, and the gaps between consecutive occurrences of $x$.
    *   We query the segment tree for the max subarray sum of each segment and update the global answer.
5.  **Complexity**:
    *   Building the tree: $O(N)$.
    *   Grouping indices: $O(N)$.
    *   Processing each unique element: In the worst case, there are $N$ unique elements. For each, we perform a constant number of range queries (at most $N$ queries total across all unique elements if we consider the sum of occurrences, but practically bounded by $O(N \log N)$ or $O(U \log N)$ where $U$ is unique count). The total time complexity is $O(N \log N)$.
    *   Space Complexity: $O(N)$ for the tree and index map.

## worker: Verify edge cases and finalize the solution code, 
1.  **Edge Case: Empty Array After Removal**: The problem states "nums remains non-empty". If removing a specific $x$ results in an empty array (e.g., `nums = [-3]` and we remove `-3`), that specific operation is invalid. However, the problem allows performing the operation "at most once". This implies we can choose *not* to perform the operation. My solution initializes `ans` with the global maximum subarray sum (the result of doing nothing), so if all removal operations lead to empty arrays or worse sums, the initial `ans` remains the correct answer.
2.  **Edge Case: All Negative Numbers**: The logic handles negative numbers correctly. `NEG_INF` is set to a sufficiently small value. The segment tree merge logic correctly computes max subarray sums even if all numbers are negative (it will pick the single largest element, i.e., the least negative one).
3.  **Segment Tree Padding**: The tree size is padded to the nearest power of 2. Leaves beyond `n-1` are initialized with `total=0` and `max_* = NEG_INF`. This ensures that queries covering these padded regions correctly return `NEG_INF` for max subarray sums, effectively ignoring them.
4.  **Complexity**:
    *   Building the tree: $O(N)$.
    *   Grouping indices: $O(N)$.
    *   Iterating unique elements: In the worst case ($N$ unique elements), we perform a constant number of range queries per unique element. Specifically, for an element with $k$ occurrences, we do $k+1$ queries. The sum of occurrences over all unique elements is exactly $N$. Thus, the total number of queries is $O(N)$. Each query takes $O(\log N)$. Total time complexity is $O(N \log N)$.
    *   Space complexity: $O(N)$ for the tree and the map.

## worker: Run the code against the provided examples and edg
The solution uses a Segment Tree to efficiently query the maximum subarray sum for any arbitrary contiguous range in $O(\log N)$ time.
1.  **Segment Tree Construction**: The tree is built over the array `nums`, padded to the nearest power of 2. Each node stores `total`, `max_pref`, `max_suff`, and `max_sub`. Padding elements (indices $\ge n$) are initialized with `total=0` and `max_*` values set to $-\infty$ to correctly represent empty ranges.
2.  **Query Logic**: The `query` function recursively finds the node covering the range $[L, R]$ and merges the results from overlapping children. The merge logic correctly computes the new `max_sub` by considering the max subarray in the left child, the right child, or a subarray crossing the boundary (left suffix + right prefix).
3.  **Algorithm**:
    *   We first compute the global maximum subarray sum (the case where we perform no operation).
    *   We group the indices of each unique number $x$.
    *   For each unique $x$, we identify the contiguous segments formed by removing all occurrences of $x$. These segments are: the prefix before the first $x$, the suffix after the last $x$, and the gaps between consecutive occurrences of $x$.
    *   We query the segment tree for the max subarray sum of each segment and update the global answer.
4.  **Complexity**:
    *   Building the tree: $O(N)$.
    *   Grouping indices: $O(N)$.
    *   Processing each unique element: In the worst case ($N$ unique elements), we perform a constant number of range queries per unique element. Specifically, for an element with $k$ occurrences, we do $k+1$ queries. The sum of occurrences over all unique elements is exactly $N$. Thus, the total number of queries is $O(N)$. Each query takes $O(\log N)$. Total time complexity is $O(N \log N)$.
    *   Space complexity: $O(N)$ for the tree and the map.
5.  **Edge Cases**:
    *   **Empty Array After Removal**: The problem states "nums remains non-empty". If removing a specific $x$ results in an empty array (e.g., `nums = [-3]` and we remove `-3`), that specific operation is invalid. However, the problem allows performing the operation "at most once". This implies we can choose *not* to perform the operation. My solution initializes `ans` with the global maximum subarray sum (the result of doing nothing), so if all removal operations lead to empty arrays or worse sums, the initial `ans` remains the correct answer.
    *   **All Negative Numbers**: The logic handles negative numbers correctly. `NEG_INF` is set to a sufficiently small value. The segment tree merge logic correctly computes max subarray sums even if all numbers are negative (it will pick the single largest element, i.e., the least negative one).
    *   **Segment Tree Padding**: The tree size is padded to the nearest power of 2. Leaves beyond `n-1` are initialized with `total=0` and `max_* = NEG_INF`. This ensures that queries covering these padded regions correctly return `NEG_INF` for max subarray sums, effectively ignoring them.
    *   **Complexity**:
        *   Building the tree: $O(N)$.
        *   Grouping indices: $O(N)$.
        *   Iterating unique elements: In the worst case ($N$ unique elements), we perform a constant number of range queries per unique element. Specifically, for an element with $k$ occurrences, we do $k+1$ queries. The sum of occurrences over all unique elements is exactly $N$. Thus, the total number of queries is $O(N)$. Each query takes $O(\log N)$. Total time complexity is $O(N \log N)$.
        *   Space complexity: $O(N)$ for the tree and the map.

## worker: Run the code against the provided examples (Exampl
The solution implements a Segment Tree to efficiently handle range queries for the maximum subarray sum.
1.  **Segment Tree Structure**: Each node stores four values: `total` (sum of the range), `max_pref` (maximum prefix sum), `max_suff` (maximum suffix sum), and `max_sub` (maximum subarray sum within the range). These values allow merging two child nodes to compute the parent's values in $O(1)$.
2.  **Initialization**: The tree is built over an array padded to the nearest power of 2 to simplify indexing. Leaves corresponding to indices $\ge n$ are initialized with `total=0` and `max_*` values set to $-\infty$ to represent empty segments correctly.
3.  **Query Logic**: The `query` function retrieves the merged node statistics for any arbitrary range $[L, R]$. This allows us to find the max subarray sum of any contiguous segment in $O(\log N)$.
4.  **Algorithm**:
    *   We first calculate the global maximum subarray sum (the case where we perform no operation).
    *   We group the indices of each unique number $x$.
    *   For each unique $x$, we identify the contiguous segments formed by removing all occurrences of $x$. These segments are: the prefix before the first $x$, the suffix after the last $x$, and the gaps between consecutive occurrences of $x$.
    *   We query the segment tree for the max subarray sum of each segment and update the global answer.
5.  **Complexity**:
    *   Building the tree: $O(N)$.
    *   Grouping indices: $O(N)$.
    *   Processing each unique element: In the worst case ($N$ unique elements), we perform a constant number of range queries per unique element. Specifically, for an element with $k$ occurrences, we do $k+1$ queries. The sum of occurrences over all unique elements is exactly $N$. Thus, the total number of queries is $O(N)$. Each query takes $O(\log N)$. Total time complexity is $O(N \log N)$.
    *   Space complexity: $O(N)$ for the tree and the map.

## worker: finalize
The solution uses a Segment Tree to efficiently handle range queries for the maximum subarray sum.
1.  **Segment Tree Structure**: Each node stores four values: `total` (sum of the range), `max_pref` (maximum prefix sum), `max_suff` (maximum suffix sum), and `max_sub` (maximum subarray sum within the range). These values allow merging two child nodes to compute the parent's values in $O(1)$.
2.  **Initialization**: The tree is built over an array padded to the nearest power of 2 to simplify indexing. Leaves corresponding to indices $\ge n$ are initialized with `total=0` and `max_*` values set to $-\infty$ to represent empty segments correctly.
3.  **Query Logic**: The `query` function retrieves the merged node statistics for any arbitrary range $[L, R]$. This allows us to find the max subarray sum of any contiguous segment in $O(\log N)$.
4.  **Algorithm**:
    *   We first calculate the global maximum subarray sum (the case where we perform no operation).
    *   We group the indices of each unique number $x$.
    *   For each unique $x$, we identify the contiguous segments formed by removing all occurrences of $x$. These segments are: the prefix before the first $x$, the suffix after the last $x$, and the gaps between consecutive occurrences of $x$.
    *   We query the segment tree for the max subarray sum of each segment and update the global answer.
5.  **Complexity**:
    *   Building the tree: $O(N)$.
    *   Grouping indices: $O(N)$.
    *   Processing each unique element: In the worst case ($N$ unique elements), we perform a constant number of range queries per unique element. Specifically, for an element with $k$ occurrences, we do $k+1$ queries. The sum of occurrences over all unique elements is exactly $N$. Thus, the total number of queries is $O(N)$. Each query takes $O(\log N)$. Total time complexity is $O(N \log N)$.
    *   Space complexity: $O(N)$ for the tree and the map.
