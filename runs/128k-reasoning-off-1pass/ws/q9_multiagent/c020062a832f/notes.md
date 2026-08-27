
## ideation
**Core Difficulty**:
The problem asks for the inversion count of a sequence $B$ where $B_i = (A_i + k) \pmod M$ for $k = 0, \dots, M-1$.
- $N, M \le 2 \times 10^5$.
- A naive calculation for each $k$ takes $O(N \log N)$ or $O(N^2)$, leading to $O(MN \log N)$ total time, which is too slow ($\approx 4 \times 10^{10}$ operations).
- We need an incremental approach: calculate the answer for $k=0$, then update it efficiently as $k$ increases to $k+1$.

**Key Insight**:
The value $B_i$ changes from $(A_i + k) \pmod M$.
- If $A_i + k < M$, then $B_i = A_i + k$. The value increases by 1.
- If $A_i + k \ge M$, then $B_i = A_i + k - M$. The value decreases by $M-1$ (effectively wrapping around).
The relative order of elements only changes when an element "wraps around".
- Let $S_{small}$ be the set of indices where $A_i + k < M$.
- Let $S_{large}$ be the set of indices where $A_i + k \ge M$.
- In the sequence $B$, elements in $S_{small}$ are sorted by $A_i + k$, and elements in $S_{large}$ are sorted by $A_i + k - M$.
- Crucially, all values in $S_{small}$ are strictly smaller than all values in $S_{large}$ in the current configuration $B$ (since max in $S_{small}$ is $M-1$ and min in $S_{large}$ is $0$).
- Wait, this is not strictly true for the *values* in the sequence $B$ at index $i$, but for the *set of values*.
  - Actually, $B_i \in [0, M-1]$.
  - For a fixed $k$, if $A_i + k < M$, $B_i = A_i + k \in [k, M-1]$.
  - If $A_i + k \ge M$, $B_i = A_i + k - M \in [0, k-1]$.
  - So, the set of values coming from $S_{large}$ (wrapped) are all $< k$, and the set of values coming from $S_{small}$ (not wrapped) are all $\ge k$.
  - Therefore, **every element in $S_{large}$ is smaller than every element in $S_{small}$**.
  
**Transition from $k$ to $k+1$**:
- An element $i$ moves from $S_{small}$ to $S_{large}$ if $A_i + k = M-1$ (so at $k+1$, $A_i + (k+1) \ge M$).
  - Condition: $A_i = M - 1 - k$.
- When element $i$ moves from $S_{small}$ to $S_{large}$:
  - At step $k$: $i \in S_{small}$. Its value is $A_i + k$. It contributes to inversions with $j \in S_{large}$ (where $B_j < B_i$) and $j \in S_{small}$ (where $i < j$ and $B_i > B_j$).
  - At step $k+1$: $i \in S_{large}$. Its value becomes small ($\approx 0$). It will be smaller than all elements in $S_{small}$ and larger than some elements in $S_{large}$ (those that wrapped earlier).
  
Let's refine the update logic.
Let $cnt[x]$ be the number of elements in $S_{large}$ that have value $x$. Or better, maintain a Fenwick tree (BIT) for the values currently in $S_{large}$.
Actually, since the values in $S_{large}$ are always in the range $[0, k-1]$ and values in $S_{small}$ are in $[k, M-1]$, the structure is very clean.
At step $k$:
- $S_{large}$ contains indices where $A_i \ge M-k$. Their values are $A_i - (M-k)$.
- $S_{small}$ contains indices where $A_i < M-k$. Their values are $A_i + k$.
- All values in $S_{large}$ are $< k$. All values in $S_{small}$ are $\ge k$.
- Thus, for any $i \in S_{large}$ and $j \in S_{small}$: $B_i < B_j$.
  - Inversion pairs involving one from $S_{large}$ and one from $S_{small}$:
    - If $i \in S_{large}, j \in S_{small}$ and $i < j$: Since $B_i < B_j$, this is NOT an inversion.
    - If $i \in S_{small}, j \in S_{large}$ and $i < j$: Since $B_i > B_j$, this IS an inversion.
  - So, inversions between sets = count of pairs $(i, j)$ such that $i \in S_{small}, j \in S_{large}, i < j$.

