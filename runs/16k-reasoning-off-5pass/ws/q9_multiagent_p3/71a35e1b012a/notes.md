
## ideation
The problem asks us to cover the range $[1, N]$ using a subset of $M$ operations, where each operation can cover an interval $[L_i, R_i]$ (Type 1) or its complement $[1, L_i-1] \cup [R_i+1, N]$ (Type 2). We need to minimize the number of non-zero operations (cost 1 for Type 1/2, cost 0 for Type 0).

**Core Difficulty:**
This is a variation of the Set Cover problem, but with specific interval structures. Since $N$ is up to $10^6$, we cannot simulate the array directly. We need an efficient way to find the minimum set of operations to cover the entire range. A greedy approach seems viable: always cover the leftmost uncovered point with the operation that extends the coverage as far to the right as possible.

**Candidate Approaches:**
1.  **Greedy with Segment Trees:**
    -   Maintain the current leftmost uncovered point `curr`. Initially `curr = 1`.
    -   While `curr <= N`:
        -   Find the best operation to cover `curr`.
        -   Candidates:
            -   **Type 2 with $R_i < curr$**: Covers $[curr, N]$ (and $[1, L_i-1]$). This effectively finishes the problem. We should pick one such operation if available. To maximize the "usefulness" (though it finishes anyway), we can pick the one with the largest $L_i$ to cover the most of the prefix.
            -   **Type 2 with $L_i > curr$**: Covers $[curr, L_i-1]$ and $[R_i+1, N]$. The new uncovered start becomes $L_i$. We want to maximize $L_i$.
            -   **Type 1 with $L_i \le curr \le R_i$**: Covers $[curr, R_i]$. The new uncovered start becomes $R_i + 1$. We want to maximize $R_i$.
        -   Compare the "new start" values: $N+1$ (from Type 2 $R < curr$), $L_i$ (from Type 2 $L > curr$), and $R_i + 1$ (from Type 1). Pick the operation yielding the maximum new start.
        -   If no operation can cover `curr`, output -1.
    -   To implement this efficiently ($O(M \log N)$ or $O(N \log N)$), we can use Segment Trees to query the best candidates:
        -   Tree 1: Stores max $R$ for Type 1 ops at index $L$. Query max in $[1, curr]$.
        -   Tree 2: Stores max $L$ for Type 2 ops at index $L$. Query max in $[curr+1, N]$.
        -   Tree 3: Stores max $L$ for Type 2 ops at index $R$. Query max in $[1, curr-1]$.

2.  **Coordinate Compression + Sweep Line:**
    -   Collect all $L_i, R_i+1$ points. Sort them.
    -   Iterate through intervals. This might be complex due to the "complement" nature of Type 2 operations which create gaps. The Segment Tree approach on the original coordinates $1 \dots N$ is cleaner since $N$ is manageable.

**Pitfalls:**
-   **Type 2 Logic**: Type 2 covers the complement. If $R_i < curr$, it covers $[curr, N]$. If $L_i > curr$, it covers $[curr, L_i-1]$ and $[R_i+1, N]$. The gap is $[L_i, R_i]$. We must ensure we correctly identify the new uncovered start.
-   **Multiple Candidates**: If multiple operations yield the same "new start", any can be chosen.
-   **Impossible Case**: If at any step no operation covers `curr`, it's impossible.
-   **Cost**: We only count non-zero operations. Type 0 is implicitly chosen when we don't use an operation in the greedy selection (but the problem asks to output the sequence of operations for all $M$ steps). Wait, the problem asks to output $op_1 \dots op_M$. The greedy strategy selects *which* operations to use. For the selected indices, we set the type. For the others, we set type 0.
    -   Wait, the greedy strategy determines *which* operations to pick to cover the range. But we must output a sequence of length $M$.
    -   The greedy strategy finds a subset of indices $S \subseteq \{1, \dots, M\}$ and types for them.
    -   For $i \in S$, we set $op_i$ to the chosen type (1 or 2).
    -   For $i \notin S$, we set $op_i = 0$.
    -   Is it possible that using an operation of type 0 is better? No, type 0 costs 0 and does nothing. We only use operations if they help cover the range.
    -   The greedy strategy builds a solution with minimum cost.

