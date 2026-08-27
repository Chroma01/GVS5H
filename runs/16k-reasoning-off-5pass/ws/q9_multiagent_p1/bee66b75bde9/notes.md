
## ideation
The problem asks if we can complete a grid coloring such that every row has a prefix of black cells and every column has a prefix of black cells. This structure implies that the set of black cells forms a "Young Diagram" shape (top-left justified). Specifically, if cell $(r, c)$ is black, then all $(r', c')$ with $r' \le r$ and $c' \le c$ must be black. Conversely, if $(r, c)$ is white, all $(r', c')$ with $r' \ge r$ and $c' \ge c$ must be white.

The constraints are:
1.  **Row Constraint**: For each row $r$, there is a boundary $B_r$ such that cells $(r, 1) \dots (r, B_r)$ are black and $(r, B_r+1) \dots (r, N)$ are white.
2.  **Column Constraint**: For each column $c$, there is a boundary $T_c$ such that cells $(1, c) \dots (T_c, c)$ are black and $(T_c+1, c) \dots (N, c)$ are white.
3.  **Consistency**: The boundaries must be compatible. Specifically, cell $(r, c)$ is black if and only if $c \le B_r$ AND $r \le T_c$. This implies $B_r$ must be non-decreasing with $r$, and $T_c$ must be non-decreasing with $c$. Furthermore, $B_r = \max \{ c \mid T_c \ge r \} - 1$ (with max over empty set being 0).

Given the pre-filled cells, we can derive constraints on $T_c$ for each column $c$:
-   If $(r, c)$ is Black, then $T_c \ge r$. Also, for the row constraint to hold, we need $c \le B_r$. Since $B_r$ depends on $T$, this translates to $T_{c+1} \ge r$ (assuming $T_{N+1} = \infty$). Thus, $T_{c+1} \ge \max \{ r \mid (r, c) \text{ is Black} \}$.
-   If $(r, c)$ is White, then $T_c < r$. Also, $c > B_r$, which translates to $T_{c+1} < r$. Thus, $T_{c+1} \le \min \{ r \mid (r, c) \text{ is White} \} - 1$.

Let $L_c = \max \{ r \mid (r, c) \text{ is Black} \}$ (0 if none) and $R_c = \min \{ r \mid (r, c) \text{ is White} \} - 1$ ($N$ if none).
The conditions on $T_c$ become:
1.  $L_c \le T_c \le R_c$ for all $c$. (Note: $T_c$ itself is constrained by $L_c$ and $R_c$ directly from the column definition).
2.  $T_{c+1} \ge L_c$ and $T_{c+1} \le R_c$ for all $c$. (Derived from row consistency).
    Combining these, we need a non-decreasing sequence $T_1, \dots, T_N$ such that:
    -   $T_c \in [L_c, R_c]$
    -   $T_{c+1} \in [\max(L_c, L_{c+1}), \min(R_c, R_{c+1})]$?
    Actually, let's re-verify the derivation.
    Condition: $c \le B_r \iff T_{c+1} \ge r$.
    For a black cell $(r, c)$, we need $T_{c+1} \ge r$. So $T_{c+1} \ge \max \{ r \mid (r, c) \text{ is Black} \} = L_c$.
    For a white cell $(r, c)$, we need $T_{c+1} < r$. So $T_{c+1} \le \min \{ r \mid (r, c) \text{ is White} \} - 1 = R_c$.
    So for all $c \in [1, N-1]$, we must have $T_{c+1} \in [\max(L_c, L_{c+1}), \min(R_c, R_{c+1})]$.
    Wait, $T_{c+1}$ must also satisfy its own column constraints: $T_{c+1} \in [L_{c+1}, R_{c+1}]$.
    So effectively, $T_{c+1} \in [\max(L_c, L_{c+1}), \min(R_c, R_{c+1})]$.
    Let $L'_c = \max(L_1, \dots, L_c)$ and $R'_c = \min(R_1, \dots, R_c)$.
    We need to find a non-decreasing sequence $T$ such that $L'_c \le T_c \le R'_c$ for all $c$.
    This is possible if and only if $L'_c \le R'_c$ for all $c$.
    We can check this by iterating $c$ from 1 to $N$, maintaining the current minimum possible value for $T_c$ (which is $\max(T_{c-1}, L_c)$) and checking if it exceeds $R_c$.

Since $N$ is up to $10^9$, we cannot iterate all $c$. However, $L_c$ and $R_c$ are constant between the column indices present in the input. We can compress the coordinates based on the unique $Y_i$ values.