Now, moving from $k$ to $k+1$:
- Elements with $A_i = M - 1 - k$ move from $S_{small}$ to $S_{large}$. Let this set of indices be $W_k$.
- For each $i \in W_k$:
  - **Before move ($k$)**: $i \in S_{small}$.
    - Inversions with $j \in S_{large}$: Since $B_i \ge k$ and $B_j < k$, $B_i > B_j$. So if $i < j$, it's an inversion. If $i > j$, it's not.
      - Contribution: Count of $j \in S_{large}$ such that $j > i$.
    - Inversions with $p \in S_{small}$: Depends on relative order and values.
  - **After move ($k+1$)**: $i \in S_{large}$.
    - Inversions with $j \in S_{small}$: Now $B_i < k+1$ and $B_j \ge k+1$. So $B_i < B_j$.
      - If $i < j$: $B_i < B_j$ (No inversion). Previously ($i \in S_{small}, j \in S_{large}$) if $i < j$, it was an inversion. So we **subtract** the count of $j \in S_{large}$ with $j > i$.
      - If $i > j$: $B_i < B_j$ (No inversion). Previously ($i \in S_{small}, j \in S_{large}$) if $i > j$, it was NOT an inversion. No change.
    - Inversions with $p \in S_{small}$:
      - $i \in S_{large}, p \in S_{small}$. $B_i < B_p$.
      - If $i < p$: $B_i < B_p$ (No inversion). Previously ($p \in S_{small}, i \in S_{small}$): $B_p = A_p + k, B_i = A_i + k$. Since $A_p, A_i$ are fixed, the relative order of values didn't change for two elements both in $S_{small}$.
      - If $i > p$: $B_i < B_p$ (No inversion). Previously ($p \in S_{small}, i \in S_{small}$): $B_p > B_i$? No, $B_p = A_p+k, B_i = A_i+k$. If $A_p > A_i$, then $B_p > B_i$, so $(p, i)$ was an inversion. Now $i \in S_{large}, p \in S_{small}$, $B_i < B_p$, so $(i, p)$ is not an inversion. Wait, we need to check pairs $(x, y)$ with $x < y$.
      - Let's re-evaluate internal $S_{small}$ changes.
        - For any pair $p, q \in S_{small}$, their values are $A_p+k$ and $A_q+k$. The comparison $A_p+k > A_q+k$ is equivalent to $A_p > A_q$. This does not change as $k$ increases, as long as both stay in $S_{small}$.
        - So inversions strictly within $S_{small}$ are constant as long as no element leaves $S_{small}$.
        - Similarly, inversions strictly within $S_{large}$: Values are $A_p - (M-k)$ and $A_q - (M-k)$. Comparison $A_p > A_q$ is constant.
        - So the only changes come from the boundary elements moving between sets.