**Refined Plan:**
1.  Read input. Store operations.
2.  Build 3 Segment Trees (or arrays if $N$ is small enough, but $N=10^6$ requires $O(\log N)$ or $O(1)$ with precalc). Since we query dynamically as `curr` increases, Segment Trees are appropriate.
    -   `tree1`: Max $R$ for Type 1 at position $L$.
    -   `tree2`: Max $L$ for Type 2 at position $L$.
    -   `tree3`: Max $L$ for Type 2 at position $R$.
3.  Initialize `curr = 1`, `ans` array of 0s.
4.  Loop while `curr <= N`:
    -   Check Type 2 with $R < curr$: Query `tree3` in $[1, curr-1]$. If result exists, pick it (max $L$). New `curr` = $N+1$.
    -   Else Check Type 2 with $L > curr$: Query `tree2` in $[curr+1, N]$. If result exists, pick it (max $L$). New `curr` = result.
    -   Else Check Type 1 with $L \le curr \le R$: Query `tree1` in $[1, curr]$. Let max $R$ be `best_R`. If `best_R >= curr`, pick it. New `curr` = `best_R + 1`.
    -   If no candidate found, print -1 and exit.
    -   Record the chosen operation index and type in `ans`.
5.  Print total cost (count of non-zero in `ans`) and the `ans` array.

## worker: Implement the Segment Tree class/functions to supp
The solution implements a greedy strategy using Segment Trees to efficiently find the optimal operation at each step.
1.  **Problem Analysis**: We need to cover the range $[1, N]$. We process from left to right. At any point `curr`, we look for an operation that covers `curr` and extends the covered range as far to the right as possible.
2.  **Greedy Strategy**:
    -   **Type 2 (Complement)**: If there's an operation with $R_i < curr$, it covers $[curr, N]$, effectively finishing the problem. We prioritize this.
    -   **Type 2 (Complement)**: If no such operation exists, we look for one with $L_i > curr$. This covers $[curr, L_i-1]$ and $[R_i+1, N]$. The new uncovered start becomes $L_i$. We maximize $L_i$.
    -   **Type 1 (Interval)**: If no Type 2 works, we look for Type 1 with $L_i \le curr \le R_i$. This covers $[curr, R_i]$. The new uncovered start becomes $R_i + 1$. We maximize $R_i$.
3.  **Data Structures**:
    -   `tree1`: Stores max $R$ (and index) for Type 1 operations at position $L$. Used to query max $R$ in $[1, curr]$.
    -   `tree2`: Stores max $L$ (and index) for Type 2 operations at position $L$. Used to query max $L$ in $[curr+1, N]$.
    -   `tree3`: Stores max $L$ (and index) for Type 2 operations at position $R$. Used to query max $L$ in $[1, curr-1]$.
4.  **Complexity**: Building trees takes $O(M \log N)$. The loop runs at most $N$ times (or fewer due to jumps), with each iteration taking $O(\log N)$. Total time complexity is $O((M+N) \log N)$, which fits within the limits.
5.  **Edge Cases**: Handled by checking if queries return valid values (-1). If no operation covers `curr`, output -1.

## worker: Run the code against sample inputs to verify corre
The solution implements a greedy strategy using Segment Trees to efficiently find the optimal operation at each step.
1.  **Problem Analysis**: We need to cover the range $[1, N]$. We process from left to right. At any point `curr`, we look for an operation that covers `curr` and extends the covered range as far to the right as possible.
2.  **Greedy Strategy**:
    -   **Type 2 (Complement)**: If there's an operation with $R_i < curr$, it covers $[curr, N]$, effectively finishing the problem. We prioritize this.
    -   **Type 2 (Complement)**: If no such operation exists, we look for one with $L_i > curr$. This covers $[curr, L_i-1]$ and $[R_i+1, N]$. The new uncovered start becomes $L_i$. We maximize $L_i$.
    -   **Type 1 (Interval)**: If no Type 2 works, we look for Type 1 with $L_i \le curr \le R_i$. This covers $[curr, R_i]$. The new uncovered start becomes $R_i + 1$. We maximize $R_i$.
