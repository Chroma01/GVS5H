
## ideation
The problem asks whether a partially colored $N \times N$ grid can be completed such that every row consists of a prefix of black cells followed by white cells, and every column consists of a prefix of black cells followed by white cells.

Let $R_r$ be the number of black cells in row $r$ (so cells $(r, 1) \dots (r, R_r)$ are black, and $(r, R_r+1) \dots (r, N)$ are white).
Let $C_c$ be the number of black cells in column $c$ (so cells $(1, c) \dots (C_c, c)$ are black, and $(C_c+1, \dots, N, c)$ are white).

A cell $(r, c)$ is black if and only if $c \le R_r$ AND $r \le C_c$.
A cell $(r, c)$ is white if and only if $c > R_r$ OR $r > C_c$.

Given pre-colored cells:
1. If $(r, c)$ is Black, we must have $R_r \ge c$ and $C_c \ge r$.
2. If $(r, c)$ is White, we must have $R_r < c$ OR $C_c < r$.

We can define bounds for each row $r$ and column $c$ based on the pre-colored cells:
- $R_{min}[r] = \max(\{c \mid (r,c) \text{ is Black}\} \cup \{0\})$
- $R_{max}[r] = \min(\{c-1 \mid (r,c) \text{ is White}\} \cup \{N\})$
- $C_{min}[c] = \max(\{r \mid (r,c) \text{ is Black}\} \cup \{0\})$
- $C_{max}[c] = \min(\{r-1 \mid (r,c) \text{ is White}\} \cup \{N\})$

If for any row $r$, $R_{min}[r] > R_{max}[r]$, it's impossible. Similarly for any column $c$, if $C_{min}[c] > C_{max}[c]$, it's impossible.

For the white cells, the condition is $R_r < c \lor C_c < r$.
If we choose the minimal valid values $R_r = R_{min}[r]$ and $C_c = C_{min}[c]$, the condition becomes $R_{min}[r] < c \lor C_{min}[c] < r$.
This is equivalent to NOT ($R_{min}[r] \ge c$ AND $C_{min}[c] \ge r$).
If this condition fails for any white cell, then no solution exists because any valid $R_r \ge R_{min}[r]$ and $C_c \ge C_{min}[c]$ would also fail the condition (since increasing $R_r$ or $C_c$ makes the inequality $R_r < c$ or $C_c < r$ harder to satisfy).
Conversely, if this condition holds for all white cells, then setting $R_r = R_{min}[r]$ and $C_c = C_{min}[c]$ provides a valid solution.

Thus, the algorithm is:
1. Compute $R_{min}, R_{max}$ for all rows involved in input.
2. Compute $C_{min}, C_{max}$ for all columns involved in input.
3. Check consistency of bounds for each row/col.
4. For each white cell $(r, c)$, check if $R_{min}[r] \ge c$ AND $C_{min}[c] \ge r$. If so, return "No".
5. If all checks pass, return "Yes".

Pitfalls:
- $N$ is up to $10^9$, so we cannot iterate over all cells. We only process the $M$ given cells.
- Need to handle rows/cols not in input correctly (default bounds).
- Use efficient data structures (hash maps or arrays if indices are small, but here indices are large so use dictionaries/hash maps).

## worker: <none>
The problem requires checking if a partially colored grid can be completed such that each row and column has a prefix of black cells followed by white cells. This structure implies that for each row $r$, there is a threshold $R_r$ (number of black cells), and for each column $c$, there is a threshold $C_c$. A cell $(r, c)$ is black iff $c \le R_r$ and $r \le C_c$, and white otherwise.

Given pre-colored cells:
1. Black cell at $(r, c)$ imposes $R_r \ge c$ and $C_c \ge r$.
2. White cell at $(r, c)$ imposes $R_r < c$ OR $C_c < r$.

We compute the tightest lower bounds $R_{min}[r]$ and $C_{min}[c]$ from black cells, and tightest upper bounds $R_{max}[r]$ and $C_{max}[c]$ from white cells. If $R_{min}[r] > R_{max}[r]$ or $C_{min}[c] > C_{max}[c]$ for any row/column, it's impossible.

For white cells, the condition $R_r < c \lor C_c < r$ must hold. Choosing the minimal valid thresholds $R_r = R_{min}[r]$ and $C_c = C_{min}[c]$ makes it hardest to satisfy the "OR" condition (since smaller values make $R_r < c$ and $C_c < r$ more likely to be true? No, wait. $R_r < c$ is easier if $R_r$ is small. So choosing minimal $R_r$ and $C_c$ is the BEST strategy to satisfy white cell conditions. If it fails with minimal values, it will fail with any larger values).

Thus, we only need to check if for every white cell $(r, c)$, $R_{min}[r] < c$ OR $C_{min}[c] < r$. If this fails for any white cell, output "No". Otherwise, "Yes".

Complexity: $O(M)$ time and space, which fits within constraints ($M \le 2 \times 10^5$).
