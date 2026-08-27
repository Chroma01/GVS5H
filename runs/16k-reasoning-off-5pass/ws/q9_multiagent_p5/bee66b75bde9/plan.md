The problem requires finding a grid where each row $r$ has a "cut" at index $R_r$ (cells $1..R_r$ are black, rest white) and each column $c$ has a "cut" at index $C_c$ (cells $1..C_c$ are black, rest white). For any cell $(r, c)$, its color must be black if $c \le R_r$ and white if $c > R_r$. Similarly, it must be black if $r \le C_c$ and white if $r > C_c$. This implies that for every cell $(r, c)$, the condition $c \le R_r \iff r \le C_c$ must hold. This is equivalent to saying $R_r \ge c \iff C_c \ge r$. If we define the set of valid black cells as the region below or to the left of some boundary, the constraints imply that the sequence of row cuts $R_1, R_2, \dots, R_N$ must be non-increasing (since if row $r$ allows column $c$ to be black, row $r+1$ must also allow column $c$ to be black? Wait, let's re-evaluate).

Actually, let's look at the condition: Cell $(r, c)$ is Black $\iff c \le R_r$ AND $r \le C_c$.
If $(r, c)$ is Black, then $(r+1, c)$ must be Black? Not necessarily.
Let's check the logic again.
Row condition: Row $r$ is $B...B$ ($R_r$ times) then $W...W$.
Col condition: Col $c$ is $B...B$ ($C_c$ times) then $W...W$.
Intersection: Cell $(r, c)$ is Black $\iff c \le R_r$ AND $r \le C_c$.
This means the set of Black cells is exactly the intersection of the region $[1, N] \times [1, R_r]$ for each row and $[1, C_c] \times [1, N]$ for each column.
Crucially, if $(r, c)$ is Black, then $(r, c-1)$ is Black (row property) and $(r-1, c)$ is Black (col property).
This implies that the set of Black cells forms a "Young Diagram" shape (or Ferrers diagram) aligned to the top-left.
Specifically, if $(r, c)$ is Black, then $(r, c-1)$ is Black. Thus $R_r \ge c$.
Also if $(r, c)$ is Black, then $(r-1, c)$ is Black. Thus $C_c \ge r$.
More importantly, the sequence of row cut-offs $R_1, R_2, \dots, R_N$ must be non-increasing?
If $(r, c)$ is Black, then $r \le C_c$. Since $C_c$ is fixed for column $c$, if row $r$ has a black cell at $c$, row $r-1$ must also have a black cell at $c$ (because $r-1 < r \le C_c$).
So if $(r, c)$ is Black, $(r-1, c)$ is Black.
This means for a fixed column $c$, the black cells are rows $1, \dots, C_c$.
For a fixed row $r$, the black cells are columns $1, \dots, R_r$.
The condition that the shape is consistent means:
If $c \le R_r$, then $r \le C_c$.
This is equivalent to: $R_r \ge c \implies C_c \ge r$.
Taking the contrapositive: $C_c < r \implies R_r < c$.
This implies that the function $f(r) = R_r$ must be non-increasing?
Let's test: Suppose $R_1 = 5, R_2 = 3$.
Row 1: B B B B B W ...
Row 2: B B B W ...
Col 1: B, B... (ok)
Col 2: B, B... (ok)
Col 3: B, B... (ok)
Col 4: B, W... -> $C_4 = 1$.
Check condition: Is $C_4 \ge 2$? No ($1 < 2$).
Is $R_2 \ge 4$? No ($3 < 4$).
Condition $c \le R_r \iff r \le C_c$.
For $(2, 4)$: $4 \le 3$ is False. $2 \le 1$ is False. Consistent (both White).
For $(1, 4)$: $4 \le 5$ is True. $1 \le 1$ is True. Consistent (both Black).
So $R_1=5, R_2=3$ works.
What if $R_1=3, R_2=5$?
Row 1: B B B W ...
Row 2: B B B B B ...
Col 4: Row 1 is W, Row 2 is B.
Col 4 must be $B...B$ then $W...W$. It cannot have W then B.
So $C_4$ would need to be $\ge 2$ (to cover row 2) but $\le 0$ (to exclude row 1)? Impossible.
Thus, $R_1 \ge R_2 \ge \dots \ge R_N$ is required.
Similarly, $C_1 \ge C_2 \ge \dots \ge C_N$ is required.
And the relationship is $R_r \ge c \iff C_c \ge r$.
This defines a unique valid configuration if we know the "boundary". The boundary is defined by the set of Black cells.
Actually, the constraints on $R_r$ and $C_c$ are fully determined by the requirement that the set of Black cells is a Young Diagram.
Specifically, $R_r$ is the largest $c$ such that $(r, c)$ is Black.
$C_c$ is the largest $r$ such that $(r, c)$ is Black.
The condition $R_1 \ge R_2 \ge \dots \ge R_N$ must hold.
Also, we can derive $R_r$ from the given constraints.
For each given Black cell $(x, y)$, we must have $R_x \ge y$.
For each given White cell $(x, y)$, we must have $R_x < y$ (i.e., $R_x \le y-1$).
So for each row $r$, we have a range $[L_r, U_r]$ for $R_r$.
$L_r = \max(\{y \mid (r, y) \text{ is Black}\} \cup \{0\})$.
$U_r = \min(\{y \mid (r, y) \text{ is White}\} \cup \{N\})$.
If $L_r > U_r$, impossible -> No.
Additionally, we have the monotonicity constraint: $R_1 \ge R_2 \ge \dots \ge R_N$.
We need to check if there exists a sequence $R_1, \dots, R_N$ such that $L_r \le R_r \le U_r$ and $R_1 \ge R_2 \ge \dots \ge R_N$.
This is a standard problem solvable by greedy or two-pass checks.
1. Initialize $R_r = U_r$ for all $r$.
2. Iterate $r$ from 1 to $N$: if $R_r < L_r$, then impossible? No, because $R_r$ is constrained by $R_{r-1}$.
Correct approach:
We need $L_r \le R_r \le U_r$ and $R_r \le R_{r-1}$.
So $R_r \le \min(U_r, R_{r-1})$.
Let's compute the maximum possible valid sequence from top to bottom?
Actually, the constraints are:
$R_r \ge L_r$
$R_r \le U_r$
$R_r \le R_{r-1}$ (for $r>1$)
$R_r \ge R_{r+1}$ (for $r<N$)
Wait, the condition is just $R_1 \ge R_2 \ge \dots \ge R_N$.
So we need to find if there exists a non-increasing sequence in the intervals $[L_r, U_r]$.
Algorithm:
1. Calculate $L_r$ and $U_r$ for all rows $r=1..N$. Initialize $L_r=0, U_r=N$. Update with input.
2. Check if $L_r \le U_r$ for all $r$. If not, return No.
3. We need to find $R_r \in [L_r, U_r]$ such that $R_1 \ge R_2 \ge \dots \ge R_N$.
   This is possible if and only if we can construct such a sequence.
   We can determine the tightest upper bound for each $R_r$ considering the prefix constraints:
   Let $MaxR_r = \min(U_r, MaxR_{r-1})$ with $MaxR_0 = N$.
   Then we must have $MaxR_r \ge L_r$. If $MaxR_r < L_r$, then no solution.
   Wait, is this sufficient?
   Suppose we pick $R_r = MaxR_r$. Then $R_1 \ge R_2 \ge \dots$ is satisfied by construction.
   But we also need $R_r \ge L_r$.
   Is it possible that picking the maximal values forces a violation later?
   No, because if a valid sequence exists, the sequence defined by $R'_r = \min(U_r, R'_{r-1})$ is the "largest" possible non-increasing sequence bounded by $U$.
   However, we also have lower bounds $L$.
   Actually, the condition for existence of a non-increasing sequence $x_i \in [l_i, u_i]$ is:
   $l_i \le u_i$ for all $i$, AND
   $l_i \le \min(u_i, u_{i-1}, \dots, u_1)$? No.
   Let's refine.
   We need $x_1 \ge x_2 \ge \dots \ge x_N$.
   $x_i \le u_i$.
   $x_i \ge l_i$.
   From $x_1 \ge x_2 \ge \dots \ge x_i$, we have $x_i \le x_1 \le u_1$.
   Also $x_i \le u_i$. So $x_i \le \min(u_i, u_{i-1}, \dots, u_1)$. Let this be $U'_i$.
   We must have $l_i \le U'_i$.
   Is this sufficient?
   Suppose $l_i \le U'_i$ for all $i$. Can we construct the sequence?
   Yes. Set $x_i = U'_i$.
   Check if $x_i \ge l_i$: Yes by assumption.
   Check if $x_i \le u_i$: Yes by definition ($U'_i \le u_i$).
   Check if $x_i \ge x_{i+1}$:
   $U'_i = \min(u_i, U'_{i-1})$.
   $U'_{i+1} = \min(u_{i+1}, U'_i)$.
   So $U'_{i+1} \le U'_i$.
   Thus $x_i \ge x_{i+1}$ holds.
   So the condition is simply:
   1. $L_r \le U_r$ for all $r$.
   2. Let $U'_1 = U_1$. For $r=2..N$, $U'_r = \min(U_r, U'_{r-1})$.
   3. Check if $L_r \le U'_r$ for all $r$.
   
   Wait, is there a symmetric constraint from the bottom?
   The condition $R_1 \ge R_2 \ge \dots \ge R_N$ is the only monotonicity constraint on rows.
   Does this ensure the column constraints are satisfied?
   If we find such $R_r$, we can define the grid.
   Then we must verify if the implied column cuts $C_c$ satisfy the column monotonicity $C_1 \ge C_2 \ge \dots \ge C_N$ and the input constraints.
   Actually, if we satisfy the row constraints and the row monotonicity, does the column monotonicity automatically hold?
   The grid is defined by $R_r$.
   $C_c = \max \{ r \mid R_r \ge c \}$.
   If $R$ is non-increasing, then the set $\{ r \mid R_r \ge c \}$ is an interval $[1, k]$. So $C_c = k$.
   Is $C_c$ non-increasing with respect to $c$?
   If $c_1 < c_2$, then $\{ r \mid R_r \ge c_2 \} \subseteq \{ r \mid R_r \ge c_1 \}$.
   So $C_{c_2} \le C_{c_1}$. Yes.
   So checking row monotonicity and row constraints is sufficient.
   
   Wait, we also need to check the column constraints directly?
   The problem statement says "For every column...".
   If we construct the grid based on $R_r$, the column condition is satisfied by definition of $C_c$ derived from $R_r$.
   The only thing is: do the given White/Black cells in columns match?
   Our check $L_r \le R_r \le U_r$ ensures that for every row, the given cells are consistent with $R_r$.
   Since the grid is fully determined by $R_r$, and we ensured every given cell matches $R_r$, the entire grid matches all given cells.
   And since $R$ is non-increasing, the column structure is valid.
   So the algorithm is:
   1. Initialize $L_r = 0, U_r = N$ for all $r \in [1, N]$.
   2. Process inputs:
      - If $(x, y)$ is 'B': $L_x = \max(L_x, y)$.
      - If $(x, y)$ is 'W': $U_x = \min(U_x, y-1)$.
   3. Check $L_r \le U_r$ for all $r$. If not, return No.
   4. Compute $U'_1 = U_1$. For $r=2..N$, $U'_r = \min(U_r, U'_{r-1})$.
   5. Check $L_r \le U'_r$ for all $r$. If not, return No.
   6. Return Yes.

   Complexity: $O(N)$ is too slow since $N \le 10^9$.
   However, $M \le 2 \times 10^5$.
   We only need to check rows that appear in the input.
   Rows not in input have $L_r=0, U_r=N$.
   The sequence $U'_r$ will be constant between updated rows.
   We can collect all unique row indices involved in inputs, sort them, and process intervals.
   Let the sorted unique rows be $r_1 < r_2 < \dots < r_k$.
   We can maintain the current $U'_{prev}$.
   For an interval $[r_i, r_{i+1}-1]$, the $U_r$ is constant (equal to $U_{r_i}$ if $r_i$ was updated, else $N$).
   Actually, simpler:
   Create a list of events for each row.
   Since $N$ is large, we use a map or sort the input by row.
   Let's sort the input lines by $X_i$.
   Iterate through the sorted unique rows.
   Maintain `current_max_U` which is the value of $U'_{r-1}$.
   For the current row $r$:
     $U_r$ is the value from input (or $N$).
     $L_r$ is the value from input (or $0$).
     Check $L_r \le U_r$.
     Update `current_max_U` = $\min(U_r, current\_max\_U)$.
     Check $L_r \le current\_max\_U$.
     Also, we need to handle the gap between $r$ and the next row $r_{next}$.
     For any row $k$ in $(r, r_{next})$, $U_k = N$ (since no input), $L_k = 0$.
     The constraint propagates: $U'_k = \min(N, U'_r) = U'_r$.
     We need $0 \le U'_r$. This is always true since $U'_r \ge 0$.
     So gaps are fine as long as the immediate row constraints are met.
     Wait, what if $U'_r$ becomes very small?
     For rows between $r$ and $r_{next}$, $U'_k = U'_r$.
     We need $L_k \le U'_k$. Since $L_k=0$ and $U'_k \ge 0$, this is always true.
     So we only need to check the rows that have explicit constraints?
     Yes, because for rows without constraints, $L=0, U=N$, and the monotonicity just carries over the upper bound. Since lower bound is 0, it's always satisfiable.
     So we just need to check the rows present in the input.
     Wait, is it possible that a row NOT in the input causes a problem?
     No, because $L=0, U=N$ is the most flexible.
     So the algorithm simplifies to:
     1. Group inputs by row.
     2. Sort unique rows.
     3. Iterate through sorted rows, maintaining `prev_U_prime`.
        For row $r$:
          $U = U_{input}$ (default $N$)
          $L = L_{input}$ (default $0$)
          $U_{prime} = \min(U, prev\_U\_prime)$
          If $L > U_{prime}$, return No.
          $prev\_U\_prime = U_{prime}$
     4. Return Yes.

   Wait, one edge case: $N$ is large, but we only iterate over $M$ rows.
   Is it possible that the "gap" logic is flawed?
   Suppose row $r$ has $U'_r = 2$.
   Row $r+1$ is not in input. $L=0, U=N$.
   $U'_{r+1} = \min(N, 2) = 2$.
   $L_{r+1} = 0 \le 2$. OK.
   So yes, gaps are fine.

   Wait, I missed something. The problem also has column constraints?
   No, the column constraints are automatically satisfied if the row constraints and row monotonicity are satisfied.
   Because the resulting grid is a Young Diagram, which satisfies both row and column properties by definition.
   The only input constraints are the specific cells.
   So the logic holds.

   Let's double check Sample 2.
   N=2, M=2.
   (1, 2) W -> Row 1: $U_1 \le 1$. $L_1=0$.
   (2, 2) B -> Row 2: $L_2 \ge 2$. $U_2=2$.
   Sorted rows: 1, 2.
   Row 1: $U_1=1, L_1=0$. $prev=2$ (initially N). $U'_1 = \min(1, 2) = 1$. Check $0 \le 1$. OK. $prev=1$.
   Row 2: $U_2=2, L_2=2$. $U'_2 = \min(2, 1) = 1$. Check $2 \le 1$. False.
   Output No. Correct.

   Sample 1:
   4 3
   4 1 B -> R4: L>=1
   3 2 W -> R3: U<=1
   1 3 B -> R1: L>=3
   Sorted: 1, 3, 4.
   Init prev=4.
   R1: U=4, L=3. U'=min(4,4)=4. 3<=4 OK. prev=4.
   R3: U=1, L=0. U'=min(1,4)=1. 0<=1 OK. prev=1.
   R4: U=4, L=1. U'=min(4,1)=1. 1<=1 OK. prev=1.
   Output Yes. Correct.

   Sample 3:
   1 1
   1 1 W
   R1: U=0, L=0.
   Init prev=1.
   R1: U'=min(0,1)=0. 0<=0 OK.
   Yes.

   Looks solid.