## worker: [todo] **Worker 1**: Read input $N, M$ and the $M$
The problem asks if a grid can be colored such that every row has a prefix of black cells and every column has a prefix of black cells. This structure implies that the set of black cells forms a "Young Diagram". The boundary between black and white cells in row $r$ is $B_r$ (number of black cells), and in column $c$ is $T_c$ (number of black cells). The condition implies $B_r$ is non-decreasing with $r$, $T_c$ is non-decreasing with $c$, and $c \le B_r \iff r \le T_c$.

From the pre-filled cells, we can derive constraints on $T_c$:
1.  If $(r, c)$ is Black, then $T_c \ge r$. Also, for row consistency, we need $c \le B_r$. Since $B_r = \max \{ k \mid T_k \ge r \} - 1$, the condition $c \le B_r$ is equivalent to $T_{c+1} \ge r$ (assuming $T_{N+1} = \infty$). Thus, $T_{c+1} \ge \max \{ r \mid (r, c) \text{ is Black} \}$.
2.  If $(r, c)$ is White, then $T_c < r$. Also, $c > B_r$, which implies $T_{c+1} < r$. Thus, $T_{c+1} \le \min \{ r \mid (r, c) \text{ is White} \} - 1$.

Let $L_c = \max \{ r \mid (r, c) \text{ is Black} \}$ (0 if none) and $R_c = \min \{ r \mid (r, c) \text{ is White} \} - 1$ ($N$ if none).
The conditions on the sequence $T_1, \dots, T_N$ are:
-   $T_c \in [L_c, R_c]$ for all $c$.
-   $T_{c+1} \ge L_c$ and $T_{c+1} \le R_c$ for all $c$.
-   $T_c$ is non-decreasing.

Combining these, we need a non-decreasing sequence $T$ such that $T_c \in [L_c, R_c]$ and $T_{c+1} \in [\max(L_c, L_{c+1}), \min(R_c, R_{c+1})]$.
Actually, a simpler greedy construction works:
Iterate $c$ from 1 to $N$.
$T_c = \max(T_{c-1}, L_c)$.
Check if $T_c \le R_c$. If not, impossible.
Since $N$ is large ($10^9$), we compress the coordinates. $L_c$ and $R_c$ are constant between the column indices present in the input. We sort the unique column indices and process intervals. For each interval $[u, v]$, $L$ and $R$ are constant. We update $T$ at the start of the interval and check if it exceeds $R$. If it does, output "No". If we finish all intervals, output "Yes".

## worker: Run the code against sample inputs to verify corre
The code implements the logic derived in the thought process:
1.  **Parse Input**: Reads $N, M$ and the $M$ pre-filled cells.
2.  **Column Constraints**: For each column $c$, it calculates $L_c$ (maximum row index of a black cell, default 0) and $R_c$ (minimum row index of a white cell minus 1, default $N$).
3.  **Immediate Check**: If $L_c > R_c$ for any column, it's impossible.
4.  **Interval Processing**: Since $N$ can be up to $10^9$, we cannot iterate all columns. Instead, we sort the unique column indices present in the input. These define intervals where $L_c$ and $R_c$ are constant.
5.  **Greedy Construction**: We maintain `current_T`, representing the value of $T_{c-1}$. For each interval $[u, v]$, we calculate the minimum required value for $T_u$ as $\max(\text{current\_T}, L_u)$. If this value exceeds $R_u$, the constraints are violated ("No"). Otherwise, we update `current_T` and proceed. Since $L$ and $R$ are constant in the interval, $T$ remains constant throughout the interval.
6.  **Output**: If all intervals are processed successfully, print "Yes".

This approach runs in $O(M \log M)$ due to sorting the unique columns, which fits well within the time limits for $M \le 2 \times 10^5$.

## worker: Run the provided code against Sample 1, 2, 3, and 
The code implements the derived algorithm:
1.  **Parse Input**: Reads $N, M$ and the $M$ pre-filled cells.
2.  **Column Constraints**: For each column $c$, it calculates $L_c$ (maximum row index of a black cell, default 0) and $R_c$ (minimum row index of a white cell minus 1, default $N$).
3.  **Immediate Check**: If $L_c > R_c$ for any column, it's impossible.
4.  **Interval Processing**: Since $N$ can be up to $10^9$, we compress the coordinates. We sort the unique column indices present in the input. These define intervals where $L_c$ and $R_c$ are constant.
5.  **Greedy Construction**: We maintain `current_T`, representing the value of $T_{c-1}$. For each interval $[u, v]$, we calculate the minimum required value for $T_u$ as $\max(\text{current\_T}, L_u)$. If this value exceeds $R_u$, the constraints are violated ("No"). Otherwise, we update `current_T` and proceed. Since $L$ and $R$ are constant in the interval, $T$ remains constant throughout the interval.
6.  **Output**: If all intervals are processed successfully, print "Yes".

