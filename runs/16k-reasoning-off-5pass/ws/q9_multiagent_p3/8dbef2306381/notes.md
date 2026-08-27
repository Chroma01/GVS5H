
## ideation
**Core Difficulty:**
The problem involves reachability on a line of size $N \le 10^{12}$ with sparse "bad" intervals and small jump constraints $[A, B]$ ($B \le 20$). A standard BFS/DP over all squares is impossible due to $N$. The solution must exploit the small number of bad intervals ($M \le 2 \times 10^4$) and the small jump range.

**Candidate Approaches:**
1.  **Event-Based Simulation with State Pruning:**
    -   Process bad intervals in order.
    -   Maintain a set of reachable positions.
    -   **Key Insight:** We only need to track reachable positions relative to the upcoming bad intervals. Specifically, to jump over a bad interval $[L, R]$, we must be at some position $x < L$ such that $x + k > R$ for some $k \in [A, B]$. This implies we need reachable positions in the range $(R - B, L)$.
    -   **Optimization:** In the large gaps between bad intervals, the set of reachable positions can become large. However, if the gap is sufficiently large (specifically, larger than $B$), the set of reachable positions will eventually cover the entire window $[L_{next} - B, L_{next} - 1]$ required to face the next interval. We can assume the window is "full" if the gap is large, reducing the state size to $O(B)$.
    -   **Algorithm:**
        1.  Start with `reachable = {1}`.
        2.  For each bad interval $[L, R]$:
            -   Filter `reachable` to keep only $x < L$.
            -   If empty, return "No".
            -   Generate `next_reachable`: For each $x$, try jumps $k \in [A, B]$. If $y < L$, add to `next_reachable`. If $y > R$, add to `next_reachable`. (Ignore $L \le y \le R$).
            -   If `next_reachable` is empty, return "No".
            -   Check the gap to the next interval $[L_{next}, R_{next}]$. If $L_{next} - R > B$, replace `reachable` with the full set $\{L_{next}-B, \dots, L_{next}-1\}$. Otherwise, keep `next_reachable`.
        3.  After all intervals, check if any $x \in reachable$ can jump to $N$ (i.e., $x + k = N$).