## worker: finalize
The solution implements an incremental approach to calculate the inversion number for $M$ sequences.
1.  **Initial State ($k=0$)**: We calculate the inversion count for the original array $A$ using a Fenwick Tree (BIT) in $O(N \log N)$.
2.  **Transition Logic**: As $k$ increments from $0$ to $M-1$, elements $A_i$ where $A_i + k \ge M$ are considered "wrapped" (in set $S_{large}$), while others are "unwrapped" ($S_{small}$).
    -   At step $k$, elements with $A_i = M - 1 - k$ transition from $S_{small}$ to $S_{large}$.
    -   For an element $i$ moving from $S_{small}$ to $S_{large}$:
        -   **Before**: It contributes to inversions with $j \in S_{large}$ if $i < j$ (since $B_i > B_j$). It contributes to inversions with $p \in S_{small}$ if $p < i$ and $A_p > A_i$.
        -   **After**: It contributes to inversions with $j \in S_{large}$ if $i < j$ and $B_i > B_j$. Since $A_i < A_j$ for all $j \in S_{large}$ (as $A_j \ge M-k > M-1-k = A_i$), $B_i < B_j$, so no inversions with $S_{large}$. Wait, my previous derivation was:
          -   Before: $i \in S_{small}, j \in S_{large} \implies B_i > B_j$. Inversion if $i < j$.
          -   After: $i \in S_{large}, j \in S_{large} \implies B_i < B_j$ (since $A_i < A_j$). No inversion if $i < j$.
          -   So we **subtract** the count of $j \in S_{large}$ with $j > i$.
        -   With $p \in S_{small}$:
          -   Before: $p, i \in S_{small}$. Inversion if $p < i$ and $A_p > A_i$.
          -   After: $p \in S_{small}, i \in S_{large} \implies B_p > B_i$. Inversion if $p < i$.
          -   Since $A_p \le A_i$ implies $A_p > A_i$ is false, the "Before" count is 0 for $A_p \le A_i$. The "After" count is 1 for $p < i$.
          -   Since we process elements with $A_i = M-1-k$, and previous batches had $A_p > M-1-k$ (wait, $k$ increases, so $M-1-k$ decreases. So previous batches had larger $A_p$).
          -   Let's re-verify the batch order.
            -   $k=0$: Move $A_i = M-1$.
            -   $k=1$: Move $A_i = M-2$.
            -   ...
            -   So we process elements with decreasing $A_i$.
            -   When processing batch with value $V$, all previously processed elements have $A_p > V$.
            -   For $p$ in previous batches ($A_p > V$):
                -   Before: $p, i \in S_{small}$. $A_p > A_i$. Inversion if $p < i$.
                -   After: $p \in S_{small}, i \in S_{large}$. $B_p > B_i$. Inversion if $p < i$.
                -   Change: 0.
            -   For $p$ in current batch ($A_p = V$):
                -   Before: $p, i \in S_{small}$. $A_p = A_i$. No inversion.
                -   After: $p \in S_{small}, i \in S_{large}$. $B_p > B_i$. Inversion if $p < i$.
                -   Change: +1 if $p < i$.
            -   So for $p$ in current batch with $p < i$, we add 1.
            -   For $p$ in previous batches with $p < i$, we add 0.
            -   Total addition from $S_{small}$ side: Count of $p \in S_{small}$ (including current batch) with $p < i$.
            -   Wait, my code used `bit_small.query(i-1)` which includes the current batch elements if they are already in `bit_small`.
            -   In the proposed algorithm:
                1. Calculate deltas using current state of BITs (where current batch is still in `bit_small`).
                2. Then remove current batch from `bit_small`.
            -   So `bit_small.query(i-1)` counts all $p$ in $S_{small}$ (including other members of current batch) with $p < i$.
            -   This matches the logic:
                -   $p$ in previous batches ($A_p > A_i$): Before inv if $p<i$. After inv if $p<i$. Net change 0.
                -   $p$ in current batch ($A_p = A_i$): Before inv 0. After inv if $p<i$. Net change +1.
                -   Sum of changes = Count($p \in S_{small}, p < i$).
            -   Subtraction from $S_{large}$ side: Count($j \in S_{large}, j > i$).
            -   So the formula `Delta = query_small(i-1) - (total_large - query_large(i))` is correct.

3.  **Complexity**:
    -   Initialization: $O(N \log N)$.
    -   Loop $M$ times. Inside, we iterate over elements moving. Each element moves exactly once.
    -   BIT operations are $O(\log N)$.
    -   Total Time: $O(N \log N + M \log N)$. Given $N, M \le 2 \times 10^5$, this fits well within time limits.
    -   Space: $O(N + M)$.
