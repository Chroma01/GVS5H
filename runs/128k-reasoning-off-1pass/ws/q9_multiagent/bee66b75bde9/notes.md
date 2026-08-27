
## ideation
**Core Difficulty**:
The problem asks if a binary grid can be completed such that rows and columns are "prefixes" of black cells. This structure is equivalent to saying the set of black cells forms a **Young Tableau** (or Ferrers diagram) shape: if cell $(r, c)$ is black, then all cells $(r', c')$ with $r' \le r$ and $c' \le c$ must also be black. Conversely, if $(r, c)$ is white, then all cells $(r', c')$ with $r' \ge r$ and $c' \ge c$ must be white.

The constraints given are specific cells colored Black (B) or White (W).
- A 'B' at $(x, y)$ implies that row $x$ must have at least $y$ black cells, and column $y$ must have at least $x$ black cells.
- A 'W' at $(x, y)$ implies that row $x$ must have at most $y-1$ black cells, and column $y$ must have at most $x-1$ black cells.

**Candidate Approaches**:
1.  **Constraint Propagation / Interval Intersection**:
    - For each row $i$, determine the minimum required black prefix length ($min\_row[i]$) from all 'B' cells in that row.
    - For each row $i$, determine the maximum allowed black prefix length ($max\_row[i]$) from all 'W' cells in that row.
    - Similarly for columns $j$: $min\_col[j]$ and $max\_col[j]$.
    - Check for immediate contradictions: $min\_row[i] > max\_row[i]$ or $min\_col[j] > max\_col[j]$.
    - **Crucial Step**: The row constraints and column constraints are coupled. If we fix the row prefix lengths $r_1, r_2, \dots, r_N$, then the column prefix lengths $c_1, c_2, \dots, c_N$ are determined by $c_j = \max \{ r_i \mid i \le j \}$. We need to check if there exists a sequence $r_1, \dots, r_N$ such that:
        1. $min\_row[i] \le r_i \le max\_row[i]$ for all $i$.
        2. Let $c_j = \max_{1 \le i \le j} r_i$. Then $min\_col[j] \le c_j \le max\_col[j]$ for all $j$.
    
    This can be solved by iterating through rows and maintaining the current maximum prefix length seen so far (which dictates the column constraints). Since $N$ is up to $10^9$, we cannot iterate all rows. However, $M$ is small ($2 \times 10^5$). The constraints only change at specific coordinates. We can coordinate compress or simply process the constraints in sorted order.
    
    Actually, a simpler greedy approach works:
    - We need to choose $r_i$ for each row. To satisfy column constraints easily, we might want $r_i$ to be as small as possible, but we must respect $min\_row[i]$.
    - However, increasing $r_i$ helps satisfy $min\_col[j]$ for $j \ge i$ but hurts $max\_col[j]$.
    - Let's define the necessary condition more strictly. The condition "if $(r, c)$ is B then $(r', c')$ is B for $r' \le r, c' \le c$" is equivalent to: The boundary between black and white cells is a non-increasing function of the column index (or non-decreasing function of row index). Specifically, let $f(c)$ be the largest row index $r$ such that $(r, c)$ is black. Then $f(c)$ must be non-increasing? No.
    - Let's re-evaluate the shape.
      Row $i$ has black cells $1 \dots r_i$.
      Col $j$ has black cells $1 \dots c_j$.
      Consistency requires: $(i, j)$ is black $\iff i \le r_j$ AND $j \le c_i$? No.
      $(i, j)$ is black $\iff i \le r_i$ (definition) AND $j \le c_j$ (definition)? No.
      The condition is: $(i, j)$ is black $\iff i \le r_i$ is false.
      Correct logic: $(i, j)$ is black if and only if $j \le r_i$.
      Also $(i, j)$ is black if and only if $i \le c_j$.
      Therefore, we must have: $j \le r_i \iff i \le c_j$.
      This implies $r_i = \max \{ j \mid i \le c_j \}$ and $c_j = \max \{ i \mid j \le r_i \}$.
      Essentially, the sequence $r_1, r_2, \dots, r_N$ must be non-decreasing? No.
      If $r_i$ is the number of black cells in row $i$.
      If $r_i = k$, then $(i, k)$ is black. This implies column $k$ has at least $i$ black cells, so $c_k \ge i$.
      If $r_{i+1} = k$, then $(i+1, k)$ is black $\implies c_k \ge i+1$.
      So if $r_{i+1} \ge r_i$, no immediate contradiction.
      What if $r_{i+1} < r_i$? Say $r_i = 5, r_{i+1} = 3$.
      Then $(i, 4)$ is black $\implies c_4 \ge i$.
      $(i+1, 4)$ is white (since $4 > 3$) $\implies c_4 < i+1 \implies c_4 \le i$.
      So $c_4 = i$. This is consistent.
      Wait, the standard property of Young Tableaux (English notation) is that row lengths are non-increasing ($r_1 \ge r_2 \ge \dots$).
      Let's check Sample 1:
      4x4.
      Row 1: B at 3 $\implies r_1 \ge 3$. W at ? No W in row 1.
      Row 2: No info.
      Row 3: W at 2 $\implies r_3 \le 1$. B at ? No B in row 3 except implied? Input: (3,2) is W.
      Row 4: B at 1 $\implies r_4 \ge 1$.
      Constraints:
      $r_1 \ge 3, r_3 \le 1, r_4 \ge 1$.
      Columns:
      Col 1: B at 4 $\implies c_1 \ge 4$.
      Col 2: W at 3 $\implies c_2 \le 2$.
      Col 3: B at 1 $\implies c_3 \ge 1$.
      
      If $c_1 \ge 4$, then $c_1=4$ (since max N=4).
      If $c_1=4$, then row 1 must have at least 1 black cell (ok), row 2 at least 1, row 3 at least 1, row 4 at least 1.
      Check Row 3: $r_3 \le 1$. Since $c_1=4 \implies (3,1)$ is black. So $r_3 \ge 1$. Thus $r_3=1$.
      Check Col 2: $c_2 \le 2$.
      Since $r_3=1$, $(3,2)$ is white (consistent with input).
      Since $c_1=4$, $(1,1), (2,1), (3,1), (4,1)$ are black.
      We need to pick $r_1, r_2, r_4$.
      $r_1 \ge 3$.
      $r_4 \ge 1$.
      $c_2 = \max(r_1, r_2, r_3, r_4)$ restricted to cols $\ge 2$? No.
      $c_j = \max \{ i \mid r_i \ge j \}$.
      We need $c_2 \le 2$.
      $c_2 = \max \{ i \mid r_i \ge 2 \}$.
      We know $r_1 \ge 3 \ge 2$, so $1 \in \{i \mid r_i \ge 2\}$.
      If $r_2 \ge 2$, then $c_2 \ge 2$. If $r_2 < 2$, $c_2$ could be 1.
      But we also have $c_1 \ge 4$. $c_1 = \max \{ i \mid r_i \ge 1 \}$. Since $r_3=1$, $c_1 \ge 3$. Input says $c_1 \ge 4$. So we need some $r_i \ge 1$ for $i=4$. Indeed $r_4 \ge 1$.
      Is it possible to have $r_1=3, r_2=1, r_3=1, r_4=1$?
      Then $c_1 = \max(1,2,3,4) = 4$. (OK, $\ge 4$).
      $c_2 = \max \{ i \mid r_i \ge 2 \} = 1$. (OK, $\le 2$).
      $c_3 = \max \{ i \mid r_i \ge 3 \} = 1$. (OK, $\ge 1$).
      This works. Output Yes.

      So the condition is: Find a sequence $r_1, \dots, r_N$ such that:
      1. $L_i \le r_i \le R_i$ for all $i$.
      2. Let $c_j = \max \{ i \mid r_i \ge j \}$. Then $A_j \le c_j \le B_j$ for all $j$.
      
      Note that $c_j$ is a non-increasing function of $j$. Also $r_i$ is non-decreasing? No.
      If $r_i$ is arbitrary, $c_j$ is well defined.
      However, note that if $r_i \ge j$, then for any $k < i$, do we know anything? No.
      But observe the structure: $c_j$ is the largest row index containing a black cell in column $j$.
      The condition "row $i$ has prefix $r_i$" means cells $(i, 1)..(i, r_i)$ are black.
      The condition "col $j$ has prefix $c_j$" means cells $(1, j)..(c_j, j)$ are black.
      Intersection: $(i, j)$ is black $\iff j \le r_i \iff i \le c_j$.
      This implies $r_i = \max \{ j \mid i \le c_j \}$ and $c_j = \max \{ i \mid j \le r_i \}$.
      From $i \le c_j \iff j \le r_i$, we can deduce properties of $r$ and $c$.
      Specifically, if $i_1 < i_2$ and $j_1 < j_2$:
      If $i_2 \le c_{j_1}$, then $j_1 \le r_{i_2}$.
      This doesn't force monotonicity of $r_i$ directly, but let's look at the relation.
      $c_j$ is non-increasing in $j$.
      $r_i$ is non-decreasing in $i$?
      Suppose $r_i = 5$. Then $(i, 5)$ is black $\implies i \le c_5$.
      Suppose $r_{i+1} = 3$. Then $(i+1, 5)$ is white $\implies i+1 > c_5 \implies c_5 \le i$.
      Contradiction ($i \le c_5 \le i \implies c_5=i$).
      So if $r_i=5, r_{i+1}=3$, then $c_5=i$.
      Then $(i, 5)$ is black, $(i+1, 5)$ is white. Consistent.
      So $r_i$ does NOT need to be non-decreasing.
      However, $c_j$ MUST be non-increasing.
      Proof: If $j_1 < j_2$. If $(i, j_2)$ is black, then $(i, j_1)$ is black (since $j_1 < j_2$).
      So the set of rows having black cells in col $j_2$ is a subset of those in col $j_1$.
      Thus $\max \{ i \mid (i, j_2) \text{ black} \} \le \max \{ i \mid (i, j_1) \text{ black} \}$.
      So $c_{j_2} \le c_{j_1}$.
      
      Algorithm Refined:
      We need to find $r_1, \dots, r_N$ satisfying row bounds and resulting $c_j$ satisfying col bounds.
      Since $N$ is large, we cannot iterate $i$.
      But we only have $M$ constraints.
      The critical values for $r_i$ are the $X$ coordinates of the input points.
      Actually, we can determine the *tightest possible* valid configuration.
      To satisfy $c_j \ge A_j$, we need enough rows $i$ to have $r_i \ge j$.
      To satisfy $c_j \le B_j$, we need that for all $i > B_j$, $r_i < j$.
      
      Let's try to construct the "maximal" valid $r$ sequence and "minimal" valid $r$ sequence?
      Or simply check consistency using the constraints directly.
      
      Key Insight:
      The condition is equivalent to: For every pair of rows $i_1 < i_2$ and columns $j_1 < j_2$, the configuration of the four cells $(i_1, j_1), (i_1, j_2), (i_2, j_1), (i_2, j_2)$ must not contain the pattern:
      Top-Right (Black), Bottom-Left (White).
      i.e., $(i_1, j_2)=B$ and $(i_2, j_1)=W$ is forbidden.
      Because if $(i_1, j_2)$ is B, then row $i_1$ has at least $j_2$ blacks. So $r_{i_1} \ge j_2$.
      If $(i_2, j_1)$ is W, then row $i_2$ has at most $j_1-1$ blacks. So $r_{i_2} \le j_1-1 < j_2$.
      But $i_1 < i_2$.
      Does this create a contradiction with column properties?
      $c_{j_2} \ge i_1$ (since $(i_1, j_2)$ is B).
      $c_{j_1} \le i_2-1$ (since $(i_2, j_1)$ is W).
      We know $j_1 < j_2$. Since $c$ is non-increasing, $c_{j_1} \ge c_{j_2}$.
      So $i_2-1 \ge c_{j_1} \ge c_{j_2} \ge i_1$.
      This is $i_2-1 \ge i_1 \implies i_2 > i_1$. Which is true.
      So the local 2x2 check is necessary but is it sufficient?
      Actually, the condition "no B at $(i, j)$ and W at $(i', j')$ with $i < i'$ and $j > j'$" is exactly the condition that the boundary is a Young Tableau.
      Wait, if $(i, j)$ is B and $(i', j')$ is W with $i < i'$ and $j > j'$, is it always invalid?
      Yes. Because $(i, j)$ B $\implies r_i \ge j$.
      $(i', j')$ W $\implies r_{i'} \le j'-1$.
      Since $j > j'$, $r_i \ge j > j' \ge r_{i'} + 1 > r_{i'}$.
      So $r_i > r_{i'}$.
      Now consider column $j$. $r_i \ge j \implies (i, j)$ is B $\implies c_j \ge i$.
      Consider column $j'$. $r_{i'} \le j'-1 \implies (i', j')$ is W $\implies c_{j'} \le i'-1$.
      We have $j > j'$. Since $c$ is non-increasing, $c_j \le c_{j'}$.
      So $i \le c_j \le c_{j'} \le i'-1 < i'$.
      So $i < i'$. This is consistent with our assumption.
      Wait, I didn't find a contradiction.
      Let's re-read the definition.
      Row $i$: $1..r_i$ Black.
      Row $i'$: $1..r_{i'}$ Black.
      If $r_i > r_{i'}$, then row $i$ extends further right than row $i'$.
      Is this allowed?
      Example:
      Row 1: B B B (r=3)
      Row 2: B B   (r=2)
      Col 1: B B (c=2)
      Col 2: B B (c=2)
      Col 3: B W (c=1)
      Check cols:
      Col 1: 2 blacks. OK.
      Col 2: 2 blacks. OK.
      Col 3: 1 black. OK.
      Check rows:
      Row 1: 3 blacks. OK.
      Row 2: 2 blacks. OK.
      This is a valid Young Tableau.
      Here $r_1=3, r_2=2$. $r_1 > r_2$.
      So $r_i$ does NOT need to be non-decreasing.
      My previous deduction about $c_j$ being non-increasing was correct.
      $c_1=2, c_2=2, c_3=1$. Non-increasing.
      
      So the only constraints are:
      1. $L_i \le r_i \le R_i$.
      2. $c_j = \max \{ i \mid r_i \ge j \}$ satisfies $A_j \le c_j \le B_j$.
      
      How to check existence of such $r$?
      We can try to construct the "most permissive" $r$ sequence.
      To satisfy $c_j \ge A_j$, we need at least $A_j$ rows with $r_i \ge j$.
      To satisfy $c_j \le B_j$, we need that for all $i > B_j$, $r_i < j$.
      
      Let's define $req\_rows[j] = A_j$. We need at least $A_j$ rows with $r_i \ge j$.
      Also $forbid\_rows[j] = B_j$. We need no rows $> B_j$ to have $r_i \ge j$.
      
      This looks like we can determine the necessary $r_i$ values.
      Let $min\_r[i]$ be the minimum possible value for $r_i$ and $max\_r[i]$ be the maximum possible value.
      Initialize $min\_r[i] = L_i, max\_r[i] = R_i$.
      
      Constraint from columns:
      If $c_j \ge A_j$, then there must be at least $A_j$ indices $i$ such that $r_i \ge j$.
      If $c_j \le B_j$, then for all $i > B_j$, $r_i < j \implies r_i \le j-1$.
      So for each $j$, we have an upper bound on $r_i$ for $i > B_j$: $r_i \le j-1$.
      And a lower bound on the count of $r_i \ge j$.
      
      This suggests a greedy strategy or a flow-like check, but simpler:
      The condition $c_j \le B_j$ implies $r_i \le j-1$ for all $i > B_j$.
      This gives us a hard upper bound on $r_i$ based on column constraints.
      Let $U_i = \min(R_i, \max \{ j-1 \mid i > B_j \})$. If no such $j$, $U_i = R_i$.
      Actually, $U_i = \min_{j: B_j < i} (j-1)$. If the set is empty, $U_i = R_i$.
      Similarly, $c_j \ge A_j$ implies we need enough rows.
      But we also have the row lower bounds $L_i$.
      So we must have $L_i \le U_i$ for all $i$. If not, return No.
      
      Now we need to check if we can pick $r_i \in [L_i, U_i]$ such that for all $j$, the count of $i$ with $r_i \ge j$ is between $A_j$ and $B_j$.
      Wait, $c_j$ is exactly the count of $i$ such that $r_i \ge j$.
      So we need: $A_j \le \text{count}(\{i \mid r_i \ge j\}) \le B_j$.
      
      This is a known problem. Can we satisfy these count constraints?
      The constraints on counts are monotonic.
      $\text{count}(j) \ge \text{count}(j+1)$.
      We need $A_j \le \text{count}(j) \le B_j$.
      And we know $A_j$ and $B_j$ must be non-increasing?
      Input constraints: $A_j$ comes from 'B' cells, $B_j$ from 'W' cells.
      If we have a 'B' at $(i, j)$, then $c_j \ge i$.
      If we have a 'W' at $(i, j)$, then $c_j \le i-1$.
      Are $A_j$ and $B_j$ guaranteed to be non-increasing?
      Not necessarily by input, but if the solution exists, the resulting $c_j$ must be non-increasing.
      So if $A_j > A_{j+1}$, that's fine (we just need count $\ge A_j$).
      But if $B_j < B_{j+1}$, that's impossible because $c_j \ge c_{j+1}$, so we need $B_j \ge c_j \ge c_{j+1} \ge A_{j+1}$.
      Actually, the condition $c_j \le B_j$ and $c_{j+1} \le B_{j+1}$ with $c_j \ge c_{j+1}$ implies we need $B_j \ge c_j \ge c_{j+1}$. It doesn't force $B_j \ge B_{j+1}$, but if $B_j < B_{j+1}$, we could still have $c_j = c_{j+1} = B_j$.
      However, we must ensure that the required counts are consistent with the row ranges.
      
      Algorithm:
      1. Initialize $L_i = 0, R_i = N$ for all $i$.
      2. Process 'B' at $(x, y)$: $L_x = \max(L_x, y)$, $A_y = \max(A_y, x)$.
      3. Process 'W' at $(x, y)$: $R_x = \min(R_x, y-1)$, $B_y = \min(B_y, x-1)$.
      4. Check $L_i \le R_i$ for all $i$. If not, No.
      5. Check $A_j \le B_j$ for all $j$. If not, No.
      6. Refine $R_i$ using column upper bounds:
         For each $j$, if $B_j < N$, then for all $i > B_j$, $r_i \le j-1$.
         So $R_i = \min(R_i, j-1)$ for all $i > B_j$.
         Since $N$ is large, we can't iterate all $i$.
         Notice that $R_i$ becomes $\min(R_i, \min_{j: B_j < i} (j-1))$.
         Let $limit[i] = \min \{ j-1 \mid B_j < i \}$. If no such $j$, $\infty$.
         We can compute this efficiently by sorting the constraints or using a sweep.
         Actually, $limit[i]$ is non-increasing with $i$?
         As $i$ increases, the set $\{ j \mid B_j < i \}$ grows, so the minimum can only decrease.
         So $limit[i]$ is non-increasing.
         We can compute $limit[i]$ for relevant $i$ (those where $L_i$ or $R_i$ changes, or simply all $i$ if we compress).
         But wait, we only care about $i$ where $L_i$ is defined? No, $L_i$ is 0 for most.
         The constraint $r_i \le limit[i]$ might cut off the lower bound $L_i$.
         So check $L_i \le limit[i]$ for all $i$.
         Since $limit[i]$ is step-wise constant (changes at $i = B_j + 1$), we only need to check $i$ in the set $\{1, \dots, N\}$.
         But $N$ is large. However, $limit[i]$ only changes at specific points.
         The values of $i$ that matter are those where $L_i > 0$ (from 'B' inputs) or where the bound $limit[i]$ drops below $L_i$.
         Actually, simpler:
         The condition $r_i \le j-1$ for $i > B_j$ means that for any $i$, $r_i \le \min_{j: B_j < i} (j-1)$.
         Let $V_i = \min_{j: B_j < i} (j-1)$.
         We need $L_i \le V_i$.
         $V_i$ is a non-increasing function of $i$.
         $V_i = \min(V_{i-1}, \text{new constraint from } j \text{ s.t. } B_j = i-1)$.
         We can compute $V_i$ for all $i$ that are endpoints of intervals?
         Actually, we can just check if there exists ANY $i$ such that $L_i > V_i$.
         Since $L_i$ is non-zero only for $i \in \{X_k\}$, and $V_i$ is non-increasing, we can check specific points.
         But $V_i$ might drop between $X_k$'s.
         However, if $L_i = 0$ for some $i$, $0 \le V_i$ is always true.
         So we only need to check $i \in \{X_k\}$.
         For a specific $x \in \{X_k\}$, we need $x \le \min_{j: B_j < x} (j-1)$.
         This is equivalent to: For all $j$ such that $B_j < x$, we must have $x \le j-1 \implies j \ge x+1$.
         So if there exists any $j$ with $B_j < x$ and $j < x+1$ (i.e., $j \le x$), then contradiction.
         Wait, $B_j < x \implies$ rows $> B_j$ must have $r \le j-1$. If $x > B_j$, then row $x$ must have $r_x \le j-1$.
         So we need $L_x \le j-1$ for all $j$ with $B_j < x$.
         So $L_x \le \min \{ j-1 \mid B_j < x \}$.
         This can be checked by iterating over all $j$? $M$ is $2 \cdot 10^5$.
         We can iterate over all $j$ where $B_j$ is defined.
         For each $j$, if $B_j < x$, update constraint.
         Better: For each $x \in \{X_k\}$, check if $\exists j$ such that $B_j < x$ and $j-1 < L_x$.
         This is equivalent to: $\min \{ j \mid B_j < x \} \le x$? No.
         We need $L_x \le j-1 \iff j \ge L_x + 1$.
         So we need: For all $j$ with $B_j < x$, we must have $j \ge L_x + 1$.
         Contradiction if $\exists j$ such that $B_j < x$ and $j < L_x + 1$.
         i.e., $j \le L_x$.
         So check: Is there any $j$ such that $B_j < x$ and $j \le L_x$?
         If yes, return No.
         This check is $O(M^2)$ if naive. We can optimize.
         Sort queries by $x$. Sort constraints by $j$.
         Or simply: For each $x$, we need $\min \{ j \mid B_j < x \} \ge L_x + 1$.
         Let $min\_j\_for\_less\_than[x] = \min \{ j \mid B_j < x \}$.
         Since $B_j$ is fixed, we can precompute this.
         Actually, $min\_j\_for\_less\_than[x]$ is non-increasing with $x$.
         We can compute it by iterating $x$ from 1 to $N$? No, $N$ large.
         But we only care about $x \in \{X_k\}$.
         Let's collect all $j$ such that $B_j$ is defined. Let these be $J_{list}$.
         For a given $x$, we need $\min \{ j \in J_{list} \mid B_j < x \} \ge L_x + 1$.
         If the set is empty, condition holds.
         We can sort $J_{list}$ by $j$. Then for a given $x$, we want the smallest $j$ in the list such that $B_j < x$.
         This can be done with binary search or two pointers if we sort $x$'s.
         
      7. Now we have valid ranges $[L_i, R'_i]$ where $R'_i = \min(R_i, \text{column upper bound})$.
         We also have column requirements $A_j \le c_j \le B_j$.
         We need to check if we can choose $r_i \in [L_i, R'_i]$ such that count($r_i \ge j$) $\in [A_j, B_j]$.
         This is the core check.
         Let $cnt_j = \text{number of } i \text{ such that } r_i \ge j$.
         We need $A_j \le cnt_j \le B_j$.
         Also $cnt_j$ is non-increasing.
         And $cnt_j = \sum_{i=1}^N [r_i \ge j]$.
         
         We can try to construct the "maximal" $cnt_j$ and "minimal" $cnt_j$.
         Maximal $cnt_j$: Set $r_i = R'_i$ for all $i$. Compute $cnt_j^{max}$. Check $cnt_j^{max} \le B_j$.
         Minimal $cnt_j$: Set $r_i = L_i$ for all $i$. Compute $cnt_j^{min}$. Check $cnt_j^{min} \ge A_j$.
         Is it sufficient to check these extremes?
         Not necessarily. The function $cnt_j$ is determined by the specific values of $r_i$.
         However, note that $cnt_j$ is the number of $r_i \ge j$.
         If we increase some $r_i$, $cnt_j$ increases for all $j \le r_i$.
         We need to satisfy lower bounds $A_j$ and upper bounds $B_j$.
         This looks like a feasibility problem for a non-increasing sequence.
         But we have freedom to choose $r_i$ in $[L_i, R'_i]$.
         Actually, we can determine the tightest possible $cnt_j$ range.
         Let $min\_cnt_j$ be the minimum possible value of $cnt_j$ given the constraints.
         To minimize $cnt_j$, we should pick $r_i$ as small as possible, i.e., $r_i = L_i$.
         Then $min\_cnt_j = \text{count}(\{i \mid L_i \ge j\})$.
         We must have $min\_cnt_j \ge A_j$.
         To maximize $cnt_j$, pick $r_i = R'_i$.
         $max\_cnt_j = \text{count}(\{i \mid R'_i \ge j\})$.
         We must have $max\_cnt_j \le B_j$.
         
         Is it true that if $min\_cnt_j \ge A_j$ and $max\_cnt_j \le B_j$, then a valid assignment exists?
         Not exactly. We need a single assignment $r_i$ that satisfies ALL $j$ simultaneously.
         However, notice that $cnt_j$ is determined by the set of $r_i$'s.
         If we choose $r_i = L_i$, we get a specific sequence $cnt_j^{L}$. If this satisfies $A_j \le cnt_j^{L} \le B_j$, we are good.
         If we choose $r_i = R'_i$, we get $cnt_j^{R}$. If $A_j \le cnt_j^{R} \le B_j$, good.
         But we might need to adjust $r_i$ upwards from $L_i$ to satisfy $A_j$ (if $cnt_j^L < A_j$) or downwards from $R'_i$ to satisfy $B_j$ (if $cnt_j^R > B_j$).
         Wait, if $cnt_j^L < A_j$, we need to increase some $r_i$'s. Increasing $r_i$ increases $cnt_k$ for all $k \le r_i$.
         This might violate $B_k$ for some $k$.
         Similarly, if $cnt_j^R > B_j$, we need to decrease some $r_i$'s.
         
         Actually, there is a simpler necessary and sufficient condition.
         The condition is equivalent to: For all $j$, $A_j \le \text{count}(L_i \ge j)$? No.
         Let's reconsider the structure.
         The condition $c_j \ge A_j$ means we need at least $A_j$ rows with $r_i \ge j$.
         The condition $c_j \le B_j$ means we need at most $B_j$ rows with $r_i \ge j$.
         Let $k_j = \text{count}(\{i \mid L_i \ge j\})$. This is the minimum possible count if we set $r_i=L_i$.
         If $k_j < A_j$, we MUST increase some $r_i$'s that are currently $< j$ to be $\ge j$.
         Specifically, we need to pick at least $A_j - k_j$ rows from those with $L_i < j$ and set them to $\ge j$.
         But setting a row to $\ge j$ increases the count for all $k \le j$.
         This suggests we should process $j$ from $N$ down to 1?
         Or use a greedy approach:
         We need to select a set of rows $S_j$ of size $c_j$ such that $S_j \supseteq S_{j+1}$ and $|S_j| \in [A_j, B_j]$.
         Also for each $i$, if $i \in S_j$, then $r_i \ge j$.
         This implies $r_i = \max \{ j \mid i \in S_j \}$.
         We need $L_i \le r_i \le R'_i$.
         So $i \in S_j \implies L_i \le \max \{ k \mid i \in S_k \}$.
         Actually, simpler: $i \in S_j \iff r_i \ge j$.
         So we need to find a sequence of sets $S_1 \supseteq S_2 \supseteq \dots \supseteq S_N$ such that $|S_j| \in [A_j, B_j]$ and for all $i$, if $i \in S_j$ then $L_i \le \max \{ k \mid i \in S_k \}$?
         No, the condition is $L_i \le r_i$ and $r_i \le R'_i$.
         $r_i = \max \{ j \mid i \in S_j \}$.
         So we need $L_i \le \max \{ j \mid i \in S_j \} \le R'_i$.
         This means:
         1. There exists some $j \ge L_i$ such that $i \in S_j$. (i.e., $i \in \bigcup_{j \ge L_i} S_j$)
         2. For all $j > R'_i$, $i \notin S_j$. (i.e., $i \notin \bigcup_{j > R'_i} S_j$)
         
         So we need to construct nested sets $S_j$ with sizes in $[A_j, B_j]$ such that:
         - Each $i$ is present in $S_j$ for some $j \in [L_i, R'_i]$?
           No, $r_i$ is the MAX $j$ such that $i \in S_j$.
           So $i$ must be in $S_{r_i}$, and not in $S_{r_i+1}$.
           So $i$ must be in $S_j$ for all $j \le r_i$.
           Thus $i \in S_j \iff j \le r_i$.
           So for each $i$, the set of $j$'s where $i \in S_j$ is exactly $\{1, 2, \dots, r_i\}$.
           This implies $i \in S_j \iff r_i \ge j$.
           So the condition is simply: Can we choose $r_i \in [L_i, R'_i]$ such that $\text{count}(\{i \mid r_i \ge j\}) \in [A_j, B_j]$?
           
         This is exactly the condition we were analyzing.
         Let $f(j) = \text{count}(\{i \mid r_i \ge j\})$.
         We need $A_j \le f(j) \le B_j$.
         We know $f(j)$ is non-increasing.
         We can construct the "minimal" valid $f(j)$ and "maximal" valid $f(j)$.
         Minimal $f(j)$: Try to make $f(j)$ as small as possible.
         This means setting $r_i$ as small as possible, i.e., $r_i = L_i$.
         Let $f_{min}(j) = \text{count}(\{i \mid L_i \ge j\})$.
         If $f_{min}(j) < A_j$ for any $j$, we MUST increase some $r_i$'s.
         To minimize the impact on other $k$, we should increase $r_i$ only when necessary.
         Actually, if $f_{min}(j) < A_j$, we need to pick $A_j - f_{min}(j)$ rows from those with $L_i < j$ and set their $r_i$ to at least $j$.
         To keep future counts low, we should pick rows with smallest $L_i$? No, we need to satisfy $A_k$ for $k < j$ too.
         Actually, the constraints $A_j$ are lower bounds.
         If $f_{min}(j) < A_j$, we have a deficit. We need to boost $f(j)$.
         Boosting $f(j)$ by increasing $r_i$ also boosts $f(k)$ for all $k < j$.
         So if we have a deficit at $j$, it helps with deficits at $k < j$.
         So we should process $j$ from $N$ down to 1?
         Or 1 to N?
         If we process $j$ from $N$ down to 1:
         At $j$, we have current count $cur$. If $cur < A_j$, we need to add $A_j - cur$ rows.
         Which rows to add? Rows that can be increased to $\ge j$.
         To minimize harm to $B_k$ (upper bounds), we should add rows that are "least useful" for higher $k$?
         But we are going downwards. Higher $k$ are already processed.
         Wait, increasing $r_i$ affects $f(k)$ for $k \le r_i$.
         If we increase $r_i$ to $j$, it affects $f(1), \dots, f(j)$.
         If we process $j$ from $N$ down to 1:
         We need $f(j) \ge A_j$.
         We can increase $r_i$ for some $i$. This increases $f(j)$ and all $f(k)$ for $k < j$.
         So increasing $r_i$ at step $j$ helps satisfy $A_k$ for $k < j$.
         So we should greedily increase $r_i$ to satisfy $A_j$.
         Which $i$? Any $i$ with $L_i < j$ and $R'_i \ge j$.
         To minimize violation of $B_k$ (upper bounds), we should pick $i$ that are "least likely" to violate $B$?
         Actually, increasing $r_i$ increases $f(k)$ for all $k \le j$.
         If we have a deficit at $j$, we must increase some $r_i$.
         Does it matter which $i$?
         Suppose we increase $r_i$ to $j$. Then $f(k)$ increases by 1 for all $k \le j$.
         This is good for $A_k$.
         But bad for $B_k$.
         However, if $B_k$ is violated, we would have detected it when processing $k$ (if we check upper bounds too).
         But we need to satisfy both.
         Actually, the condition is:
         There exists $r_i$ such that $A_j \le \sum [r_i \ge j] \le B_j$.
         This is equivalent to:
         $\sum_{i} [L_i \ge j] \le B_j$ is NOT required.
         We need to find IF there exists.
         
         Let's use the property that $f(j)$ must be non-increasing.
         The minimal possible $f(j)$ is $f_{min}(j) = \text{count}(L_i \ge j)$.
         The maximal possible $f(j)$ is $f_{max}(j) = \text{count}(R'_i \ge j)$.
         We need $A_j \le f(j) \le B_j$.
         Is it true that if $f_{min}(j) \le B_j$ and $f_{max}(j) \ge A_j$ for all $j$, then a solution exists?
         Not necessarily, because $f(j)$ must be non-increasing and consistent with the same set of $r_i$.
         However, note that $f_{min}(j)$ is non-increasing, $f_{max}(j)$ is non-increasing.
         If $f_{min}(j) \le B_j$ and $f_{max}(j) \ge A_j$, does there exist a non-increasing $f(j)$ such that $f_{min}(j) \le f(j) \le f_{max}(j)$ and $A_j \le f(j) \le B_j$?
         Yes, we can take $f(j) = \max(A_j, f_{min}(j))$? No, must be $\le f_{max}(j)$.
         Actually, we can construct $f(j)$ as follows:
         Start with $g(j) = f_{min}(j)$.
         If $g(j) < A_j$, we must increase $g(j)$. But increasing $g(j)$ might violate $g(j) \le g(j-1)$.
         So we set $g(j) = \max(A_j, g(j+1))$? No.
         The standard way to check feasibility of such sequences is:
         Let $lower(j) = \max(A_j, lower(j+1))$.
         Let $upper(j) = \min(B_j, upper(j+1))$.
         Then check if $lower(j) \le upper(j)$ for all $j$.
         But this is for constructing a sequence $f(j)$ directly.
         We also need $f(j)$ to be realizable by some $r_i \in [L_i, R'_i]$.
         Realizability condition: $f(j) - f(j+1)$ is the number of $r_i = j$.
         So we need $0 \le f(j) - f(j+1) \le \text{count}(L_i \le j \le R'_i)$.
         Let $cap(j) = \text{count}(L_i \le j \le R'_i)$.
         We need to find non-increasing $f(j)$ such that:
         1. $A_j \le f(j) \le B_j$.
         2. $f(j) - f(j+1) \le cap(j)$.
         3. $f(N+1) = 0$.
         
         This can be solved greedily from $N$ down to 1.
         $f(N+1) = 0$.
         For $j = N$ down to 1:
           Max possible $f(j)$ is $B_j$.
           Min possible $f(j)$ is $\max(A_j, f(j+1))$.
           Also, we need $f(j) - f(j+1) \le cap(j) \implies f(j) \le f(j+1) + cap(j)$.
           So $f(j) \le \min(B_j, f(j+1) + cap(j))$.
           And $f(j) \ge \max(A_j, f(j+1))$.
           If $\max(A_j, f(j+1)) > \min(B_j, f(j+1) + cap(j))$, then impossible.
           Otherwise, we can choose any value in the range.
           To maximize chances for lower $j$, we should choose the largest possible $f(j)$?
           Because $f(j-1) \ge f(j)$. Larger $f(j)$ makes the lower bound for $f(j-1)$ larger, which is harder?
           Wait, $f(j-1) \ge f(j)$. If $f(j)$ is large, $f(j-1)$ must be large.
           But we also have $f(j-1) \le f(j) + cap(j-1)$.
           If $f(j)$ is large, the upper bound for $f(j-1)$ is larger, which is easier.
           So we should choose $f(j)$ as large as possible.
           Set $f(j) = \min(B_j, f(j+1) + cap(j))$.
           Then check if $f(j) \ge A_j$ and $f(j) \ge f(j+1)$.
           If $f(j) < A_j$ or $f(j) < f(j+1)$, then impossible.
           (Note: $f(j) \ge f(j+1)$ is guaranteed if $f(j+1) + cap(j) \ge f(j+1)$, which is true since $cap \ge 0$. But we need to check $f(j) \ge A_j$).
           
         So the algorithm:
         1. Compute $L_i, R_i$ from inputs.
         2. Compute $A_j, B_j$ from inputs.
         3. Refine $R_i$ with column upper bounds ($R_i = \min(R_i, j-1)$ for $i > B_j$).
         4. Compute $cap(j) = \text{count}(i \mid L_i \le j \le R'_i)$.
         5. Greedy from $j=N$ down to 1:
            $f(j) = \min(B_j, f(j+1) + cap(j))$ (with $f(N+1)=0$).
            If $f(j) < A_j$ or $f(j) < f(j+1)$, return No.
         6. If loop finishes, return Yes.

## worker: Implement the Python solution using coordinate com
The solution implements the derived algorithm:
1.  **Constraint Parsing**: Reads input and initializes row/column constraints ($L, R, A, B$).
2.  **Row Refinement**: Computes the effective upper bound $U[i]$ for each row based on column 'W' constraints. This is done efficiently by sorting critical row indices and processing events.
3.  **Consistency Check**: Verifies $L[i] \le R'[i]$ for all rows.
4.  **Greedy Interval Check**:
    *   Identifies critical column indices where constraints ($A, B, cap$) change.
    *   Computes $cap(j)$ (number of valid rows covering column $j$) using a sweep-line over row intervals.
    *   Processes column intervals backwards from $N$ to $0$.
    *   Maintains the maximum possible valid prefix count $f(j)$ satisfying $f(j) \le B[j]$ and $f(j) \le f(j+1) + cap(j)$.
    *   Checks if $f(j) \ge A[j]$ and $f(j) \ge f(j+1)$ hold.
5.  **Output**: Prints "Yes" or "No".

Complexity: $O(M \log M)$ due to sorting critical coordinates and events. Space $O(M)$. Handles $N \le 10^9$ via coordinate compression.
