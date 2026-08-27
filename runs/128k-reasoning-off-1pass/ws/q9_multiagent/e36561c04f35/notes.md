
## ideation
**Core Difficulty:**
The problem requires minimizing operations to empty an array using two moves: swapping adjacent elements and deleting a prefix of identical values. The key challenge is determining the optimal sequence of swaps and deletions to maximize the efficiency of deletions (i.e., deleting as many elements as possible in a single operation).

**Candidate Approaches:**
1.  **Greedy Simulation:**
    -   Always check if the current head of the array can form a block of identical values.
    -   If a block of size $\ge 2$ exists at the start, delete it.
    -   If not, check if swapping the head with the next occurrence of the same value creates a block of size 2. If so, swap and then delete.
    -   If neither is possible, delete the head individually.
    -   This approach seems to align with the sample cases (e.g., Sample 3 where alternating deletions are inefficient, but grouping pairs helps).

2.  **Optimization:**
    -   A naive simulation with list slicing or `pop(0)` is $O(N^2)$, which might TLE for $N=2 \times 10^5$.
    -   However, the constraints and problem type suggest that the number of operations is relatively small or the test cases are structured such that the simulation is efficient.
    -   Alternatively, the answer might be derived from counting runs or inversions, but the greedy simulation is the most direct way to model the process described.

**Pitfalls:**
-   **Inefficiency:** Repeatedly scanning the array to find the next occurrence of a value can be slow.
-   **Optimality:** The greedy choice of swapping to form a block of 2 might not always be globally optimal if a larger block could be formed with fewer total operations, but given the operation costs (1 swap vs 1 delete), forming a block of 2 is usually the threshold for saving operations.
-   **Sample 3 Analysis:** The sample output 8 for `1 2 1 2 1 2 1 2 1 2 1` (6 ones, 5 twos) suggests that grouping pairs (1,2) into (1,1,2,2) blocks is beneficial. The simulation should capture this by swapping adjacent different elements if it leads to a block.

## worker: Implement the greedy simulation logic: iterate thr
The problem requires minimizing operations to empty the array. The strategy is to greedily form blocks of identical values at the start and delete them.
1.  **State**: We maintain the current array implicitly using original indices and a data structure to track which elements are present.
2.  **Finding Next Occurrence**: For the current head value `v`, we find the nearest occurrence of `v` after the head. This determines if we can form a block of size >= 2.
3.  **Swaps**: If the nearest `v` is at rank `r_next` and head is at rank `r_head`, the number of swaps needed to bring it to position 1 is `(r_next - r_head - 1)`.
4.  **Block Length**: After swapping (conceptually), we count how many consecutive `v`s are at the start. This is done by checking the next present elements.
5.  **Deletion**: We delete the block (cost 1) and update the state.
6.  **Efficiency**: We use a Fenwick tree (Binary Indexed Tree) to efficiently find the rank of an index (number of present elements <= index) and to skip deleted elements. We also maintain pointers for each value to quickly find the next occurrence.

## worker: Implement the full solution code based on the gree
The solution implements a greedy strategy using a Fenwick Tree (Binary Indexed Tree) to efficiently manage the array state and find elements.
1.  **Data Structures**:
    *   `pos`: Dictionary mapping each value to a sorted list of its original indices.
    *   `ptr`: Dictionary tracking the current position in `pos` for each value to avoid re-scanning.
    *   `FenwickTree`: Maintains the presence of elements (1 if present, 0 if deleted) to allow efficient rank queries (finding the k-th present element) and updates.
2.  **Algorithm**:
    *   Iterate while the array is not empty.
    *   Identify the current head element (original index `head_idx`).
    *   Find the nearest occurrence of the same value (`next_occ_idx`) that is still present.
    *   **Case 1 (Match found)**:
        *   Calculate the number of swaps required to bring `next_occ_idx` to the position immediately following `head_idx`. This is `(rank(next_occ_idx) - rank(head_idx) - 1)`.
        *   Count the length of the contiguous block of identical values starting from `head_idx` (including `next_occ_idx` and any subsequent identical values).
        *   Add `swaps + 1` to the total operations.
        *   Remove all elements in the block from the Fenwick Tree.
        *   Update `head_idx` to the next present element.
    *   **Case 2 (No match)**:
        *   Delete the single head element (1 operation).
        *   Update `head_idx` to the next present element.
3.  **Complexity**:
    *   Finding the next occurrence and counting the block involves binary search on the Fenwick Tree, taking $O(\log N)$.
    *   Each element is deleted exactly once.
    *   Total time complexity is $O(N \log N)$ per test case, which fits within the limits.

## worker: finalize
The solution implements a greedy strategy using a Fenwick Tree (Binary Indexed Tree) to efficiently manage the array state.
1.  **State Management**: The Fenwick Tree tracks which elements are present (1) or deleted (0).
2.  **Finding Elements**:
    *   `find_kth(k)`: Finds the original index of the element with rank `k` (i.e., the $k$-th present element). This is done in $O(\log N)$ using binary lifting on the BIT.
    *   `query(i)`: Returns the number of present elements with original index $\le i$.
3.  **Greedy Logic**:
    *   Identify the current head element (rank 1).
    *   Find the nearest occurrence of the same value after the head.
    *   **If found**:
        *   Calculate the number of swaps required to bring this occurrence to the position immediately following the head. This is `(rank(next) - rank(head) - 1)`.
        *   Count the length of the contiguous block of identical values starting from the head. This involves checking subsequent present elements until a different value is found.
        *   Add `swaps + 1` to the total operations.
        *   Delete all elements in the block from the BIT.
        *   Update the current head rank to `block_len + 1`.
    *   **If not found**:
        *   Delete the single head element (1 operation).
        *   Update the current head rank to `current_head_rank + 1`.
4.  **Complexity**: Each element is deleted exactly once. Finding the next occurrence and counting the block takes $O(\log N)$ per step. Total time complexity is $O(N \log N)$ per test case, which fits within the limits ($N \le 2 \times 10^5$).
