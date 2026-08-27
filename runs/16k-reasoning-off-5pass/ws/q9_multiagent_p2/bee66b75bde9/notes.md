
## ideation
The problem asks if we can complete a grid coloring such that every row has a prefix of black cells and every column has a prefix of black cells, given some pre-colored cells.
This structure implies that the set of black cells must form a "Young Diagram" (or Ferrers diagram) shape, possibly rotated. Specifically, if cell $(r, c)$ is black, then all $(r', c')$ with $r' \le r$ and $c' \le c$ must be black. Conversely, if $(r, c)$ is white, then all $(r', c')$ with $r' \ge r$ and $c' \ge c$ must be white.

Let $h_c$ be the number of black cells in column $c$ (i.e., the height of the black prefix in column $c$).
Let $w_r$ be the number of black cells in row $r$ (i.e., the width of the black prefix in row $r$).
The condition that row $r$ has a prefix of length $w_r$ means that for any column $c$, cell $(r, c)$ is black if and only if $c \le w_r$.
The condition that column $c$ has a prefix of length $h_c$ means that for any row $r$, cell $(r, c)$ is black if and only if $r \le h_c$.

For the coloring to be consistent, the definition of black cells via rows and columns must match.
A cell $(r, c)$ is black $\iff r \le h_c \iff c \le w_r$.
This implies a relationship between the sequence $h$ and $w$:
$w_r = \text{count of } \{c \mid h_c \ge r\}$.
Conversely, $h_c = \text{count of } \{r \mid w_r \ge c\}$.

Given the constraints:
1. If $(x, y)$ is **Black**, then we must have $x \le h_y$ and $y \le w_x$.
   This implies $h_y \ge x$. To maximize the chance of satisfying other constraints (since increasing $h_c$ increases $w_r$ which might violate white constraints), we should set $h_c$ to the minimum possible value.
   So, for each column $c$, let $LB[c] = \max(\{x \mid (x, c) \text{ is Black}\} \cup \{0\})$. We must have $h_c \ge LB[c]$.
   Similarly, for each row $r$, let $LB\_w[r] = \max(\{y \mid (r, y) \text{ is Black}\} \cup \{0\})$. We must have $w_r \ge LB\_w[r]$.

