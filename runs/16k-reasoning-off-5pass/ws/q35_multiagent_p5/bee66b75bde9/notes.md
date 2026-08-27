
## ideation
The core difficulty lies in efficiently handling the constraints for an $N \times N$ grid where $N$ can be up to $10^9$, while only $M$ cells are pre-colored ($M \le 2 \times 10^5$). We cannot iterate over all cells.

The problem requires that each row $r$ has a threshold $R_r$ such that cells $(r, 1) \dots (r, R_r)$ are black and the rest are white. Similarly, each column $c$ has a threshold $C_c$ such that cells $(1, c) \dots (R_c, c)$ are black and the rest are white. Note that the condition for a cell $(r, c)$ to be black is $c \le R_r$ AND $r \le C_c$. If either condition fails, the cell is white.

From the pre-colored black cells, we can derive minimum required values for $R_r$ and $C_c$:
- For a black cell at $(X_i, Y_i)$, we must have $Y_i \le R_{X_i}$ and $X_i \le C_{Y_i}$.
- Thus, $R_{X_i} \ge Y_i$ and $C_{Y_i} \ge X_i$.
- To maximize the chance of satisfying white cell constraints, we should choose the smallest possible values for $R_r$ and $C_c$. Let $min\_R[r]$ be the maximum $Y_i$ among all black cells in row $r$ (or 0 if none). Let $min\_C[c]$ be the maximum $X_i$ among all black cells in column $c$ (or 0 if none).

For a pre-colored white cell at $(X_i, Y_i)$, the condition is that it is NOT black. This means it must fail at least one of the black conditions:
- $Y_i > R_{X_i}$ OR $X_i > C_{Y_i}$.
- Using our minimal thresholds, we check if $Y_i > min\_R[X_i]$ OR $X_i > min\_C[Y_i]$.
- If this condition fails for any white cell (i.e., $Y_i \le min\_R[X_i]$ AND $X_i \le min\_C[Y_i]$), then it's impossible, and we output "No".

If all white cells satisfy the condition, we output "Yes". We use hash maps (dictionaries) to store $min\_R$ and $min\_C$ since $N$ is large.

Pitfalls:
1. Using arrays of size $N$ will lead to Memory Limit Exceeded or Time Limit Exceeded. Must use dictionaries.
2. Incorrectly interpreting the white cell condition. It's an OR condition for failure of black status.
3. Forgetting that $R_r$ and $C_c$ are determined by the maximum coordinate of black cells in that row/column.

## worker: (None)
The problem asks if a partially colored grid can be completed such that each row has a prefix of black cells and each column has a prefix of black cells. This structure implies that for each row $r$, there is a threshold $R_r$ such that cells $(r, 1) \dots (r, R_r)$ are black, and for each column $c$, there is a threshold $C_c$ such that cells $(1, c) \dots (R_c, c)$ are black. A cell $(r, c)$ is black if and only if $c \le R_r$ AND $r \le C_c$.

From the given black cells, we can derive the minimum necessary values for $R_r$ and $C_c$. Specifically, for a black cell at $(X_i, Y_i)$, we must have $R_{X_i} \ge Y_i$ and $C_{Y_i} \ge X_i$. To maximize the chance of satisfying the white cell constraints, we should choose the smallest possible values for $R_r$ and $C_c$. Thus, we set $min\_R[r] = \max(\{Y_i \mid (r, Y_i) \text{ is black}\} \cup \{0\})$ and $min\_C[c] = \max(\{X_i \mid (X_i, c) \text{ is black}\} \cup \{0\})$.

For each white cell at $(X_i, Y_i)$, it must NOT be black. This means it must fail at least one of the black conditions: $Y_i > R_{X_i}$ OR $X_i > C_{Y_i}$. Using our minimal thresholds, we check if $Y_i > min\_R[X_i]$ OR $X_i > min\_C[Y_i]$. If this condition fails for any white cell (i.e., $Y_i \le min\_R[X_i]$ AND $X_i \le min\_C[Y_i]$), then it's impossible to satisfy the conditions, and we output "No". Otherwise, we output "Yes".

Since $N$ can be up to $10^9$, we use dictionaries to store $min\_R$ and $min\_C$, only storing entries for rows and columns that have at least one black cell. The time complexity is $O(M)$ and space complexity is $O(M)$, which is efficient given $M \le 2 \times 10^5$.