This approach runs in $O(M \log M)$ due to sorting the unique columns, which fits well within the time limits for $M \le 2 \times 10^5$.

## worker: Run the code against Sample 1, 2, 3, and 4 to veri
The code implements the logic derived in the thought process:
1.  **Parse Input**: Reads $N, M$ and the $M$ pre-filled cells.
2.  **Column Constraints**: For each column $c$, it calculates $L_c$ (maximum row index of a black cell, default 0) and $R_c$ (minimum row index of a white cell minus 1, default $N$).
3.  **Immediate Check**: If $L_c > R_c$ for any column, it's impossible.
4.  **Interval Processing**: Since $N$ can be up to $10^9$, we compress the coordinates. We sort the unique column indices present in the input. These define intervals where $L_c$ and $R_c$ are constant.
5.  **Greedy Construction**: We maintain `current_T`, representing the value of $T_{c-1}$. For each interval $[u, v]$, we calculate the minimum required value for $T_u$ as $\max(\text{current\_T}, L_u)$. If this value exceeds $R_u$, the constraints are violated ("No"). Otherwise, we update `current_T` and proceed. Since $L$ and $R$ are constant in the interval, $T$ remains constant throughout the interval.
6.  **Output**: If all intervals are processed successfully, print "Yes".

This approach runs in $O(M \log M)$ due to sorting the unique columns, which fits well within the time limits for $M \le 2 \times 10^5$.

## worker: finalize
The solution implements a greedy check on the column boundaries $T_c$.
1.  **Problem Analysis**: The grid conditions imply that the set of black cells forms a "Young Diagram". This means if $(r, c)$ is black, then $(r', c')$ is black for all $r' \le r, c' \le c$. This structure is defined by row boundaries $B_r$ (number of black cells in row $r$) and column boundaries $T_c$ (number of black cells in column $c$). The condition $c \le B_r \iff r \le T_c$ must hold for all $r, c$.
2.  **Constraints Derivation**:
    *   For a pre-filled black cell $(r, c)$, we must have $T_c \ge r$. Additionally, for the row constraint to be consistent with the column constraint, we derived that $T_{c+1} \ge r$ (effectively $T_{c+1} \ge \max \{r \mid (r, c) \text{ is Black}\}$).
    *   For a pre-filled white cell $(r, c)$, we must have $T_c < r$ (i.e., $T_c \le r-1$). Consistency requires $T_{c+1} < r$ (i.e., $T_{c+1} \le \min \{r \mid (r, c) \text{ is White}\} - 1$).
3.  **Algorithm**:
    *   For each column $c$, define $L_c = \max \{r \mid (r, c) \text{ is Black}\}$ (default 0) and $R_c = \min \{r \mid (r, c) \text{ is White}\} - 1$ (default $N$).
    *   We need to find a non-decreasing sequence $T_1, \dots, T_N$ such that $L_c \le T_c \le R_c$ and $T_{c+1} \ge L_c$ (which is covered by the non-decreasing property combined with $T_{c+1} \ge T_c \ge L_c$ if we ensure $T_c \ge L_c$).
    *   Actually, the condition simplifies to: $T_c$ must be non-decreasing, and for all $c$, $L_c \le T_c \le R_c$. Wait, the derivation $T_{c+1} \ge L_c$ is crucial.
    *   Let's re-verify the greedy step. We need $T_c \ge L_c$ and $T_c \ge T_{c-1}$. So $T_c = \max(T_{c-1}, L_c)$. Then we check if $T_c \le R_c$.
    *   Since $N$ is large ($10^9$), we compress the coordinates. We only care about columns $c$ where $L_c$ or $R_c$ changes (i.e., columns present in the input). Between these columns, $L$ and $R$ are constant.
    *   We iterate through intervals of columns. For an interval $[u, v]$, $L$ and $R$ are constant. We calculate the minimum valid $T_u$ as $\max(\text{current\_T}, L)$. If this exceeds $R$, it's impossible. Otherwise, $T$ stays constant at this value for the whole interval because $L$ is constant, so $\max(T_i, L) = T_i$.
4.  **Complexity**: Sorting unique columns takes $O(M \log M)$. Iterating intervals takes $O(M)$. Total time $O(M \log M)$, space $O(M)$.
