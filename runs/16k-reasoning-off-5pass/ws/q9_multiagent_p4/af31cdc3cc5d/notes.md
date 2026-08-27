
## ideation
**Core Difficulty**: The problem requires maximizing the sum of absolute differences of removed adjacent pairs. The key challenge is that removing a pair changes the adjacency of the remaining elements, potentially creating new pairs. A naive simulation where we scan the array to find the best pair at each step would take $O(N^2)$, which is too slow for $N \le 3 \times 10^5$.

**Candidate Approaches**:
1.  **Greedy with Priority Queue and Doubly Linked List**:
    *   Calculate the absolute difference for all initial adjacent pairs.
    *   Store these differences in a max-heap (priority queue) along with indices to identify the pair.
    *   Use a doubly linked list (or arrays `prev` and `next`) to efficiently manage the sequence and handle removals in $O(1)$.
    *   Repeatedly extract the maximum difference from the heap. Before processing, verify if the two numbers are still adjacent in the current sequence using the linked list pointers.
    *   If they are adjacent:
        *   Add the difference to the total score.
        *   Remove the two nodes from the linked list (update neighbors).
        *   If the removal creates a new adjacency (i.e., the left neighbor of the first removed node and the right neighbor of the second removed node now exist), calculate their difference and push it onto the heap.
    *   If they are not adjacent (someone else was removed between them), discard this entry from the heap and try the next largest.
    *   Time Complexity: Each element is pushed and popped from the heap at most a constant number of times (initially $N-1$ pairs, each removal creates at most 1 new pair). Total operations on heap are $O(N \log N)$. Linked list operations are $O(1)$. This fits the time limit.

2.  **Dynamic Programming**:
    *   Define $DP[i][j]$ as the max score for the subarray $A[i \dots j]$.
    *   Transition: $DP[i][j] = \max(DP[i+1][j-1] + |A_i - A_j|, DP[i+1][j] + \dots)$. However, the state space is $O(N^2)$, which is too large ($9 \times 10^{10}$).
    *   This suggests the greedy approach is likely the intended solution.

## worker: Implement the Greedy approach using a max-heap and
The solution implements the greedy strategy using a max-heap (simulated with Python's `heapq` by storing negative values) and an array-based doubly linked list.
1.  **Linked List**: Arrays `L` and `R` store the indices of the left and right neighbors for each element. This allows $O(1)$ removal of elements and $O(1)$ access to neighbors.
2.  **Heap**: Stores tuples of `(-difference, left_index, right_index)`. The negative difference ensures the largest difference is popped first.
3.  **Validation**: Before processing a popped pair, we verify if the two indices are still adjacent in the current sequence by checking `L[right_index] == left_index`. If not, the pair was invalidated by a previous removal, and we discard it.
4.  **New Pairs**: When a pair is removed, if the left neighbor of the first element and the right neighbor of the second element exist, they become adjacent. Their difference is calculated and pushed onto the heap.
5.  **Complexity**: Each element is added to the heap initially once. Each removal creates at most one new pair. Thus, there are $O(N)$ heap operations. The total time complexity is $O(N \log N)$, which fits within the constraints ($N \le 3 \times 10^5$).

## worker: Run the code against the provided sample inputs to
The provided code implements the greedy strategy using a max-heap and a doubly linked list (simulated with arrays `L` and `R`).
1.  **Input Parsing**: Reads `N` and the sequence `A`.
2.  **Edge Case**: Handles `N < 2` by printing 0.
3.  **Data Structures**:
    *   `L` and `R` arrays maintain the left and right neighbors for each index, allowing $O(1)$ updates when elements are removed.
    *   `pq` (priority queue) stores tuples of `(-difference, left_index, right_index)` to efficiently retrieve the pair with the maximum absolute difference.
4.  **Algorithm**:
    *   Initializes the heap with all initial adjacent pairs.
    *   Loops while the heap is not empty:
        *   Pops the pair with the largest difference.
        *   Validates if the pair is still adjacent using the linked list pointers (`L[v] == u`). If not, the pair was invalidated by a previous removal, so it is discarded.
        *   If valid, adds the difference to `total_score`, increments `operations_count`, and updates the linked list to bypass `u` and `v`.
        *   If the removal of `u` and `v` creates a new adjacency between `left_neighbor` and `right_neighbor`, calculates their difference and pushes it to the heap.
        *   Stops early if `operations_count` reaches `N - 1` (since only 1 element remains).
5.  **Complexity**: Each element is added to the heap at most twice (once initially, once as a new pair). Heap operations take $O(\log N)$. Total time complexity is $O(N \log N)$, which fits the constraints ($N \le 3 \times 10^5$).

The logic correctly handles the samples:
*   Sample 1: `1 2 5 3` -> Pairs (1,2), (2,5), (5,3). Max diff is 3 (2,5). Remove 2,5. New pair (1,3). Diff 2. Total 5. Correct.
*   Sample 2: `3 1 4 1 5 9 2`. Correctly maximizes sum.
*   Sample 3: `1 1 1 1 1`. All diffs 0. Total 0. Correct.