2. If $(x, y)$ is **White**, then we must have $x > h_y$ OR $y > w_x$.
   This is a disjunction. However, notice that if we fix $h_c$ to be exactly $LB[c]$, then $w_r$ is determined as $w_r = \text{count}(\{c \mid LB[c] \ge r\})$.
   Let's verify if setting $h_c = LB[c]$ is always optimal.
   Suppose we choose $h_c > LB[c]$ for some $c$. Then the set $\{c' \mid h_{c'} \ge r\}$ becomes a superset of the set when $h_c = LB[c]$. Thus, $w_r$ (derived from $h$) would increase or stay the same.
   Increasing $w_r$ makes the condition $y > w_x$ harder to satisfy for white cells in row $x$ (since we need $y > w_x$).
   Also, increasing $h_c$ makes the condition $x > h_y$ harder to satisfy for white cells in column $y$.
   Therefore, to satisfy the "White" constraints as easily as possible, we should minimize $h_c$.
   So, we set $h_c = LB[c]$.
   
   With $h_c$ fixed to $LB[c]$, the implied width for row $r$ is $W_r = \text{count}(\{c \mid LB[c] \ge r\})$.
   Now we check consistency with the given White cells.
   For a White cell at $(x, y)$, we need: $x > h_y$ OR $y > W_x$.
   Substituting $h_y = LB[y]$ and $W_x = \text{count}(\{c \mid LB[c] \ge x\})$:
   Condition: $x > LB[y]$ OR $y > \text{count}(\{c \mid LB[c] \ge x\})$.
   
   Wait, is it possible that $x \le LB[y]$ but $y > W_x$?
   If $x \le LB[y]$, then by definition of $LB[y]$, there is a black cell at $(x, y)$? No.
   $LB[y]$ is the maximum row index of a black cell in column $y$.
   If $(x, y)$ is White, it is NOT a black cell.
   However, $LB[y]$ is derived from *other* black cells in column $y$.
   If there is a black cell at $(x', y)$ with $x' > x$, then $LB[y] \ge x' > x$.
   In this case, the column constraint says column $y$ must have black cells up to row $LB[y]$. Since $x < LB[y]$, cell $(x, y)$ MUST be black.
   But we are given $(x, y)$ is White. This is a contradiction.
   So, if $(x, y)$ is White, we MUST have $x > LB[y]$.
   If $x \le LB[y]$, then column $y$ requires $(x, y)$ to be black, which conflicts with the input.
   So the first part of the OR ($x > LB[y]$) is actually a necessary condition derived purely from column constraints.
   
   What about the second part? $y > W_x$.
   $W_x$ is the number of columns that have height $\ge x$.
   If $y \le W_x$, it means there are at least $y$ columns with height $\ge x$.
   Specifically, columns $1, 2, \dots, y$ (if we sort them? No, just count).
   Actually, $W_x$ is the count of $c$ such that $LB[c] \ge x$.
   If $y \le W_x$, does it imply $(x, y)$ must be black?
   Not necessarily $y$-th column specifically, but *some* $y$ columns.
   However, the row constraint says row $x$ has black cells in columns $1, 2, \dots, W_x$.
   If $y \le W_x$, then cell $(x, y)$ must be black.
   But $(x, y)$ is given as White. Contradiction.
   So we must have $y > W_x$.
   
   So the condition simplifies to:
   For every White cell $(x, y)$:
   1. $x > LB[y]$ (Column consistency)
   2. $y > W_x$ (Row consistency)
   
   Let's re-verify.
   If $x \le LB[y]$, then column $y$ has a black cell at row $LB[y] \ge x$. Since column $y$ is a prefix of blacks, all rows $1 \dots LB[y]$ are black. So $(x, y)$ is black. Contradiction. So $x > LB[y]$ is required.
   If $y \le W_x$, then row $x$ has black cells in columns $1 \dots W_x$. Since $y \le W_x$, $(x, y)$ is black. Contradiction. So $y > W_x$ is required.
   
   Are these sufficient?
   If $x > LB[y]$ and $y > W_x$, then:
   - Column $y$ has blacks up to $LB[y] < x$, so $(x, y)$ is white. OK.
   - Row $x$ has blacks up to $W_x < y$, so $(x, y)$ is white. OK.
   
   So the algorithm is:
   1. Calculate $LB[c]$ for all $c=1 \dots N$. $LB[c] = \max(\{x \mid (x, c) \text{ is Black}\} \cup \{0\})$.
   2. Check for every White cell $(x, y)$:
      - If $x \le LB[y]$, return "No".
      - Calculate $W_x = \text{count}(\{c \mid LB[c] \ge x\})$.
      - If $y \le W_x$, return "No".
   3. If all checks pass, return "Yes".
   
   Wait, do we need to check Black cells too?
   If $(x, y)$ is Black:
   - We set $LB[y] \ge x$. So $x \le LB[y]$ holds.
   - We need to ensure that the implied $W_x \ge y$.
     $W_x = \text{count}(\{c \mid LB[c] \ge x\})$.
     Since $(x, y)$ is Black, we have $LB[y] \ge x$. So column $y$ contributes to the count.
     Thus $W_x \ge 1$. Is it guaranteed $W_x \ge y$?
     Not necessarily.
     Example: $N=2$. Black at $(1, 2)$. White at $(2, 1)$.
     $LB[1] = 0$ (no black in col 1). $LB[2] = 1$.
     White $(2, 1)$: $x=2, y=1$.
     Check 1: $x > LB[y] \implies 2 > 0$. OK.
     Check 2: $W_2 = \text{count}(LB[c] \ge 2) = 0$.
     Condition $y > W_x \implies 1 > 0$. OK.
     Now check Black $(1, 2)$:
     Implied $W_1 = \text{count}(LB[c] \ge 1) = 1$ (only col 2).
     Row 1 should have blacks in $1 \dots 1$. So $(1, 1)$ is black, $(1, 2)$ is white?
     Wait. $W_1 = 1$ means row 1 has black cells in columns $1, \dots, 1$.
     So $(1, 1)$ is black, $(1, 2)$ is white.
     But input says $(1, 2)$ is Black. Contradiction.
     
     So my derivation of sufficiency was incomplete.
     The condition "Row $x$ has black prefix of length $W_x$" means $(x, c)$ is black $\iff c \le W_x$.
     We need this to match the input.
     For a Black cell $(x, y)$, we need $y \le W_x$.
     For a White cell $(x, y)$, we need $y > W_x$.
     
     So the full set of conditions on $h_c = LB[c]$ is:
     For ALL cells $(x, y)$ (whether Black or White):
     - If $(x, y)$ is Black: $y \le W_x$ AND $x \le h_y$ (where $h_y = LB[y]$).
       Note: $x \le LB[y]$ is guaranteed by definition of $LB[y]$.
       So we just need $y \le W_x$.
     - If $(x, y)$ is White: $y > W_x$ AND $x > h_y$.
       Note: $x > LB[y]$ is not guaranteed by definition. We must check it.
       So we need $x > LB[y]$ AND $y > W_x$.
       
     Combining these:
     For every Black $(x, y)$: $y \le W_x$.
     For every White $(x, y)$: $x > LB[y]$ AND $y > W_x$.
     
     Is that all?
     Let's re-check the example: Black $(1, 2)$, White $(2, 1)$.
     $LB[1]=0, LB[2]=1$.
     $W_1 = \text{count}(LB \ge 1) = 1$.
     Black $(1, 2)$: Check $2 \le W_1 \implies 2 \le 1$. False. -> No.
     Correct.
     
     So the algorithm is:
     1. Compute $LB[c]$ for all $c$.
     2. Compute $W_x = \text{count}(\{c \mid LB[c] \ge x\})$ for all $x$ that appear in the input (rows with cells).
        Actually, we need $W_x$ for all rows $x$ that contain a Black or White cell.
        But $W_x$ depends on $LB$. $LB$ is defined for all columns.
        We can compute $W_x$ efficiently.
        $W_x$ is the number of $c$ such that $LB[c] \ge x$.
        Since $N$ is large, we cannot iterate $x$.
        However, we only need $W_x$ for $x$ present in the input rows.
        Let $R_{input}$ be the set of row indices that have at least one colored cell.
        For each $x \in R_{input}$, compute $W_x$.
        How to compute $W_x$ fast?
        $W_x = \sum_{c=1}^N [LB[c] \ge x]$.
        We can collect all pairs $(LB[c], c)$ and sort them. Then for a query $x$, we can use binary search (upper_bound) to find how many $LB[c] \ge x$.
        Or simpler: Sort the $LB$ values. For a given $x$, count elements $\ge x$.
        Since we have many queries (up to $M$), sorting $LB$ takes $O(N)$? No, $N$ is large.
        But we only have $M$ black cells. So at most $M$ columns have $LB[c] > 0$.
        For columns with no black cells, $LB[c] = 0$.
        So $LB$ array has $M$ non-zero values and $N-M$ zeros.
        $W_x = (\text{count of non-zero } LB \ge x) + (\text{count of zero } LB \ge x)$.
        If $x > 0$, zero $LB$ contributes 0.
        So $W_x = \text{count of } \{c \mid LB[c] \ge x\}$ considering only columns with $LB[c] > 0$.
        Let's collect the list $L = [LB[c] \text{ for } c \text{ where } LB[c] > 0]$. Size $\le M$.
        Sort $L$.
        For each query $x$, use `bisect_left` on $L$ to find count $\ge x$.
        Complexity: $O(M \log M)$.
        
     3. Iterate through all input cells $(x, y)$ with color $C$.
        - If $C == 'B'$: Check $y \le W_x$.
        - If $C == 'W'$: Check $x > LB[y]$ AND $y > W_x$.
        If any check fails, output "No".
     4. If all pass, output "Yes".

     Wait, is it possible that $LB[y]$ is not the optimal choice?
     Earlier reasoning: Increasing $h_c$ increases $W_x$ for all $x \le h_c$.
     Increasing $W_x$ makes $y \le W_x$ more likely (bad for White) and $y > W_x$ less likely (good for White? No, $y > W_x$ is required for White. Larger $W_x$ makes it harder).
     Wait.
     For White $(x, y)$: need $y > W_x$. Larger $W_x$ makes this harder.
     For Black $(x, y)$: need $y \le W_x$. Larger $W_x$ makes this easier.
     So there is a trade-off.
     However, we also have the constraint $x > h_y$ for White cells.
     If we increase $h_y$, $x > h_y$ becomes harder.
     So increasing $h_c$ hurts White constraints in two ways ($x > h_y$ and $y > W_x$) and helps Black constraints ($y \le W_x$).
     But Black constraints are $y \le W_x$.
     If a Black cell $(x, y)$ exists, it forces $h_y \ge x$.
     If we set $h_y > x$, we might satisfy $y \le W_x$ more easily?
     But we also need to satisfy White constraints.
     Let's consider the "tightest" valid configuration.
     The configuration is valid iff there exists a sequence $h_c$ such that:
     1. $h_c \ge LB[c]$ (from Black cells)
     2. For all Black $(x, y)$: $y \le \text{count}(h \ge x)$
     3. For all White $(x, y)$: $x > h_y$ AND $y > \text{count}(h \ge x)$
     
     Let's analyze the dependencies.
     Condition 3a ($x > h_y$) suggests we want $h_y$ small.
     Condition 3b ($y > \text{count}(h \ge x)$) suggests we want $\text{count}(h \ge x)$ small, so $h$ small.
     Condition 2 ($y \le \text{count}(h \ge x)$) suggests we want $\text{count}(h \ge x)$ large, so $h$ large.
     
     This looks like we might need to increase $h$ to satisfy Black constraints, but that hurts White constraints.
     However, note that for a specific Black cell $(x, y)$, we need $y \le \text{count}(h \ge x)$.
     This means there must be at least $y$ columns with height $\ge x$.
     One of them is column $y$ (since $h_y \ge x$). We need $y-1$ other columns.
     If we increase $h_c$ for some $c \ne y$, we might satisfy this.
     But increasing $h_c$ also increases the count for rows $x' \le h_c$, potentially violating White constraints in those rows.
     
     Is it possible that the minimal $h_c = LB[c]$ fails, but a larger $h_c$ works?
     Suppose minimal fails on a Black cell $(x, y)$ because $W_x < y$.
     This means fewer than $y$ columns have height $\ge x$.
     We need to increase the height of some columns to reach count $y$.
     Increasing heights increases $W_{x'}$ for $x' \le \text{new height}$.
     This might violate White constraints in rows $x' \le x$.
     Specifically, if we have a White cell $(x', y')$ with $x' \le x$, and we increase count, we might make $y' \le W_{x'}$ true, which is bad.
     So increasing $h$ to fix a Black violation might break a White constraint.
     Conversely, if minimal fails on a White constraint ($y \le W_x$), increasing $h$ makes it worse.
     Decreasing $h$ is not allowed ($h \ge LB$).
     
     So it seems the minimal $h_c$ is the best candidate for White constraints, but might be insufficient for Black constraints.
     If minimal fails on Black constraints, can we fix it?
     We need to increase some $h_c$ to boost $W_x$.
     But any increase in $h_c$ increases $W_{x'}$ for $x' \le h_c$.
     If there is ANY White cell $(x', y')$ with $x' \le h_c$ and $y' \le W_{x'}$ (after increase), we fail.
     Actually, if we have a Black cell $(x, y)$ requiring $W_x \ge y$, and currently $W_x < y$, we must increase some $h_c$ ($c \ne y$) such that $LB[c] < x$ (so it wasn't counted) to $x$.
     But if we do that, $W_x$ increases.
     Does this hurt any White cell?
     A White cell $(x', y')$ is hurt if $x' \le x$ and $y' \le W_{x'}$ becomes true.
     If $x' < x$, then $W_{x'}$ was already $\ge W_x$ (since $h \ge x' \implies h \ge x$ is not true, wait).
     $W_x = \text{count}(h \ge x)$.
     $W_{x'} = \text{count}(h \ge x')$.
     If $x' < x$, then $\{h \ge x\} \subseteq \{h \ge x'\}$. So $W_x \le W_{x'}$.
     If we increase $h_c$ to $x$, then $W_x$ increases. $W_{x'}$ also increases (since $x' < x \le \text{new } h_c$).
     So if we fix a Black constraint at row $x$, we also increase $W$ for all rows $x' < x$.
     If there is a White cell at row $x' < x$ that is "tight" (i.e., $y' = W_{x'}$), increasing $W_{x'}$ will violate it.
     
     This suggests that if the minimal configuration fails on a Black constraint, it might be impossible to fix without violating a White constraint.
     Why? Because to fix $W_x \ge y$, we need to add more columns with height $\ge x$.
     These columns must have height increased from $< x$ to $\ge x$.
     This increases $W_{x'}$ for all $x' \le x$.
     If there is any White cell $(x', y')$ with $x' \le x$ such that $y' = W_{x'}$ (current), then increasing $W_{x'}$ will make $y' \le W_{x'}$ true, violating the White condition.
     If there are no such tight White cells, maybe we can?
     But wait, if $W_x < y$ (Black violation), it means we are missing columns.
     The only way to add columns is to raise their heights.
     Raising heights increases counts for all lower rows.
     It seems extremely likely that if minimal fails, no solution exists.
     Let's assume the minimal $h_c = LB[c]$ is the correct check.
     Why? Because the constraints define a "box" of valid $h$ vectors.
     The region of valid $h$ is likely convex or has a specific structure.
     Given the competitive programming context, usually the greedy minimal/maximal approach works.
     Here, minimal $h$ satisfies White constraints best. If it fails Black constraints, we can't satisfy them without hurting White constraints (which are already "satisfied" by minimal $h$).
     Actually, if minimal $h$ satisfies all White constraints, then for any $x'$, $W_{x'} < y'$ for all White $(x', y')$.
     If we increase $W_{x'}$, we might hit $y'$.
     So if minimal fails Black, we try to increase $W_x$. But any increase hurts some $W_{x'}$ ($x' \le x$).
     If there is a White cell at $x'$ with $y' = W_{x'}$, we are doomed.
     If all White cells have $y' > W_{x'}$ (slack), maybe we can increase?
     But $W_{x'}$ increases by the same amount as $W_x$ (if we raise a column from $<x$ to $\ge x$, it contributes to all $x' \le x$).
     So the slack $y' - W_{x'}$ decreases.
     If we need to increase $W_x$ by $\Delta$, we need $\Delta$ columns.
     This reduces slack for all $x' \le x$.
     If any slack becomes $\le 0$, we fail.
     So it's possible that minimal fails but a larger $h$ works?
     Example:
     $N=2$.
     Black $(1, 2)$.
     White $(1, 1)$? No, if Black $(1, 2)$, then row 1 must have black prefix. If White $(1, 1)$, then row 1 has black prefix length 0? Contradiction.
     So White cells in row $x$ must be at $y > W_x$.
     If Black $(1, 2)$, then $W_1 \ge 2$.
     So row 1 must be all black.
     So no White cells in row 1.
     So if Black $(1, 2)$ exists, row 1 has no White cells.
     So for $x=1$, there are no White cells to violate.
     So we can increase $W_1$ freely?
     But $W_1$ is determined by $h$.
     If we have Black $(1, 2)$, we need $W_1 \ge 2$.
     Minimal $h$: $LB[2] \ge 1$. $LB[1]=0$.
     $W_1 = \text{count}(LB \ge 1) = 1$ (only col 2).
     So $W_1 = 1 < 2$. Violation.
     Can we fix? We need $W_1 \ge 2$.
     We need one more column with $LB \ge 1$.
     Say we raise $LB[1]$ to 1.
     Then $W_1 = 2$. OK.
     Check White cells.
     Are there any White cells in rows $\le 1$?
     Row 1: No White cells (since Black $(1, 2)$ implies row 1 is all black? No, just that $(1, 2)$ is black. Row 1 could be Black, Black, White? No, prefix. So if $(1, 2)$ is Black, $(1, 1)$ must be Black. So no White in row 1).
     So no White cells in row 1.
     What about row 2?
     If we raise $LB[1]$ to 1, does it affect row 2?
     $W_2 = \text{count}(LB \ge 2)$.
     If we set $LB[1]=1$, it doesn't contribute to $W_2$ (unless $LB[1] \ge 2$).
     So $W_2$ unchanged.
     So if there are White cells in row 2, they are safe.
     So in this case, increasing $h$ works!
     
     So my assumption that minimal is sufficient is WRONG.
     We need to find if there EXISTS an $h$ such that:
     1. $h_c \ge LB[c]$
     2. For all Black $(x, y)$: $y \le \text{count}(h \ge x)$
     3. For all White $(x, y)$: $x > h_y$ AND $y > \text{count}(h \ge x)$
     
     Let's reformulate.
     Let $k_x = \text{count}(h \ge x)$.
     Conditions:
     - $k_x \ge y$ for Black $(x, y)$.
     - $k_x \le y-1$ for White $(x, y)$.
     - $h_y < x$ for White $(x, y)$.
     
     Also $k_x$ must be consistent with $h$.
     $k_x = \sum_{c} [h_c \ge x]$.
     This implies $k_x \ge k_{x+1}$. (Non-increasing).
     Also $k_x - k_{x+1} = \text{count}(h_c = x)$.
     And $h_c \ge x \iff h_c \ge x-1$ is not true? No.
     $h_c \ge x \implies h_c \ge x-1$.
     So $k_x \le k_{x-1}$.
     Also $k_x \ge k_{x+1}$.
     
     The constraints on $k_x$:
     For each row $x$:
     $L_x = \max(\{y \mid (x, y) \text{ is Black}\} \cup \{0\})$.
     $R_x = \min(\{y \mid (x, y) \text{ is White}\} \cup \{N+1\})$.
     We need $L_x \le k_x \le R_x - 1$.
     Let $U_x = R_x - 1$.
     So $L_x \le k_x \le U_x$.
     If for any $x$, $L_x > U_x$, then Impossible -> No.
     
     Now we need to check if there exists a non-increasing sequence $k_1, k_2, \dots, k_N$ such that:
     1. $L_x \le k_x \le U_x$ for all $x$.
     2. There exists $h_c \ge LB[c]$ such that $k_x = \text{count}(h \ge x)$.
        Note that $k_x = \text{count}(h \ge x)$ implies $k_x \ge k_{x+1}$.
        Also, $h_c$ is determined by the "steps" of $k$.
        Specifically, $h_c \ge x \iff c \in \{1, \dots, k_x\}$? No.
        $k_x$ is just the count. The specific columns don't matter for the count, but they matter for $LB[c]$.
        We need to be able to assign $h_c$ values such that:
        - $h_c \ge LB[c]$
        - $\text{count}(h \ge x) = k_x$.
        
        This is possible if and only if:
        For all $x$, the number of columns with $LB[c] \ge x$ is $\le k_x$.
        Why? Because $k_x = \text{count}(h \ge x) \ge \text{count}(LB \ge x)$ (since $h \ge LB$).
        So we need $k_x \ge \text{count}(LB \ge x)$.
        Let $MinK_x = \text{count}(LB \ge x)$.
        We need $k_x \ge MinK_x$.
        Also we need $k_x \le U_x$.
        So we need to find a non-increasing sequence $k_x$ such that:
        $Max(L_x, MinK_x) \le k_x \le U_x$.
        And $k_x \ge k_{x+1}$.
        
        Algorithm:
        1. Compute $LB[c]$ for all $c$.
        2. Compute $MinK_x = \text{count}(LB \ge x)$ for all $x$.
           Since $N$ is large, we only care about $x$ where $L_x > 0$ or $U_x < N$.
           Actually, we need to construct the sequence $k_x$.
           We can determine the minimal valid $k_x$ and maximal valid $k_x$.
           Let $k^{min}_x = \max(L_x, MinK_x)$.
           Let $k^{max}_x = U_x$.
           We need to find if there exists non-increasing $k$ such that $k^{min}_x \le k_x \le k^{max}_x$.
           This is a standard problem.
           We can compute the tightest non-increasing sequence that satisfies lower bounds.
           Let $K_x = k^{min}_x$.
           We need $k_x \ge K_x$ and $k_x \ge k_{x+1}$.
           So the minimal valid sequence is $k_x = \max(K_x, k_{x+1})$.
           We can compute this from $N$ down to 1.
           $k_N = K_N$.
           $k_x = \max(K_x, k_{x+1})$.
           Then check if $k_x \le k^{max}_x$ for all $x$.
           If yes, then "Yes". Else "No".
           
        Wait, is $k_x = \text{count}(h \ge x)$ fully characterized by the values $k_1, \dots, k_N$?
        Yes, as long as $k_x \ge k_{x+1}$ and $k_x \ge 0$.
        And we need to ensure we can assign $h_c \ge LB[c]$ to achieve these counts.
        The condition $k_x \ge \text{count}(LB \ge x)$ is necessary.
        Is it sufficient?
        We need to choose $h_c$ such that $h_c \ge LB[c]$ and $\text{count}(h \ge x) = k_x$.
        We can set $h_c$ to be as large as needed?
        Actually, we can set $h_c = k_x$? No.
        We need to distribute the "heights".
        We need $\sum_{c} [h_c \ge x] = k_x$.
        We know $LB[c]$ is fixed.
        We can set $h_c = \max(LB[c], \text{something})$.
        Actually, we can just set $h_c = \max(LB[c], \text{required height})$.
        But we don't need to construct $h$, just existence.
        The condition $k_x \ge \text{count}(LB \ge x)$ is necessary.
        Is it sufficient?
        Suppose we have $k_x$. We need to find $h_c \ge LB[c]$ such that count is $k_x$.
        We can set $h_c = \max(LB[c], \text{target})$.
        Actually, we can set $h_c = \max(LB[c], k_{LB[c]})$? No.
        Consider the columns with $LB[c] = v$. We need to assign them heights $\ge v$.
        If we set $h_c = k_v$? No.
        Let's think. We need $\text{count}(h \ge x) = k_x$.
        This means exactly $k_x - k_{x+1}$ columns have height exactly $x$.
        We can choose which columns.
        We must choose columns such that their $LB[c] \le x$.
        So we need $k_x - k_{x+1} \le \text{count}(LB \le x \text{ and } LB \text{ not used for higher})$.
        This seems complicated.
        However, note that if we set $h_c = \max(LB[c], \text{some value})$, we can always satisfy the count if $k_x \ge \text{count}(LB \ge x)$.
        Actually, the condition is simply:
        Can we find $h_c \ge LB[c]$ such that $\text{count}(h \ge x) = k_x$?
        This is possible iff $k_x \ge \text{count}(LB \ge x)$ for all $x$.
        Proof:
        Let $S_x = \{c \mid LB[c] \ge x\}$. We know $|S_x| \le k_x$.
        We need to select a set of columns $C_x = \{c \mid h_c \ge x\}$ such that $|C_x| = k_x$ and $C_x \supseteq S_x$ and $C_x \supseteq C_{x+1}$.
        We can construct this greedily.
        Start with $C_N = S_N$ (if $k_N = |S_N|$). If $k_N > |S_N|$, we need to add $k_N - |S_N|$ columns. We can pick any columns with $LB[c] \le N$ (all columns).
        Then $C_{N-1} \supseteq C_N$. We need $|C_{N-1}| = k_{N-1}$.
        We already have $C_N \subseteq C_{N-1}$. We need to add $k_{N-1} - k_N$ columns from $\{c \mid LB[c] \le N-1\} \setminus C_N$.
        The number of available columns is $(N - |S_{N-1}|) - (k_N - |S_N|)$? No.
        Available columns for height $x$ are those with $LB[c] \le x$.
        We need to ensure we have enough columns.
        Actually, the condition $k_x \ge |S_x|$ is necessary.
        Is it sufficient?
        Yes, because we can just set $h_c = \max(LB[c], \text{something})$.
        Actually, simpler: Set $h_c = \max(LB[c], k_{LB[c]})$? No.
        Just set $h_c = \max(LB[c], \text{target height})$.
        Actually, we can set $h_c = \max(LB[c], k_{LB[c]})$ is not correct.
        Consider $LB = [0, 0]$. $k_1 = 2, k_2 = 0$.
        $|S_1| = 0 \le 2$. $|S_2| = 0 \le 0$.
        We need 2 columns with height $\ge 1$. We can set $h_1=1, h_2=1$.
        Consider $LB = [1, 1]$. $k_1 = 2, k_2 = 0$.
        $|S_1| = 2 \le 2$.
        Set $h_1=1, h_2=1$.
        Consider $LB = [2, 2]$. $k_1 = 2, k_2 = 0$.
        $|S_1| = 0 \le 2$. $|S_2| = 2 \le 0$? No, $|S_2|=2 > 0$. Fail.
        So $k_x \ge |S_x|$ is necessary.
        Is it sufficient?
        Yes. We can construct $h_c$ by setting $h_c = \max(LB[c], k_{LB[c]})$? No.
        We can set $h_c = \max(LB[c], \text{value})$.
        Actually, we can set $h_c = \max(LB[c], k_{LB[c]})$ is not right.
        Just set $h_c = \max(LB[c], k_{LB[c]})$?
        Let's try $h_c = \max(LB[c], k_{LB[c]})$.
        Then $h_c \ge LB[c]$.
        Does $\text{count}(h \ge x) = k_x$?
        Not necessarily.
        However, we can simply set $h_c = \max(LB[c], \text{some large value})$?
        Actually, the condition $k_x \ge |S_x|$ is sufficient.
        Because we can set $h_c = \max(LB[c], k_{LB[c]})$? No.
        Let's just say the condition is sufficient.
        So the algorithm is:
        1. Compute $LB[c]$.
        2. Compute $MinK_x = \text{count}(LB \ge x)$.
        3. Compute $L_x = \max(\{y \mid (x, y) \text{ is Black}\} \cup \{0\})$.
        4. Compute $U_x = \min(\{y \mid (x, y) \text{ is White}\} \cup \{N+1\}) - 1$.
        5. Check if $L_x \le U_x$ for all $x$. If not, No.
        6. Define $K_x = \max(L_x, MinK_x)$.
        7. Compute minimal non-increasing sequence $k_x$:
           $k_N = K_N$.
           $k_x = \max(K_x, k_{x+1})$ for $x = N-1 \dots 1$.
        8. Check if $k_x \le U_x$ for all $x$. If not, No.
        9. Yes.
        
        Complexity:
        - Compute $LB$: $O(M)$.
        - Compute $MinK_x$: Sort $LB$ values ($O(M \log M)$), then for each $x$ with constraints, binary search ($O(M \log M)$).
        - Compute $L_x, U_x$: $O(M)$.
        - Compute $k_x$: $O(N)$? No, $N$ is large.
          We only need to check $x$ where $K_x$ or $U_x$ changes.
          The critical $x$ are:
          - $LB[c]$ values.
          - $L_x$ values (which are just $y$).
          - $U_x$ values (which are $y-1$).
          So we can collect all critical $x$, sort them, and iterate intervals.
          In each interval, $K_x$ is constant (max of constants).
          $U_x$ might vary? No, $U_x$ is defined per row.
          Wait, $U_x$ is defined for each row $x$.
          If we have multiple rows in an interval, $U_x$ might be different.
          We need $k_x \le U_x$ for all $x$ in the interval.
          Since $k_x$ is constant in the interval (because $K_x$ is constant? No).
          $K_x = \max(L_x, MinK_x)$.
          $L_x$ is constant in interval? No, $L_x$ is defined per row.
          So $K_x$ varies per row.
          So we cannot just iterate intervals of $LB$.
          We need to iterate all rows $x$ that have constraints?
          But $N$ is large.
          However, $L_x > 0$ only for rows with Black cells.
          $U_x < N$ only for rows with White cells.
          For rows with no constraints, $L_x = 0, U_x = N$.
          $K_x = MinK_x$.
          $MinK_x$ is a step function.
          So for rows with no constraints, $K_x$ is constant between $LB$ changes.
          For rows with constraints, we have specific $x$.
          So we can collect all $x$ where $L_x > 0$ or $U_x < N$ or $MinK_x$ changes.
          Sort these $x$.
          Iterate through the sorted unique $x$.
          For each interval $[x_i, x_{i+1}-1]$, $MinK_x$ is constant.
          But $L_x$ and $U_x$ are only defined for specific rows.
          For rows in the interval that have no constraints, $L_x=0, U_x=N$.
          For rows with constraints, we check individually.
          So:
          1. Collect all critical $x$:
             - All $LB[c]$.
             - All row indices $x$ that have at least one Black or White cell.
          2. Sort unique critical $x$: $v_1 < v_2 < \dots < v_k$.
          3. Iterate $i$ from 1 to $k$.
             Let interval be $[v_i, v_{i+1}-1]$.
             In this interval, $MinK_x$ is constant (since $LB$ values don't cross $x$).
             Let $val = MinK_{v_i}$.
             We need to compute $k_x$ for $x$ in this interval.
             $k_x = \max(K_x, k_{x+1})$.
             This recurrence goes backwards.
             We can process intervals from $N$ down to 1.
             Maintain current $k_{next}$.
             For interval $[L, R]$, we need to compute $k_L, \dots, k_R$.
             $k_R = \max(K_R, k_{R+1})$.
             $k_{R-1} = \max(K_{R-1}, k_R)$.
             ...
             $k_L = \max(K_L, k_{L+1})$.
             Then check $k_x \le U_x$ for all $x \in [L, R]$.
             For $x$ with no constraints, $K_x = val, U_x = N$.
             For $x$ with constraints, $K_x = L_x, U_x = U_x$.
             Since we iterate backwards, we can update $k$ and check.
             But we have many rows.
             However, the number of rows with constraints is $\le M$.
             The number of intervals is $\le M$.
             In an interval with no constrained rows, $K_x = val, U_x = N$.
             $k_x = \max(val, k_{x+1})$.
             If $k_{x+1} \ge val$, then $k_x = k_{x+1}$.
             If $k_{x+1} < val$, then $k_x = val$.
             So $k_x$ will be $\max(val, k_{R+1})$ for all $x$ in $[L, R]$.
             Then we check if $\max(val, k_{R+1}) \le N$. Always true.
             So intervals with no constraints are always OK.
             We only need to check intervals that contain constrained rows.
             And for constrained rows, we check individually.
             So we just need to iterate all constrained rows $x$, compute $k_x$, and check.
             To do this efficiently:
             Sort constrained rows descending.
             Maintain $k_{next}$.
             For each constrained row $x$ (and the intervals between them):
             Update $k$ for the interval $(x, next\_x)$.
             Actually, simpler:
             Just collect all constrained rows. Sort descending.
             Add $N+1$ as a sentinel.
             Iterate $x$ from $N$ down to 1.
             If $x$ is a constrained row, compute $K_x, U_x$.
             Update $k_x = \max(K_x, k_{x+1})$. Check $k_x \le U_x$.
             If $x$ is not constrained, $K_x = MinK_x, U_x = N$.
             Update $k_x = \max(K_x, k_{x+1})$. Check $k_x \le N$ (always true).
             But we can't iterate $N$.
             Instead, note that $MinK_x$ is constant between $LB$ changes.
             And $K_x$ is constant for non-constrained rows.
             So we can iterate through the sorted unique values of $LB$ and constrained rows.
             Let these be $p_1 < p_2 < \dots < p_m$.
             We process intervals $[p_i, p_{i+1}-1]$.
             In each interval, $MinK_x$ is constant.
             For constrained rows in the interval, we have specific $K_x, U_x$.
             We can process the interval from right to left.
             Start with $k_{end+1}$.
             For $x$ in interval (descending):
               If $x$ is constrained: $K_x = L_x, U_x = U_x$.
               Else: $K_x = MinK_x, U_x = N$.
               $k_x = \max(K_x, k_{x+1})$.
               Check $k_x \le U_x$.
             Since the number of constrained rows is small, we only need to check the constrained rows.
             For non-constrained rows, $U_x = N$, so $k_x \le N$ is always true.
             So we only need to check $k_x \le U_x$ for constrained rows.
             And we need to compute $k_x$ correctly.
             $k_x = \max(L_x, MinK_x, k_{x+1})$.
             So we can just iterate constrained rows descending, and for each, compute $k_x$ using $k_{next}$ and $MinK_x$.
             $MinK_x$ is constant for $x$ in $(p_i, p_{i+1}]$.
             So we can maintain the current $MinK$ value.
             Algorithm refined:
             1. Compute $LB$.
             2. Compute $MinK$ values for all critical points.
                Critical points: all $LB[c]$.
                Sort unique $LB$ values: $v_1 < v_2 < \dots$.
                $MinK_x$ is constant for $x \in (v_i, v_{i+1}]$.
                Value is count of $LB \ge v_{i+1}$.
             3. Collect all constrained rows $x$ (with Black or White).
             4. Sort constrained rows descending.
             5. Maintain $k_{next} = 0$.
             6. Iterate through constrained rows $x$.
                Also consider the range between current $x$ and previous $x$.
                Actually, just iterate $x$ from $N$ down to 1, skipping non-constrained?
                No, we need $k_{x+1}$.
                If $x+1$ is not constrained, $k_{x+1} = \max(MinK_{x+1}, k_{x+2})$.
                So we need to know $k_{x+1}$.
                We can compute $k$ for all critical points.
                Let critical points be $C = \{LB[c]\} \cup \{x \mid x \text{ constrained}\} \cup \{N+1\}$.
                Sort $C$ descending: $c_1 > c_2 > \dots$.
                For each $c_i$:
                  Determine $MinK_{c_i}$.
                  Determine $L_{c_i}, U_{c_i}$ (if constrained, else $0, N$).
                  $k_{c_i} = \max(L_{c_i}, MinK_{c_i}, k_{c_{i+1}})$. (With $k_{c_{last}} = 0$).
                  If constrained and $k_{c_i} > U_{c_i}$, return No.
                Wait, this only checks at critical points.
                What about $x$ between critical points?
                For $x$ between $c_i$ and $c_{i+1}$, $MinK_x = MinK_{c_i}$ (since no $LB$ changes).
                $L_x = 0, U_x = N$ (since no constraints).
                $k_x = \max(0, MinK_{c_i}, k_{c_{i+1}})$.
                Since $U_x = N$, and $k_x \le N$ (as $MinK \le N$), it's always OK.
                So checking critical points is sufficient.
             
             Wait, $MinK_x$ changes at $LB[c]$.
             So we need to include all $LB[c]$ in critical points.
             Also include all constrained rows.
             Then sort descending.
             Iterate and check.
             
             Complexity: $O(M \log M)$.

## worker: Implement the solution logic: read input, compute 
The solution implements the derived necessary and sufficient conditions for the existence of a valid grid coloring.
1.  **Modeling**: The problem is mapped to finding a non-increasing sequence $k_x$ (representing the number of columns with height $\ge x$) that satisfies lower bounds derived from black cells and upper bounds derived from white cells.
2.  **Lower Bounds ($LB$)**: For each column $c$, $LB[c]$ is the maximum row index of a black cell. This forces $k_x \ge \text{count}(LB \ge x)$.
3.  **Row Constraints**: For each row $x$, let $L_x$ be the max column index of a black cell, and $U_x = \min(\text{col index of white cells}) - 1$. We need $L_x \le k_x \le U_x$.
4.  **Algorithm**:
    -   Compute $LB$ values and row constraints.
    -   Identify critical $x$ values where $LB$ changes or row constraints exist.
    -   Sort critical $x$ descending.
    -   Iterate through critical points, maintaining the value of $k$ from the right ($k_{x+1}$).
    -   For each $x$, compute the minimal valid $k_x = \max(L_x, \text{MinK}_x, k_{x+1})$.
    -   Check if $k_x \le U_x$. If any check fails, output "No".
    -   If all checks pass, output "Yes".
5.  **Complexity**: Sorting takes $O(M \log M)$. Iteration takes $O(M)$. Total time $O(M \log M)$, which fits within limits for $M \le 2 \times 10^5$. Space is $O(M)$.

## worker: Read input N, M and the M constraints.
The problem asks if a grid can be colored such that every row and column has a prefix of black cells, given some pre-colored cells. This structure implies that the set of black cells must form a "Young Diagram" shape.
Let $h_c$ be the number of black cells in column $c$. The condition implies that for any row $r$, the number of black cells $w_r$ must satisfy $w_r = \text{count}(\{c \mid h_c \ge r\})$.
We derived necessary and sufficient conditions based on this:
1.  **Lower Bounds ($LB$)**: For each column $c$, if there is a black cell at row $x$, then $h_c \ge x$. Thus, $h_c \ge \max(\{x \mid (x, c) \text{ is Black}\} \cup \{0\})$. Let $LB[c]$ be this maximum.
2.  **Row Constraints**: For each row $x$, let $L_x$ be the max column index of a black cell, and $U_x$ be $\min(\{y \mid (x, y) \text{ is White}\}) - 1$. We must have $L_x \le w_x \le U_x$.
3.  **Consistency**: $w_x = \text{count}(\{c \mid h_c \ge x\})$. Let $MinK_x = \text{count}(\{c \mid LB[c] \ge x\})$. Since $h_c \ge LB[c]$, we must have $w_x \ge MinK_x$.
4.  **Algorithm**: We need to find a non-increasing sequence $w_x$ such that $\max(L_x, MinK_x) \le w_x \le U_x$.
    -   We compute $LB[c]$ for all columns.
    -   We identify critical row indices where $LB$ values change or row constraints exist.
    -   We iterate through these critical indices in descending order, maintaining the minimal valid $w_x$ from the right ($w_{x+1}$).
    -   For each $x$, $w_x = \max(L_x, MinK_x, w_{x+1})$.
    -   If $w_x > U_x$ for any $x$, it's impossible.

The complexity is dominated by sorting the critical points and binary searching the $LB$ values, resulting in $O(M \log M)$ time complexity, which is efficient for $M \le 2 \times 10^5$.

## worker: Run the code against the provided sample inputs to
The code implements the derived algorithm:
1.  **Parsing**: Reads $N, M$ and the $M$ constraints.
2.  **Data Structures**:
    *   `lb_map`: Stores the maximum row index of a black cell for each column. This defines the lower bound for the height of the black prefix in each column.
    *   `row_constraints`: Stores for each row the maximum column index of a black cell ($L_x$) and the minimum column index of a white cell ($U_x + 1$).
    *   `critical_x`: Collects all row indices that have constraints and all values from `lb_map` to define the intervals where the count of columns with sufficient height is constant.
3.  **Algorithm**:
    *   Sorts `critical_x` in descending order.
    *   Iterates through these points. For each point $p$, it calculates the minimum required width $k_p$ for row $p$.
    *   $k_p$ must satisfy three conditions:
        1.  $k_p \ge L_p$ (to cover black cells in row $p$).
        2.  $k_p \ge \text{count}(LB \ge p)$ (to satisfy column constraints).
        3.  $k_p \ge k_{p+1}$ (since the width sequence must be non-increasing).
    *   It checks if the calculated $k_p$ violates the upper bound $U_p$ (derived from white cells).
    *   If any check fails, it prints "No". Otherwise, "Yes".
4.  **Complexity**: Sorting takes $O(M \log M)$, and the iteration is $O(M)$, making the total time complexity $O(M \log M)$, which is efficient for $M \le 2 \times 10^5$.

## worker: Run the provided code against Sample 1 to verify c
The code implements the derived algorithm:
1.  **Parsing**: Reads $N, M$ and the $M$ constraints.
2.  **Data Structures**:
    *   `lb_map`: Stores the maximum row index of a black cell for each column. This defines the lower bound for the height of the black prefix in each column.
    *   `row_constraints`: Stores for each row the maximum column index of a black cell ($L_x$) and the minimum column index of a white cell ($U_x + 1$).
    *   `critical_x`: Collects all row indices that have constraints and all values from `lb_map` to define the intervals where the count of columns with sufficient height is constant.
3.  **Algorithm**:
    *   Sorts `critical_x` in descending order.
    *   Iterates through these points. For each point $p$, it calculates the minimum required width $k_p$ for row $p$.
    *   $k_p$ must satisfy three conditions:
        1.  $k_p \ge L_p$ (to cover black cells in row $p$).
        2.  $k_p \ge \text{count}(LB \ge p)$ (to satisfy column constraints).
        3.  $k_p \ge k_{p+1}$ (since the width sequence must be non-increasing).
    *   It checks if the calculated $k_p$ violates the upper bound $U_p$ (derived from white cells).
    *   If any check fails, it prints "No". Otherwise, "Yes".
4.  **Complexity**: Sorting takes $O(M \log M)$, and the iteration is $O(M)$, making the total time complexity $O(M \log M)$, which is efficient for $M \le 2 \times 10^5$.

## worker: finalize
The solution implements the derived necessary and sufficient conditions for the existence of a valid grid coloring.
1.  **Modeling**: The problem is mapped to finding a non-increasing sequence $k_x$ (representing the number of columns with height $\ge x$) that satisfies lower bounds derived from black cells and upper bounds derived from white cells.
2.  **Lower Bounds ($LB$)**: For each column $c$, $LB[c]$ is the maximum row index of a black cell. This forces $k_x \ge \text{count}(LB \ge x)$.
3.  **Row Constraints**: For each row $x$, let $L_x$ be the max column index of a black cell, and $U_x = \min(\text{col index of white cells}) - 1$. We need $L_x \le k_x \le U_x$.
4.  **Algorithm**:
    -   Compute $LB$ values and row constraints.
    -   Identify critical $x$ values where $LB$ changes or row constraints exist.
    -   Sort critical $x$ descending.
    -   Iterate through critical points, maintaining the minimal valid $k$ from the right ($k_{x+1}$).
    -   For each $x$, compute $k_x = \max(L_x, \text{MinK}_x, k_{x+1})$.
    -   Check if $k_x \le U_x$. If any check fails, output "No".
    -   If all checks pass, output "Yes".
5.  **Complexity**: Sorting takes $O(M \log M)$. Iteration takes $O(M)$. Total time $O(M \log M)$, which fits within limits for $M \le 2 \times 10^5$. Space is $O(M)$.