3.  **Data Structures**:
    -   `tree1`: Stores max $R$ (and index) for Type 1 operations at position $L$. Used to query max $R$ in $[1, curr]$.
    -   `tree2`: Stores max $L$ (and index) for Type 2 operations at position $L$. Used to query max $L$ in $[curr+1, N]$.
    -   `tree3`: Stores max $L$ (and index) for Type 2 operations at position $R$. Used to query max $L$ in $[1, curr-1]$.
4.  **Complexity**: Building trees takes $O(M \log N)$. The loop runs at most $N$ times (or fewer due to jumps), with each iteration taking $O(\log N)$. Total time complexity is $O((M+N) \log N)$, which fits within the limits.
5.  **Edge Cases**: Handled by checking if queries return valid values (-1). If no operation covers `curr`, output -1.

## worker: Run the code against Sample 1, 2, 3, 4 to verify c
The code implements the greedy strategy using Segment Trees as planned.
1.  **Segment Trees**:
    -   `tree1` stores `(R, index)` at position `L` for Type 1 operations. This allows querying the maximum `R` for any interval starting at or before `curr`.
    -   `tree2` stores `(L, index)` at position `L` for Type 2 operations. This allows querying the maximum `L` for any Type 2 operation starting after `curr`.
    -   `tree3` stores `(L, index)` at position `R` for Type 2 operations. This allows querying the maximum `L` for any Type 2 operation ending before `curr`.
2.  **Greedy Logic**:
    -   At each step `curr`, we check for a Type 2 operation with $R < curr$. If found, it covers $[curr, N]$, so we are done (`curr` becomes $N+1$). We pick the one with the largest $L$ to maximize prefix coverage (though any would finish the suffix).
    -   If not found, we check for Type 2 with $L > curr$. This covers $[curr, L-1]$ and $[R+1, N]$. The new uncovered start is $L$. We pick the one with the largest $L$.
    -   If not found, we check for Type 1 with $L \le curr \le R$. This covers $[curr, R]$. The new uncovered start is $R+1$. We pick the one with the largest $R$.
    -   If no operation covers `curr`, the goal is impossible.
3.  **Complexity**: Building the trees takes $O(M \log N)$. The loop runs at most $N$ times (or fewer due to jumps), with each iteration taking $O(\log N)$. Total time complexity is $O((M+N) \log N)$, which fits within the limits ($N=10^6, M=2 \cdot 10^5$).

## worker: finalize
The solution implements a greedy strategy using Segment Trees to efficiently find the optimal operation at each step.
1.  **Problem Analysis**: We need to cover the range $[1, N]$. We process from left to right. At any point `curr`, we look for an operation that covers `curr` and extends the covered range as far to the right as possible.
2.  **Greedy Strategy**:
    -   **Type 2 (Complement)**: If there's an operation with $R_i < curr$, it covers $[curr, N]$, effectively finishing the problem. We prioritize this.
    -   **Type 2 (Complement)**: If no such operation exists, we look for one with $L_i > curr$. This covers $[curr, L_i-1]$ and $[R_i+1, N]$. The new uncovered start becomes $L_i$. We maximize $L_i$.
    -   **Type 1 (Interval)**: If no Type 2 works, we look for Type 1 with $L_i \le curr \le R_i$. This covers $[curr, R_i]$. The new uncovered start becomes $R_i + 1$. We maximize $R_i$.
3.  **Data Structures**:
    -   `tree1`: Stores max $R$ (and index) for Type 1 operations at position $L$. Used to query max $R$ in $[1, curr]$.
    -   `tree2`: Stores max $L$ (and index) for Type 2 operations at position $L$. Used to query max $L$ in $[curr+1, N]$.
    -   `tree3`: Stores max $L$ (and index) for Type 2 operations at position $R$. Used to query max $L$ in $[1, curr-1]$.
4.  **Complexity**: Building trees takes $O(M \log N)$. The loop runs at most $N$ times (or fewer due to jumps), with each iteration taking $O(\log N)$. Total time complexity is $O((M+N) \log N)$, which fits within the limits ($N=10^6, M=2 \cdot 10^5$).
5.  **Edge Cases**: Handled by checking if queries return valid values (-1). If no operation covers `curr`, output -1.