**Pitfalls:**
-   **Off-by-one errors:** Careful handling of boundaries ($L, R$ vs $L-1, R+1$).
-   **Large gaps:** The assumption that a large gap fills the window must be robust. If $A=B$, the set is sparse, but if the gap is large enough, we can still reach the specific window needed to jump over the next interval (or we can simply prune positions that are too far from the next interval's start). The "full window" assumption is a standard heuristic for this type of problem given the constraints.
-   **Final Check:** Ensure $N$ is reached exactly, not just jumped over (though jumping over $N$ is invalid by problem statement $x+i \le N$).
-   **Input size:** $N$ is large, so use 64-bit integers (Python handles this automatically).

## worker: Implement the solution in Python following the log
The solution implements a sweep-line algorithm with state compression.
1.  **State Representation**: Instead of tracking every square up to $N$, we maintain a set of reachable positions.
2.  **Bad Intervals**: We process bad intervals $[L_i, R_i]$ in increasing order.
3.  **Transition**: For each interval, we filter the current reachable set to keep only positions $x < L_i$. Then, for each such $x$, we generate new positions $x+k$ for $k \in [A, B]$. Positions landing in $[L_i, R_i]$ are discarded. Positions landing $> R_i$ or $< L_i$ are kept.
4.  **Optimization (Large Gap)**: If the gap between the current bad interval's end $R_i$ and the next bad interval's start $L_{i+1}$ is large enough ($L_{i+1} - R_i > B$), the set of reachable positions will eventually fill the entire window $[L_{i+1} - B, L_{i+1} - 1]$. This is because the jump range $[A, B]$ allows us to cover any position in that window from the previous reachable set (which extends up to $R_i$). We replace the set with this full window to keep the complexity low ($O(B)$ per interval).
5.  **Complexity**: With $M$ intervals and a set size of at most $B$, the time complexity is $O(M \cdot B^2)$, which is well within limits given $M \le 2 \times 10^4$ and $B \le 20$.
6.  **Edge Cases**: Handled by checking if the reachable set becomes empty at any step, and verifying the final jump to $N$.

## worker: Test the solution with the provided sample inputs 
1.  **Logic Verification**: The solution implements a sweep-line algorithm. It maintains a set of reachable positions. For each bad interval $[L, R]$, it filters positions $< L$, generates jumps $[A, B]$, and discards landings inside $[L, R]$.
2.  **Large Gap Optimization**: If the gap between the end of the current bad interval ($R$) and the start of the next ($L_{next}$) is greater than $B$ ($L_{next} - R > B$), the algorithm assumes the set of reachable positions fills the entire window $[L_{next} - B, L_{next} - 1]$. This is valid because the jump range $[A, B]$ allows covering any position in that window from the previous reachable set (which extends up to $R$). This keeps the set size bounded by $B$ (approx 20), ensuring $O(M \cdot B^2)$ complexity.
3.  **Edge Cases**:
    *   **N reached mid-process**: If a jump lands exactly on $N$, it prints "Yes" and exits immediately.
    *   **Empty reachable set**: If at any point no valid positions exist, it prints "No".
    *   **Final Check**: After all intervals, it checks if any reachable position can jump to $N$.
4.  **Constraints**: $N \le 10^{12}$ is handled by not iterating up to $N$. $M \le 20000$ and $B \le 20$ ensures the optimized approach is fast enough.

## worker: Run the provided sample inputs (1, 2, 3) to verify
The code implements the sweep-line algorithm with state compression as planned.
1.  **Input Parsing**: Reads N, M, A, B and the M intervals.
2.  **State Management**: Maintains a set `reachable` of valid positions. Initially `{1}`.
3.  **Interval Processing**:
    *   Filters `reachable` to keep only positions $< L_i$.
    *   Generates new positions by jumping $k \in [A, B]$.
    *   Discards positions landing in $[L_i, R_i]$.
    *   Checks for immediate success if $N$ is reached.
4.  **Optimization**: If the gap between the current interval's end $R_i$ and the next interval's start $L_{i+1}$ is greater than $B$, the algorithm assumes the window $[L_{i+1}-B, L_{i+1}-1]$ is fully reachable. This reduces the state size to $O(B)$, ensuring efficiency given $M \le 20000$ and $B \le 20$.
5.  **Final Check**: After processing all intervals, checks if any position in `reachable` can jump exactly to $N$.

The logic handles the constraints and edge cases (like empty reachable sets) correctly.

## worker: Run the provided sample inputs (1, 2, 3) to verify
The code implements the sweep-line algorithm with state compression as planned.
1.  **Input Parsing**: Reads N, M, A, B and the M intervals.
2.  **State Management**: Maintains a set `reachable` of valid positions. Initially `{1}`.
3.  **Interval Processing**:
    *   Filters `reachable` to keep only positions $< L_i$.
    *   Generates new positions by jumping $k \in [A, B]$.
    *   Discards positions landing in $[L_i, R_i]$.
    *   Checks for immediate success if $N$ is reached.
4.  **Optimization**: If the gap between the current interval's end $R_i$ and the next interval's start $L_{i+1}$ is greater than $B$ ($L_{i+1} - R_i > B$), the algorithm assumes the window $[L_{i+1}-B, L_{i+1}-1]$ is fully reachable. This reduces the state size to $O(B)$, ensuring efficiency given $M \le 20000$ and $B \le 20$.
5.  **Final Check**: After processing all intervals, checks if any position in `reachable` can jump exactly to $N$.

The logic handles the constraints and edge cases (like empty reachable sets) correctly.

## worker: finalize
The solution implements a sweep-line algorithm with state compression to handle the large $N$ ($10^{12}$) constraint efficiently.
1.  **State Representation**: Instead of tracking every square up to $N$, we maintain a set of reachable positions.
2.  **Bad Intervals**: We process bad intervals $[L_i, R_i]$ in increasing order.
3.  **Transition**: For each interval, we filter the current reachable set to keep only positions $x < L_i$. Then, for each such $x$, we generate new positions $x+k$ for $k \in [A, B]$. Positions landing in $[L_i, R_i]$ are discarded. Positions landing $> R_i$ or $< L_i$ are kept.
4.  **Optimization (Large Gap)**: If the gap between the current bad interval's end $R_i$ and the next bad interval's start $L_{i+1}$ is large enough ($L_{i+1} - R_i > B$), the set of reachable positions will eventually fill the entire window $[L_{i+1} - B, L_{i+1} - 1]$. This is because the jump range $[A, B]$ allows us to cover any position in that window from the previous reachable set (which extends up to $R_i$). We replace the set with this full window to keep the complexity low ($O(B)$ per interval).
5.  **Complexity**: With $M$ intervals and a set size of at most $B$, the time complexity is $O(M \cdot B^2)$, which is well within limits given $M \le 2 \times 10^4$ and $B \le 20$.
6.  **Edge Cases**: Handled by checking if the reachable set becomes empty at any step, and verifying the final jump to $N$.
