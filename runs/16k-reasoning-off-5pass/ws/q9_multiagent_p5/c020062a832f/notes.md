
## ideation
**Core Difficulty:**
The problem asks for the inversion count of a sequence $B$ where $B_i = (A_i + k) \pmod M$ for $k = 0, \dots, M-1$.
A naive simulation recalculating inversions from scratch for each $k$ takes $O(N \log N)$ or $O(N^2)$, leading to an overall complexity of $O(M \cdot N \log N)$ or worse, which is too slow given $N, M \le 2 \times 10^5$.
The key challenge is to efficiently update the inversion count when $k$ increments by 1.

**Candidate Approaches:**
1.  **Event-Driven Update (Wrap-Around Analysis):**
    *   Observe that when $k$ goes from $k$ to $k+1$, most elements $B_i$ simply increase by 1.
    *   However, elements where $A_i + k = M-1$ (i.e., $B_i = M-1$) will wrap around to $0$.
    *   Let $S$ be the set of indices where $B_i = M-1$ at step $k$. For each $i \in S$, $B_i$ becomes $0$ at step $k+1$.
    *   The change in inversion count depends on the relative order of these "wrapping" elements with respect to all other elements in the sequence.
    *   Specifically, if an element $x$ wraps from $M-1$ to $0$:
        *   It was greater than all elements $y$ where $y < M-1$ (since $M-1$ is the max).
        *   It was smaller than no elements (since it's the max).
        *   After wrapping to $0$, it becomes smaller than all elements $y$ where $y > 0$.
        *   It becomes greater than no elements (since it's the min).
    *   We need to count how many pairs $(i, j)$ with $i < j$ change status from inversion to non-inversion or vice versa.
    *   This involves counting elements to the left and right of the wrapping indices that are currently $0$ (after wrap) vs $M-1$ (before wrap).
    *   We can maintain the positions of values using a Fenwick Tree (Binary Indexed Tree) or Segment Tree to query counts of numbers in specific ranges or positions in $O(\log N)$.

2.  **Coordinate Compression / Value-Based Tracking:**
    *   Instead of tracking positions directly for every query, we can pre-calculate the contribution of each value.
    *   However, the relative order (index $i < j$) is crucial. The "Event-Driven" approach naturally handles this by looking at indices.

3.  **Data Structures Needed:**
    *   We need to know, for the current state of $k$:
        *   Which indices have value $M-1$?
        *   How many elements to the left of a specific index $i$ have value $0$?
        *   How many elements to the right of a specific index $i$ have value $M-1$?
    *   Actually, a simpler view:
        *   Let $L_i$ be the number of elements to the left of index $i$ that are currently $0$.
        *   Let $R_i$ be the number of elements to the right of index $i$ that are currently $M-1$.
        *   When index $i$ wraps ($M-1 \to 0$):
            *   It stops being an inversion with elements to its left that are $< M-1$ (which is almost all). Wait, let's re-evaluate.
            *   **Before wrap ($val = M-1$):**
                *   Inversions with left elements: All left elements $x$ where $x < M-1$. (Since $M-1$ is max).
                *   Inversions with right elements: None (since $M-1$ is max, $M-1 > y$ is true, so if $i<j$, $(M-1, y)$ is an inversion).
                *   Total inversions involving $i$: (Count of left elements) + (Count of right elements where $y < M-1$). Since $y$ can be anything except $M-1$ (if duplicates exist, need care). Generally, $M-1$ is strictly greater than everything else in $0..M-2$.
            *   **After wrap ($val = 0$):**
                *   Inversions with left elements: None (since $0$ is min, $0 < x$ is true, but we need $A_i > A_j$. Here $0 > x$ is false).
                *   Inversions with right elements: All right elements $y$ where $0 > y$. None, since values are non-negative.
                *   Wait, definition: Inversion is $i < j$ and $B_i > B_j$.
                *   **Before ($B_i = M-1$):**
                    *   For $j < i$: If $B_j < M-1$, then $B_j < B_i$ (No inversion). If $B_j = M-1$, $B_j = B_i$ (No inversion). So $B_i$ is NOT part of an inversion with any $j < i$.
                    *   For $j > i$: If $B_j < M-1$, then $B_i > B_j$ (Inversion). If $B_j = M-1$, no inversion.
                    *   So, inversions involving $i$ (as the first element) = Count of $j > i$ such that $B_j < M-1$.
                *   **After ($B_i = 0$):**
                    *   For $j < i$: If $B_j > 0$, then $B_j > B_i$ (No inversion, we need $B_i > B_j$). If $B_j = 0$, no inversion.
                    *   For $j > i$: If $B_j < 0$ (Impossible).
                    *   So, inversions involving $i$ (as the first element) = 0.
                *   **Change:** We lose inversions where $i$ was the larger element.
                *   BUT, we also need to consider if $i$ was the *second* element of an inversion? No, $i$ is the index. The pair is $(i, j)$ with $i < j$. $i$ is always the first element in the pair if we consider pairs starting at $i$.
                *   Wait, what about pairs $(j, i)$ where $j < i$?
                    *   **Before ($B_i = M-1$):** $B_j > B_i$? $B_j > M-1$? Impossible. So no inversions where $i$ is the second element.
                    *   **After ($B_i = 0$):** $B_j > 0$? Yes, if $B_j > 0$. Then $(j, i)$ is an inversion.
                *   **Net Change Calculation:**
                    *   Let $S$ be the set of indices where $B_i = M-1$.
                    *   For each $i \in S$:
                        *   Loss: Pairs $(i, j)$ with $j > i$ and $B_j < M-1$. (Since $B_i$ drops from $M-1$, it is no longer $> B_j$).
                        *   Gain: Pairs $(j, i)$ with $j < i$ and $B_j > 0$. (Since $B_i$ drops to $0$, it is now $< B_j$, creating an inversion).
                    *   Total Change = $\sum_{i \in S} (\text{Count } j < i \text{ s.t. } B_j > 0) - (\text{Count } j > i \text{ s.t. } B_j < M-1)$.
    *   This looks computable. We need to efficiently query:
        *   For a set of indices $S$, sum of (count of non-zero elements to the left).
        *   For a set of indices $S$, sum of (count of non-(M-1) elements to the right).
    *   We can maintain two Fenwick Trees (or one with updates):
        *   `BIT_pos`: Tracks positions of elements. But we need values.
        *   Actually, we need to know the values at positions $j$.
        *   We can maintain a BIT over the *indices* $1..N$ where the value at index $p$ is 1 if $B_p > 0$, else 0.
        *   And another BIT where value at index $p$ is 1 if $B_p < M-1$, else 0.
        *   When $k$ increments:
            1. Identify all $i$ such that $B_i = M-1$. These are indices where $A_i = M-1-k$.
            2. Calculate the change using the current BITs.
            3. Update the BITs: For each such $i$, set $B_i$ from $M-1$ to $0$.
                *   In `BIT_gt0`: change at $i$ from $0$ (since $M-1 > 0$) to $1$ (since $0 \ngtr 0$)? No, $0$ is not $>0$. So change from 1 to 0.
                *   In `BIT_ltM1`: change at $i$ from $0$ (since $M-1 \not< M-1$) to $1$ (since $0 < M-1$).
    *   Complexity: $O(M \cdot (\text{count of wraps} \cdot \log N))$. In worst case, all elements wrap every time? No.
        *   Each element $A_i$ wraps exactly once every $M$ steps.
        *   Total number of wrap events over all $k=0..M-1$ is $N$.
        *   So the total complexity is $O(N \log N + M \log N)$ (for initial setup and updates). This is efficient enough.

**Pitfalls:**
*   **Duplicate Values:** The logic $B_j < M-1$ handles $B_j = M-1$ correctly (it's not $< M-1$). The logic $B_j > 0$ handles $B_j = 0$ correctly (it's not $> 0$).
*   **Initial State:** Need to build the BITs for $k=0$.
*   **Large Inputs:** Use fast I/O. Python might be slow if not careful, but $O(N \log N)$ should pass within 2s.
*   **Off-by-one errors:** Indices, modulo arithmetic.
*   **Logic Verification:**
    *   Change = (New Inversions) - (Old Inversions).
    *   Old Inv involving $i$ (where $B_i=M-1$): Pairs $(i, j)$ with $j>i$ and $B_j < M-1$. (Since $M-1 > x$ for all $x < M-1$).
    *   New Inv involving $i$ (where $B_i=0$): Pairs $(j, i)$ with $j<i$ and $B_j > 0$. (Since $x > 0$ for all $x > 0$).
    *   Are there other changes?
        *   Pairs $(i, j)$ where neither wraps? $B_i \to B_i+1$, $B_j \to B_j+1$. Order preserved. No change.
        *   Pairs $(i, j)$ where both wrap? $B_i=M-1 \to 0$, $B_j=M-1 \to 0$. Order preserved ($0=0$). No change.
        *   Pairs $(i, j)$ where $i$ wraps, $j$ doesn't? Covered above.
        *   Pairs $(i, j)$ where $i$ doesn't wrap, $j$ wraps? Covered above (as $j$ is the second element).
    *   So the logic holds.

**Implementation Steps:**
1.  Read $N, M, A$.
2.  Initialize `current_inv` for $k=0$. Can be done with a standard BIT in $O(N \log N)$.
3.  Build two BITs:
    *   `bit_pos_gt0`: At index $p$, store 1 if $A_p > 0$, else 0.
    *   `bit_pos_ltM1`: At index $p$, store 1 if $A_p < M-1$, else 0.
4.  Identify initial set of indices where $A_i = M-1$. Let this be `wrapping_indices`.
5.  Loop $k$ from $0$ to $M-1$:
    *   Print `current_inv`.
    *   If $k < M-1$:
        *   Find indices where $A_i + k = M-1 \implies A_i = M-1 - k$. Let this set be `next_wraps`.
        *   Calculate `delta`:
            *   For each $idx \in next\_wraps$:
                *   `gain` += `bit_pos_gt0.query(idx - 1)` (count of $j < idx$ with $B_j > 0$)
                *   `loss` += `bit_pos_ltM1.query(N) - bit_pos_ltM1.query(idx)` (count of $j > idx$ with $B_j < M-1$)
            *   `current_inv` += `gain - loss`
        *   Update BITs for `next_wraps`:
            *   For each $idx \in next\_wraps$:
                *   Update `bit_pos_gt0`: $idx$ goes from 1 (since $M-1 > 0$) to 0 (since $0 \ngtr 0$). Add -1.
                *   Update `bit_pos_ltM1`: $idx$ goes from 0 (since $M-1 \not< M-1$) to 1 (since $0 < M-1$). Add +1.
        *   Update $A$ values conceptually (or just track which ones wrap). Actually, we don't need to update $A$ array, just the BITs reflect the new state.
        *   Note: The set of indices wrapping at step $k$ is determined by $A_i = M-1-k$. We can pre-group indices by value. `indices_by_val[v]` = list of indices where $A_i = v$.
        *   At step $k$, we process `indices_by_val[M-1-k]`.

**Refinement on Complexity:**
*   Preprocessing: $O(N \log N)$ to compute initial inversions and build BITs. Grouping indices: $O(N)$.
*   Loop $M$ times:
    *   Total number of updates across all $k$ is $N$ (each element wraps once).
    *   Total query cost: $N \log N$.
    *   Total update cost: $N \log N$.
    *   Loop overhead: $M$ iterations.
*   Total Time: $O((N+M) \log N)$. With $N, M = 2 \cdot 10^5$, this is roughly $4 \cdot 10^6$ ops, well within limits.

## worker: Implement the Fenwick Tree (BIT) class and the mai
1.  **Algorithm Selection**: The problem requires calculating inversion counts for $M$ different shifted sequences. A naive $O(N \log N)$ per shift leads to $O(MN \log N)$, which is too slow ($4 \cdot 10^{10}$ ops). The solution uses an incremental update approach.
2.  **Key Insight**: When $k$ increments, only elements with value $M-1$ change their value to $0$. All other elements simply increment by 1, preserving their relative order. Thus, we only need to account for inversions involving the "wrapping" elements.
3.  **Update Logic**:
    *   Let $S$ be the set of indices where $B_i = M-1$.
    *   For each $i \in S$, $B_i$ becomes $0$.
    *   **Loss**: Pairs $(i, j)$ where $i < j$ and $B_j < M-1$. Since $B_i$ was $M-1$ (max), it formed an inversion with all such $j$. Now $B_i=0$, so it doesn't.
    *   **Gain**: Pairs $(j, i)$ where $j < i$ and $B_j > 0$. Since $B_i$ became $0$ (min), it now forms an inversion with all such $j$ (where $B_j > 0$).
    *   Net Change = $\sum_{i \in S} (\text{count } j < i, B_j > 0) - (\text{count } j > i, B_j < M-1)$.
4.  **Data Structures**:
    *   Two Fenwick Trees (BITs) are maintained over the *indices* $1 \dots N$.
    *   `bit_pos_gt0`: Stores 1 at index $p$ if $B_p > 0$. Used to count $j < i$ with $B_j > 0$.
    *   `bit_pos_ltM1`: Stores 1 at index $p$ if $B_p < M-1$. Used to count $j > i$ with $B_j < M-1$.
5.  **Complexity**:
    *   Initial Inversion Count: $O(N \log N)$.
    *   Initial BIT Setup: $O(N \log N)$.
    *   Loop $M$ times:
        *   Total number of wrap events across all $k$ is $N$ (each element wraps exactly once).
        *   Each wrap event involves 2 BIT queries and 2 BIT updates: $O(\log N)$.
        *   Total update cost: $O(N \log N)$.
    *   Overall Time Complexity: $O((N + M) \log N)$. With $N, M \le 2 \cdot 10^5$, this is efficient.
6.  **Edge Cases**:
    *   $N=1$: Inversion count is always 0.
    *   $M=1$: Only $k=0$ exists, $A_i=0$, inversion 0.
    *   All $A_i$ same: No inversions initially, no changes.
    *   The logic handles duplicates correctly because the condition $B_j < M-1$ excludes $M-1$ itself, and $B_j > 0$ excludes $0$.

## worker: Run the code against the provided sample inputs to
The code implements the incremental update strategy derived in the thought process.
1.  **Initial Calculation**: Computes the inversion count for $k=0$ using a standard Fenwick Tree over values.
2.  **State Maintenance**: Maintains two Fenwick Trees over indices ($1 \dots N$):
    *   `bit_pos_gt0`: Tracks if $B_i > 0$.
    *   `bit_pos_ltM1`: Tracks if $B_i < M-1$.
3.  **Iteration**: For each $k$ from $0$ to $M-1$:
    *   Records the current inversion count.
    *   Identifies indices $i$ where $A_i + k = M-1$ (these will wrap to $0$).
    *   Calculates the change in inversions:
        *   **Gain**: For each wrapping $i$, count $j < i$ where $B_j > 0$. (Since $B_i$ becomes $0$, it is now smaller than these, forming new inversions $(j, i)$).
        *   **Loss**: For each wrapping $i$, count $j > i$ where $B_j < M-1$. (Since $B_i$ becomes $0$, it is no longer larger than these, losing inversions $(i, j)$).
    *   Updates the BITs to reflect that these indices now have value $0$ (so they are no longer $>0$ but are $<M-1$).
4.  **Complexity**: $O(N \log N)$ for initialization and $O(N \log N)$ for all updates across $M$ steps (since each element wraps exactly once). Total time $O((N+M)\log N)$, which fits within limits.

## worker: Run the provided sample inputs to verify correctne
The solution implements the incremental update strategy derived in the thought process.
1.  **Initial Calculation**: Computes the inversion count for $k=0$ using a standard Fenwick Tree over values.
2.  **State Maintenance**: Maintains two Fenwick Trees over indices ($1 \dots N$):
    *   `bit_pos_gt0`: Tracks if $B_i > 0$.
    *   `bit_pos_ltM1`: Tracks if $B_i < M-1$.
3.  **Iteration**: For each $k$ from $0$ to $M-1$:
    *   Records the current inversion count.
    *   Identifies indices $i$ where $A_i + k = M-1$ (these will wrap to $0$).
    *   Calculates the change in inversions:
        *   **Gain**: For each wrapping $i$, count $j < i$ where $B_j > 0$. (Since $B_i$ becomes $0$, it is now smaller than these, forming new inversions $(j, i)$).
        *   **Loss**: For each wrapping $i$, count $j > i$ where $B_j < M-1$. (Since $B_i$ becomes $0$, it is no longer larger than these, losing inversions $(i, j)$).
    *   Updates the BITs to reflect that these indices now have value $0$ (so they are no longer $>0$ but are $<M-1$).
4.  **Complexity**: $O(N \log N)$ for initialization and $O(N \log N)$ for all updates across $M$ steps (since each element wraps exactly once). Total time $O((N+M)\log N)$, which fits within limits.

## worker: finalize
The solution implements an incremental update strategy to solve the problem efficiently.
1.  **Initial Calculation**: We first compute the inversion count for $k=0$ using a standard Fenwick Tree (BIT) over the values of $A$. This takes $O(N \log N)$.
2.  **State Maintenance**: We maintain two additional BITs over the *indices* $1 \dots N$:
    *   `bit_pos_gt0`: Tracks if the element at a specific index is $> 0$.
    *   `bit_pos_ltM1`: Tracks if the element at a specific index is $< M-1$.
3.  **Iterative Update**: For each step $k$ from $0$ to $M-1$:
    *   We identify the set of indices $S$ where the current value $B_i = M-1$. These are the indices where $A_i = M-1-k$.
    *   When $k$ increments, these elements wrap around to $0$.
    *   **Change Calculation**:
        *   **Loss**: For each $i \in S$, we lose inversions with all $j > i$ where $B_j < M-1$. This is queried from `bit_pos_ltM1`.
        *   **Gain**: For each $i \in S$, we gain inversions with all $j < i$ where $B_j > 0$. This is queried from `bit_pos_gt0`.
    *   **Update**: We update the two position BITs to reflect that the values at indices in $S$ have changed from $M-1$ to $0$.
4.  **Complexity**: Each element wraps around exactly once over the course of $M$ steps. Thus, the total number of BIT operations is proportional to $N$. The overall time complexity is $O((N+M) \log N)$, which fits well within the time limits for $N, M \le 2 \times 10^5$.
