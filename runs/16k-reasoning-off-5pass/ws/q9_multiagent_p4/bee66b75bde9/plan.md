The problem requires determining if a grid can be colored such that every row has a prefix of black cells followed by white cells, and every column has a prefix of black cells followed by white cells. This structure implies that the boundary between black and white cells in any row $r$ is at some column index $L_r$, and in any column $c$ is at some row index $U_c$. Crucially, for the grid to be valid, these boundaries must satisfy $L_r \leq U_c$ for all $r, c$ where the cell $(r, c)$ is black, and $L_r > U_c$ where it is white. More simply, if we define $L_r$ as the count of black cells in row $r$ and $U_c$ as the count of black cells in column $c$, the condition is equivalent to: for all $r, c$, if $c \leq L_r$ then $U_c \geq r$, and if $c > L_r$ then $U_c < r$. This implies that the set of black cells forms a "Young Tableau" shape (or Ferrers diagram). We can model this as a system of inequalities: $L_r \geq c \iff U_c \geq r$. Given fixed cells, we can derive constraints on $L_r$ and $U_c$. Specifically, if $(r, c)$ is Black, then $L_r \geq c$ and $U_c \geq r$. If $(r, c)$ is White, then $L_r < c$ (so $L_r \leq c-1$) and $U_c < r$ (so $U_c \leq r-1$). We need to find if there exist sequences $L_1, \dots, L_N$ and $U_1, \dots, U_N$ satisfying these and the monotonicity implied by the structure (actually, the structure itself enforces $L_r$ is non-decreasing? No, $L_r$ can vary, but the condition $c \leq L_r \implies U_c \geq r$ must hold for all pairs). Actually, a simpler characterization is: Let $f(r)$ be the number of black cells in row $r$, and $g(c)$ be the number of black cells in column $c$. The condition is equivalent to $f(r) \geq c \iff g(c) \geq r$. This implies $f(r) = \max \{ c \mid g(c) \geq r \}$ and $g(c) = \max \{ r \mid f(r) \geq c \}$. Thus, the sequence $f$ and $g$ must be conjugate partitions. We can solve this by determining the necessary range for each $f(r)$ and $g(c)$ based on the fixed cells, then checking if a valid conjugate pair exists within those ranges. Since $N$ is large but $M$ is small, we only care about rows and columns that appear in the input. We can use a sweep-line or coordinate compression approach, or simply check consistency of the "max possible" and "min possible" boundaries. A robust method: For each row $r$, let $min\_L[r]$ be the minimum possible black count (from forced whites) and $max\_L[r]$ be the maximum (from forced blacks). Similarly for columns. Then check if there exists a valid configuration. However, the constraints are coupled. A better approach: The condition $f(r) \geq c \iff g(c) \geq r$ means that the set of black cells is exactly $\{(r,c) \mid c \leq f(r)\}$. This implies $f(r)$ is non-decreasing? No. But $g(c)$ is non-increasing? No. Wait, if $c \leq f(r)$ then $(r,c)$ is black. If $c > f(r)$ then $(r,c)$ is white.
Let's re-evaluate the structure.
Row $r$: Black in $1..f(r)$, White in $f(r)+1..N$.
Col $c$: Black in $1..g(c)$, White in $g(c)+1..N$.
Consistency: Cell $(r,c)$ is Black $\iff c \leq f(r) \iff r \leq g(c)$.
So we need $c \leq f(r) \iff r \leq g(c)$.
This implies $f(r) = \max \{ c \mid g(c) \geq r \}$ and $g(c) = \max \{ r \mid f(r) \geq c \}$.
This means the function $f$ and $g$ must be conjugate.
Given fixed cells:
If $(r,c)$ is Black: $f(r) \geq c$ and $g(c) \geq r$.
If $(r,c)$ is White: $f(r) < c \implies f(r) \leq c-1$ and $g(c) < r \implies g(c) \leq r-1$.
We need to find if there exist functions $f: \{1..N\} \to \{0..N\}$ and $g: \{1..N\} \to \{0..N\}$ satisfying the fixed constraints and the conjugacy property.
Since $N$ is large, we cannot iterate all rows/cols. But only $M$ constraints exist.
Key insight: The conjugacy property implies that if we plot points $(r, f(r))$, the area under the curve corresponds to the set of black cells. The condition is that the shape defined by $f$ must match the shape defined by $g$.
Actually, we can determine the exact values of $f(r)$ and $g(c)$ if we assume the "tightest" fit.
Let $L_{min}[r]$ be the lower bound for $f(r)$ (from Black cells in row $r$) and $L_{max}[r]$ be the upper bound (from White cells in row $r$).
Similarly $R_{min}[c]$ and $R_{max}[c]$ for $g(c)$.
Initially $L_{min}[r] = 0, L_{max}[r] = N$. Update with constraints.
Then we need to check if there exists a valid $f$ such that $L_{min}[r] \leq f(r) \leq L_{max}[r]$ and the resulting $g$ (derived from $f$) satisfies $R_{min}[c] \leq g(c) \leq R_{max}[c]$.
However, $g(c)$ is determined by $f$. Specifically $g(c) = \max \{ r \mid f(r) \geq c \}$.
This looks like we can binary search or use a greedy strategy.
Actually, there is a simpler necessary and sufficient condition.
Consider the set of "critical" rows and columns.
Let's try to construct the "largest possible" valid grid and "smallest possible" valid grid?
No, the constraints are local.
Let's define $f(r)$ as the number of black cells in row $r$.
From constraints:
For each row $r$, $f(r) \geq \max \{ c \mid (r,c) \text{ is Black} \}$ (if any black exists, else 0).
$f(r) \leq \min \{ c-1 \mid (r,c) \text{ is White} \}$ (if any white exists, else $N$).
Same for columns: $g(c) \geq \max \{ r \mid (r,c) \text{ is Black} \}$, $g(c) \leq \min \{ r-1 \mid (r,c) \text{ is White} \}$.
Let $LB_r = \max(\{0\} \cup \{c \mid (r,c)=B\})$ and $UB_r = \min(\{N\} \cup \{c-1 \mid (r,c)=W\})$.
Let $LB_c = \max(\{0\} \cup \{r \mid (r,c)=B\})$ and $UB_c = \min(\{N\} \cup \{r-1 \mid (r,c)=W\})$.
We need to find $f(r) \in [LB_r, UB_r]$ such that if we define $g(c) = \max \{ r \mid f(r) \geq c \}$, then $g(c) \in [LB_c, UB_c]$.
Note that $g(c)$ is non-increasing with $c$? No, $g(c)$ is the max row index with $\geq c$ blacks. As $c$ increases, the set $\{r \mid f(r) \geq c\}$ shrinks, so $g(c)$ is non-increasing.
Also $f(r)$ does not have to be monotonic. But the conjugacy implies a specific relationship.
Actually, the condition $c \leq f(r) \iff r \leq g(c)$ is symmetric.
We can check consistency by verifying if the intervals allow a valid conjugate pair.
Since $M$ is small, the number of rows/cols with non-trivial bounds is small.
Algorithm:
1. Collect all rows and columns involved. Let $R_{active}$ be rows with $LB_r < UB_r$ or just all rows? No, only rows/cols with constraints matter. But the function is defined on all $1..N$.
2. However, if a row $r$ has no constraints, $LB_r=0, UB_r=N$.
3. The critical observation: The function $f(r)$ must be such that the "staircase" formed by $(r, f(r))$ is consistent with the column constraints.
4. We can try to determine the "tightest" valid $f$.
   Let's try to maximize $f(r)$ subject to column constraints?
   Or simply: Check if $LB_r \leq UB_r$ for all $r, c$. If not, impossible.
   Then, we need to ensure that for every $c$, the required $g(c) \geq LB_c$ and $g(c) \leq UB_c$.
   $g(c) = \max \{ r \mid f(r) \geq c \}$.
   So we need $\max \{ r \mid f(r) \geq c \} \geq LB_c$ and $\max \{ r \mid f(r) \geq c \} \leq UB_c$.
   The second condition implies: for all $r > UB_c$, we must have $f(r) < c$.
   The first condition implies: there exists some $r \geq LB_c$ such that $f(r) \geq c$.
   So for each $c$, we need:
   (A) $\forall r > UB_c, f(r) \leq c-1$.
   (B) $\exists r \geq LB_c, f(r) \geq c$.
   We also have the row constraints: $LB_r \leq f(r) \leq UB_r$.
   So we need to find $f(r)$ satisfying:
   1. $LB_r \leq f(r) \leq UB_r$ for all $r$.
   2. $\forall c, \forall r > UB_c \implies f(r) \leq c-1$.
   3. $\forall c, \exists r \geq LB_c \implies f(r) \geq c$.
   
   Condition 2 can be rewritten: For any $r$, and any $c$ such that $UB_c < r$, we must have $f(r) \leq c-1$.
   This means $f(r) \leq \min \{ c-1 \mid UB_c < r \}$.
   Let $GlobalUB_r = \min(UB_r, \min \{ c-1 \mid UB_c < r \})$.
   If $UB_c < r$ has no solution (i.e., for all $c$, $UB_c \geq r$), then the min is effectively $N$ (or infinity).
   Actually, let's refine:
   From (A): If $r > UB_c$, then $f(r) < c$. So $f(r) \leq c-1$.
   This must hold for ALL $c$ where $UB_c < r$.
   So $f(r) \leq \min_{c: UB_c < r} (c-1)$.
   Let $LimitUB_r = \min(UB_r, \min_{c: UB_c < r} (c-1))$. If the set $\{c: UB_c < r\}$ is empty, the min term is $N$.
   Also, we must have $f(r) \geq LB_r$. So we need $LB_r \leq LimitUB_r$. If not, return No.
   
   Now check condition (B): $\forall c, \exists r \geq LB_c$ such that $f(r) \geq c$.
   We need to be able to choose $f(r)$ large enough.
   The maximum possible value for $f(r)$ is $LimitUB_r$.
   So we need: $\exists r \geq LB_c$ such that $LimitUB_r \geq c$.
   This is equivalent to: $\max_{r \geq LB_c} (LimitUB_r) \geq c$.
   If for any $c$, $\max_{r \geq LB_c} (LimitUB_r) < c$, then impossible.
   
   So the algorithm is:
   1. Parse input, compute $LB_r, UB_r$ for all rows $1..N$ and $LB_c, UB_c$ for all cols $1..N$.
      Note: Only rows/cols appearing in input have non-trivial bounds. Others are $[0, N]$.
      Since $N$ is large, we cannot iterate $1..N$. We must handle ranges.
      The constraints define intervals.
      $LB_r, UB_r$ are defined for specific rows. For others, $0, N$.
      $LB_c, UB_c$ are defined for specific cols. For others, $0, N$.
      
   2. Compute $LimitUB_r$ for all $r$.
      $LimitUB_r = \min(UB_r, \min \{ c-1 \mid UB_c < r \})$.
      The term $\min \{ c-1 \mid UB_c < r \}$ depends on $r$.
      Let $S_c = UB_c$. We need $\min \{ c-1 \mid S_c < r \}$.
      This is a function of $r$. Let $H(r) = \min \{ c-1 \mid UB_c < r \}$.
      If no $c$ satisfies $UB_c < r$, $H(r) = N$.
      Notice that as $r$ increases, the set $\{ c \mid UB_c < r \}$ grows, so $H(r)$ is non-increasing.
      We can compute $H(r)$ efficiently.
      The values of $UB_c$ are fixed. Sort unique values of $UB_c$.
      For a given $r$, we need the smallest $c$ such that $UB_c < r$.
      Actually, we need $\min (c-1)$ over that set.
      Let's collect all pairs $(UB_c, c)$. Sort by $UB_c$.
      We want for a query $r$: $\min \{ c-1 \mid UB_c < r \}$.
      This is equivalent to: consider all $c$ with $UB_c < r$. Take min of $c-1$.
      Since we need this for all $r$ (or at least relevant $r$), and $H(r)$ is non-increasing step function.
      We can compute $H(r)$ for all "critical" $r$ (where $UB_c$ changes).
      Actually, we only need to check the condition $LB_r \leq LimitUB_r$ for all $r$.
      And the condition $\max_{r \geq LB_c} LimitUB_r \geq c$ for all $c$.
      
      Since $N$ is large, we can't iterate all $r$.
      However, the function $LimitUB_r$ is piecewise constant or linear?
      $UB_r$ is constant for most $r$ (only non-zero for input rows).
      $H(r)$ is non-increasing.
      The critical points for $r$ are the $UB_c$ values.
      Let's collect all $UB_c$ values. Sort them: $v_1 < v_2 < \dots < v_k$.
      For $r \in (v_i, v_{i+1}]$, the set $\{ c \mid UB_c < r \}$ is constant? No.
      $UB_c < r$. If $r$ increases, more $c$'s satisfy the condition.
      The set of $c$'s is $\{ c \mid UB_c \leq r-1 \}$.
      So as $r$ increases, we add $c$'s where $UB_c = r-1$.
      So $H(r) = \min ( H(r-1), \min \{ c-1 \mid UB_c = r-1 \} )$.
      We can compute $H(r)$ for all $r$ that are "active" or boundaries.
      Actually, we only need to check $LB_r \leq LimitUB_r$.
      $LB_r$ is non-zero only for input rows.
      So we only need to check $r$ where $LB_r > 0$ (input rows).
      For these $r$, we need $LimitUB_r \geq LB_r$.
      $LimitUB_r = \min(UB_r, H(r))$.
      So we need $H(r) \geq LB_r$ (since $UB_r \geq LB_r$ by definition).
      $H(r) = \min \{ c-1 \mid UB_c < r \}$.
      So we need: For every row $r$ with $LB_r > 0$, $\min \{ c-1 \mid UB_c < r \} \geq LB_r$.
      This is equivalent to: For every row $r$ with $LB_r > 0$, and for every $c$ such that $UB_c < r$, we must have $c-1 \geq LB_r \implies c \geq LB_r + 1$.
      Contrapositive: If $c \leq LB_r$, then $UB_c \geq r$.
      This is a direct consistency check!
      Check: For every input row $r$ and input col $c$:
      If $(r,c)$ is Black: $LB_r \geq c$ and $UB_c \geq r$. (Already checked by input validity? Input says if Black, then $c \leq f(r)$ and $r \leq g(c)$. So $LB_r \geq c$ and $UB_c \geq r$ is guaranteed by construction of $LB, UB$).
      Wait, $LB_r$ is derived from Black cells in row $r$. So $LB_r \geq c$ is true if $(r,c)$ is Black.
      $UB_c$ is derived from White cells in col $c$. So $UB_c \geq r$ is true if $(r,c)$ is Black (since if it were White, $UB_c < r$).
      So for Black cells, the basic constraints are satisfied.
      The issue arises from White cells and cross-constraints.
      The condition derived: $\forall r, c: c \leq LB_r \implies UB_c \geq r$.
      Let's verify this logic.
      We need $H(r) \geq LB_r$.
      $H(r) = \min \{ c-1 \mid UB_c < r \}$.
      Condition: $\min \{ c-1 \mid UB_c < r \} \geq LB_r$.
      This means for all $c$ with $UB_c < r$, we have $c-1 \geq LB_r \implies c \geq LB_r + 1$.
      So if $c \leq LB_r$, then it is NOT the case that $UB_c < r$, i.e., $UB_c \geq r$.
      So yes: $\forall r, c: c \leq LB_r \implies UB_c \geq r$.
      This must hold for ALL $r, c$.
      Since $LB_r$ and $UB_c$ are defined based on input, we can check this.
      But $r, c$ range up to $N$. We can't iterate all.
      However, $LB_r > 0$ only for rows with Black cells.
      $UB_c < r$ only for cols with White cells (or $UB_c$ small).
      Actually, $UB_c$ is defined as $\min(\{N\} \cup \{r-1 \mid (r,c)=W\})$.
      So $UB_c < r$ implies there is a White cell at $(r', c)$ with $r' \leq r$.
      Specifically, if $UB_c < r$, then there exists some $r' \leq UB_c < r$ such that $(r', c)$ is White.
      So the condition "For all $c$ with $UB_c < r$, $c \geq LB_r + 1$" can be rewritten:
      If there exists a White cell at $(r', c)$ with $r' < r$, then we must have $c \geq LB_r + 1$.
      Wait, $UB_c$ is the max row index of black cells in col $c$. So $UB_c < r$ means row $r$ is White in col $c$ (or above).
      Actually, $UB_c$ is the number of black cells in col $c$. So rows $1..UB_c$ are Black, $UB_c+1..N$ are White.
      So $UB_c < r$ means $(r,c)$ is White.
      So the condition is: For any row $r$ and any column $c$ such that $(r,c)$ is White, we must have $c \geq LB_r + 1$.
      $LB_r$ is the number of black cells in row $r$.
      So: If $(r,c)$ is White, then $c > LB_r$.
      This is exactly the row condition! "Leftmost $LB_r$ are Black, rest White".
      So if $(r,c)$ is White, $c$ must be $> LB_r$.
      This is tautologically true by definition of $LB_r$?
      $LB_r = \max \{ c \mid (r,c)=B \}$.
      If $(r,c)$ is White, then $c$ cannot be $\leq LB_r$?
      If $c \leq LB_r$, then by definition of $LB_r$, $(r,c)$ must be Black (since $LB_r$ is the max index of a Black cell, all $1..LB_r$ are Black).
      So if $(r,c)$ is White, then $c > LB_r$.
      So the condition $c \leq LB_r \implies UB_c \geq r$ is automatically satisfied for the rows/cols involved in the input?
      Wait, $UB_c$ is defined similarly.
      The condition we derived was $LimitUB_r \geq LB_r$.
      $LimitUB_r = \min(UB_r, \min \{ c-1 \mid UB_c < r \})$.
      The term $\min \{ c-1 \mid UB_c < r \}$ is the constraint from columns.
      $UB_c < r$ means $(r,c)$ is White.
      So we need: For all $r, c$ such that $(r,c)$ is White, $c-1 \geq LB_r \implies c \geq LB_r + 1$.
      This is just the row consistency.
      So $LimitUB_r = UB_r$?
      No. $UB_r$ is the max possible black count in row $r$.
      $UB_c$ is the max possible black count in col $c$.
      The constraint is: If $(r,c)$ is White, then $c > LB_r$. (Row constraint).
      AND if $(r,c)$ is White, then $r > LB_c$? No.
      Let's re-evaluate the conjugacy check.
      We need $f(r) \in [LB_r, UB_r]$ and $g(c) \in [LB_c, UB_c]$ and $f, g$ conjugate.
      The condition for existence of such $f, g$ is:
      1. $LB_r \leq UB_r$ for all $r$.
      2. $LB_c \leq UB_c$ for all $c$.
      3. For all $r, c$: if $c \leq LB_r$ then $r \leq UB_c$. (From $f(r) \geq c \implies g(c) \geq r$).
         Since $f(r) \geq LB_r$, if $c \leq LB_r$, then $f(r) \geq c$, so we need $g(c) \geq r$.
         Since $g(c) \leq UB_c$, we need $UB_c \geq r$.
         So: $c \leq LB_r \implies UB_c \geq r$.
      4. For all $r, c$: if $r > UB_c$ then $c > LB_r$. (From $g(c) < r \implies f(r) < c$).
         If $r > UB_c$, then $g(c) < r$. We need $f(r) < c$.
         Since $f(r) \geq LB_r$, we need $LB_r < c \implies c \geq LB_r + 1$.
         So: $r > UB_c \implies c \geq LB_r + 1$.
      
      These are the two main conditions to check.
      Condition 3: For all $r, c$, if $c \leq LB_r$ then $UB_c \geq r$.
      Condition 4: For all $r, c$, if $r > UB_c$ then $c \geq LB_r + 1$.
      
      We can check these efficiently.
      Condition 3: Iterate over all rows $r$ where $LB_r > 0$. For each such $r$, we need $UB_c \geq r$ for all $c \leq LB_r$.
      This means $\min_{c \leq LB_r} UB_c \geq r$.
      Since $UB_c$ is defined by input, we can precompute prefix minimums of $UB_c$.
      Let $PUB_k = \min \{ UB_c \mid 1 \leq c \leq k \}$.
      Then we need $PUB_{LB_r} \geq r$ for all $r$ with $LB_r > 0$.
      (If $LB_r = 0$, condition is vacuous).
      
      Condition 4: For all $c$, if $r > UB_c$ then $c \geq LB_r + 1$.
      This is equivalent to: For all $r, c$, if $c \leq LB_r$ then $r \leq UB_c$. (Same as Cond 3).
      Wait, Cond 4 is: $r > UB_c \implies c \geq LB_r + 1$.
      Contrapositive: $c \leq LB_r \implies r \leq UB_c$.
      Yes, Cond 3 and Cond 4 are the same statement!
      So we only need to check: For all $r, c$, $c \leq LB_r \implies UB_c \geq r$.
      Which is equivalent to: For all $r$, $\min_{c \leq LB_r} UB_c \geq r$.
      
      Is that sufficient?
      We also need to ensure that we can pick $f(r)$ and $g(c)$ such that they are conjugate.
      The condition $c \leq f(r) \iff r \leq g(c)$ is satisfied if $f(r) \in [LB_r, UB_r]$ and $g(c) \in [LB_c, UB_c]$ and the boundary condition holds.
      But we also need $f(r)$ to be consistent with $g(c)$.
      Actually, the condition $c \leq LB_r \implies UB_c \geq r$ ensures that the "forced" black cells don't conflict with "forced" white cells in a way that breaks the Young Tableau shape.
      Is there any other constraint?
      What about the "gaps"?
      Suppose $LB_r = 2, UB_r = 4$. $LB_c = 2, UB_c = 4$.
      We need to pick $f(r), g(c)$.
      The condition $c \leq LB_r \implies UB_c \geq r$ ensures that if we are forced to have black up to $c$, the column allows it.
      But do we need to check if the intervals allow a valid conjugate pair?
      Yes. The condition $c \leq LB_r \implies UB_c \geq r$ is necessary.
      Is it sufficient?
      Consider $N=2$.
      Row 1: $LB_1=1, UB_1=1$. (Must be 1 black).
      Row 2: $LB_2=0, UB_2=0$. (Must be 0 black).
      Col 1: $LB_1=1, UB_1=1$.
      Col 2: $LB_2=0, UB_2=0$.
      Check Cond: $c \leq LB_r \implies UB_c \geq r$.
      $r=1, LB_1=1$. $c=1 \leq 1 \implies UB_1 \geq 1$ (True).
      $r=2, LB_2=0$. Vacuous.
      So Cond holds.
      Can we form grid?
      Row 1: B W. Row 2: W W.
      Col 1: B W (1 black). Col 2: W W (0 black).
      Matches $LB, UB$. Yes.
      
      Another case:
      $N=2$.
      Row 1: $LB_1=0, UB_1=2$.
      Row 2: $LB_2=2, UB_2=2$.
      Col 1: $LB_1=2, UB_1=2$.
      Col 2: $LB_2=2, UB_2=2$.
      Check Cond:
      $r=1, LB_1=0$. Vacuous.
      $r=2, LB_2=2$. $c=1 \leq 2 \implies UB_1 \geq 2$. $UB_1=2$. OK.
      $c=2 \leq 2 \implies UB_2 \geq 2$. $UB_2=2$. OK.
      So Cond holds.
      But can we form grid?
      Row 2 must have 2 blacks: B B.
      Row 1 must have 0..2 blacks.
      Col 1 must have 2 blacks: B B.
      Col 2 must have 2 blacks: B B.
      So grid must be:
      B B
      B B
      Row 1 has 2 blacks. $LB_1=0, UB_1=2$. OK.
      Row 2 has 2 blacks. $LB_2=2, UB_2=2$. OK.
      Col 1 has 2 blacks. $LB_1=2, UB_1=2$. OK.
      Col 2 has 2 blacks. $LB_2=2, UB_2=2$. OK.
      Yes.
      
      Is there a case where Cond holds but no solution?
      Maybe if the intervals are too tight?
      Actually, the condition $c \leq LB_r \implies UB_c \geq r$ is necessary and sufficient for the existence of a valid grid given the bounds?
      Wait, we also need $LB_c \leq UB_c$ and $LB_r \leq UB_r$.
      And we need to ensure that we can choose $f(r)$ such that the resulting $g(c)$ falls in $[LB_c, UB_c]$.
      The condition $c \leq LB_r \implies UB_c \geq r$ ensures that the "lower bound" of $f$ is compatible with the "upper bound" of $g$.
      What about "upper bound" of $f$ and "lower bound" of $g$?
      Symmetry: The problem is symmetric for rows and cols.
      So we also need: $r \leq LB_c \implies UB_r \geq c$.
      (Swap roles of $r$ and $c$).
      Let's check this.
      Condition A: $c \leq LB_r \implies UB_c \geq r$.
      Condition B: $r \leq LB_c \implies UB_r \geq c$.
      Are these both needed?
      Yes, because $LB$ and $UB$ are defined independently for rows and cols.
      So the algorithm is:
      1. Compute $LB_r, UB_r$ for all $r$.
      2. Compute $LB_c, UB_c$ for all $c$.
      3. Check $LB_r \leq UB_r$ for all $r$. If not, No.
      4. Check $LB_c \leq UB_c$ for all $c$. If not, No.
      5. Check Condition A: For all $r$, if $LB_r > 0$, then $\min_{c \leq LB_r} UB_c \geq r$.
         (Use prefix min of $UB_c$).
      6. Check Condition B: For all $c$, if $LB_c > 0$, then $\min_{r \leq LB_c} UB_r \geq c$.
         (Use prefix min of $UB_r$).
      
      If all pass, Yes.
      
      Complexity:
      $M \leq 2 \cdot 10^5$.
      Number of active rows/cols $\leq M$.
      We can use coordinate compression or just sort the unique $LB_r, UB_c$ values.
      Actually, we only need to check $r$ where $LB_r > 0$. There are at most $M$ such rows.
      For each such $r$, we need $\min_{c \leq LB_r} UB_c$.
      Since $LB_r$ can be up to $N$, we cannot iterate $c$.
      But we only care about $c$ that appear in the input (where $UB_c$ is defined).
      For $c$ not in input, $UB_c = N$.
      So $\min_{c \leq K} UB_c = \min( \min_{c \in Input, c \leq K} UB_c, N )$.
      So we can precompute the prefix minimums of $UB_c$ for the sorted unique column indices present in input.
      Let $Cols$ be sorted unique columns with constraints.
      Build an array $PUB$ where $PUB[i] = \min(UB_{Cols[i]}, PUB[i-1])$.
      For a query $K = LB_r$, find the largest index $i$ such that $Cols[i] \leq K$.
      Then the min is $PUB[i]$ (if $i$ exists, else $N$).
      This can be done with binary search (bisect_right).
      Same for Condition B (using rows).
      
      Total time: $O(M \log M)$.
      
      Edge cases: $N$ large, $M$ small.
      $LB_r, UB_c$ can be 0.
      If $LB_r = 0$, condition A is vacuous.
      If $LB_r > N$, impossible (but input constraints say $X_i, Y_i \leq N$, so $LB_r \leq N$).
      
      Implementation details:
      - Read N, M.
      - Store constraints in dictionaries/maps for rows and cols.
      - Initialize $LB_r=0, UB_r=N$ for all.
      - Update with input.
      - Collect all rows with $LB_r > 0$ and all cols with $LB_c > 0$.
      - Sort unique columns, build prefix min of $UB_c$.
      - Sort unique rows, build prefix min of $UB_r$.
      - Iterate and check.