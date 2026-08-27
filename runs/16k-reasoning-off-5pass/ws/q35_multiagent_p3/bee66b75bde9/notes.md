
## ideation
The core difficulty lies in efficiently checking the consistency of the pre-colored cells with the structural constraints of the grid. The constraints imply that each row $i$ has a threshold $r_i$ such that cells $(i, 1)$ to $(i, r_i)$ are black and the rest are white. Similarly, each column $j$ has a threshold $c_j$ such that cells $(1, j)$ to $(r_j, j)$ are black and the rest are white. A cell $(i, j)$ is black if and only if $j \le r_i$ AND $i \le c_j$. It is white if and only if $j > r_i$ OR $i > c_j$.

From the black cells, we can derive lower bounds for $r_i$ and $c_j$. Specifically, for each row $i$, $r_i$ must be at least the maximum column index of any black cell in that row. Let this be $R_{min}[i]$. Similarly, for each column $j$, $c_j$ must be at least the maximum row index of any black cell in that column. Let this be $C_{min}[j]$. If a row or column has no black cells, the lower bound is 0.

The "minimal" configuration is setting $r_i = R_{min}[i]$ and $c_j = C_{min}[j]$. This configuration minimizes the number of black cells, which is optimal for satisfying the white cell constraints. For a white cell at $(i, j)$, we need $r_i < j$ OR $c_j < i$. In the minimal configuration, this becomes $R_{min}[i] < j$ OR $C_{min}[j] < i$. If this condition fails for any white cell (i.e., $R_{min}[i] \ge j$ AND $C_{min}[j] \ge i$), then it's impossible to satisfy the conditions because increasing $r_i$ or $c_j$ would only make the condition $r_i < j$ or $c_j < i$ harder to satisfy (or keep it false).

Therefore, the algorithm is:
1. Initialize arrays `R_min` and `C_min` of size $N+1$ with 0.
2. For each black cell $(X, Y)$, update `R_min[X] = max(R_min[X], Y)` and `C_min[Y] = max(C_min[Y], X)`.
3. For each white cell $(X, Y)$, check if `R_min[X] < Y` OR `C_min[Y] < X`. If not, return "No".
4. If all white cells satisfy the condition, return "Yes".

Pitfalls:
- $N$ is up to $10^9$, so we cannot allocate arrays of size $N$. However, $M$ is up to $2 \times 10^5$, so we only need to store values for rows and columns that appear in the input. We can use dictionaries (hash maps) for `R_min` and `C_min`.
- The condition for white cells is an OR condition. We must check both parts.
- We need to handle the case where a row or column has no black cells (value 0).

## worker: (None)
The problem requires checking if a partial grid coloring can be extended to satisfy row and column prefix constraints. Each row $i$ has a threshold $r_i$ such that cells $(i, 1)$ to $(i, r_i)$ are black. Each column $j$ has a threshold $c_j$ such that cells $(1, j)$ to $(c_j, j)$ are black. A cell $(i, j)$ is black if and only if $j \le r_i$ AND $i \le c_j$. It is white if and only if $j > r_i$ OR $i > c_j$.

From the black cells, we derive lower bounds for $r_i$ and $c_j$:
- $r_i \ge \max \{ j \mid (i, j) \text{ is black} \}$
- $c_j \ge \max \{ i \mid (i, j) \text{ is black} \}$

Let $R_{min}[i]$ be this lower bound for row $i$ (0 if no black cells), and $C_{min}[j]$ for column $j$. The minimal configuration $r_i = R_{min}[i], c_j = C_{min}[j]$ is optimal for satisfying white cell constraints because increasing any $r_i$ or $c_j$ only makes the condition $r_i < j$ or $c_j < i$ harder to satisfy (or keeps it false).

For each white cell $(x, y)$, we check if $R_{min}[x] < y$ OR $C_{min}[y] < x$. If this fails for any white cell, it's impossible. Otherwise, it's possible.

Using dictionaries for $R_{min}$ and $C_{min}$ handles the large $N$ efficiently since $M$ is small.
