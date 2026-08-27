
## ideation
The problem asks for the number of valid paths in a grid $[0, W] \times [0, H]$ with a rectangular forbidden region $[L, R] \times [D, U]$. A path is valid if it starts at a valid block, ends at a valid block, and every intermediate point is a valid block. Moves are only in the positive x or y direction.

The total number of paths in the full grid (ignoring the hole) can be computed efficiently. Let $Total$ be this sum.
The number of invalid paths (those that visit at least one point in the hole) can be computed using the "first hit" principle. A path is invalid if it enters the hole. The first point in the hole visited by a path must be on the "entry boundary" of the hole. Since we move only Right and Up, the entry points are:
1. The left edge of the hole: $P_L = (L, y)$ for $D \le y \le U$.
2. The bottom edge of the hole: $P_B = (x, D)$ for $L \le x \le R$.

Note that $(L, D)$ is in both sets.

For a point $P$ on the entry boundary, let $First(P)$ be the number of paths that start at some valid $S$, end at some valid $E$, and have $P$ as the *first* point in the hole visited.
Then, the total number of invalid paths is $\sum_{P \in \text{Entry}} First(P)$.

$First(P)$ can be decomposed into:
$First(P) = (\text{Number of valid starts } S \text{ such that the path from } S \text{ to } P \text{ avoids the hole before } P) \times (\text{Number of valid ends } E \text{ such that the path from } P \text{ to } E \text{ stays in valid blocks?})$

Wait, if $P$ is in the hole, it is not a block. So a path cannot "stand" on $P$.
However, the problem states Snuke moves between blocks. If he tries to move to a non-block, he can't.
So, strictly speaking, a path *cannot* visit a point in the hole.
Thus, the set of "paths that visit the hole" is empty in the context of Snuke's movement?
No, the question is "Print the number of possible paths that Snuke could have taken."
Snuke only takes paths consisting of blocks.
So we just need to count the number of paths that lie entirely within the valid region.

This is equivalent to:
$Answer = (\text{Total paths in full grid}) - (\text{Paths in full grid that intersect the hole})$.
Why? Because any path in the full grid that intersects the hole is invalid for Snuke, and any path that doesn't intersect the hole is valid.
Note: "Intersect" here means the sequence of lattice points includes at least one point in $[L, R] \times [D, U]$.

To count paths in the full grid that intersect the hole, we use the first-hit method.
Let $H$ be the hole.
$Paths(H) = \sum_{P \in \text{FirstHitBoundary}} (\text{Paths } S \to P \text{ avoiding } H \setminus \{P\}) \times (\text{Paths } P \to E)$.

The first hit boundary consists of:
- $L_{entry} = \{ (L, y) \mid D \le y \le U \}$
- $B_{entry} = \{ (x, D) \mid L \le x \le R \}$

For $P=(L, y)$ with $y > D$:
The path from $S$ to $P$ must not touch any point in $H$ before $P$.
Since $P$ is on the left edge, the path must come from $x < L$.
The number of such paths from $S$ to $P$ is simply the number of paths from $S$ to $P$ in the full grid, provided $S$ is "safe".
Actually, it's easier to compute the total contribution of all starts $S$ to the first hit at $P$.
Let $WaysToHit(P)$ be the number of pairs $(S, \text{path } S \to P)$ such that $S$ is valid, $P$ is the first hole point, and the path stays in valid blocks until $P$.
Since $P$ is not a block, the path ends at a neighbor of $P$? No, the path *visits* $P$. In the "Full Grid" counting, we count all lattice point sequences.
So, $WaysToHit(P) = \sum_{S \in Valid, S \le P} (\text{Paths } S \to P \text{ avoiding } H \setminus \{P\})$.

For $P=(L, y)$ with $y > D$:
The condition "avoiding $H \setminus \{P\}$" means the path does not touch any $(L, y')$ for $D \le y' < y$ and does not touch any $(x, y')$ for $x > L, y' \ge D$.
Since the path ends at $(L, y)$, and moves only Right/Up, it must stay in $x \le L$.
If it ever has $x > L$, it would have entered the hole earlier (since $y \ge D$).
So the path must stay in $x \le L$.
Also, it must not touch $(L, y')$ for $D \le y' < y$.
This implies the path must stay in $x < L$ until the very last step?
No, it can touch $(L, y')$ for $y' < D$.
So, the path from $S$ to $(L, y)$ avoids $H \setminus \{P\}$ if and only if:
1. It stays in $x \le L$.
2. It does not touch any $(L, y')$ for $D \le y' < y$.

This can be computed using DP or inclusion-exclusion on the boundary.
Let $A_L[y]$ be the number of paths from any valid $S$ to $(L, y)$ that hit $(L, y)$ as the first point in $H$.
$A_L[y] = (\text{Total paths from any } S \text{ to } (L, y) \text{ staying in } x \le L) - \sum_{y'=D}^{y-1} A_L[y'] \times \text{Paths}((L, y') \to (L, y))$.

Similarly for $B_{entry}$.

Then, the number of invalid paths is:
$\sum_{y=D}^U A_L[y] \times (\text{Sum of paths from } (L, y) \text{ to any valid } E)$
$+ \sum_{x=L}^R A_B[x] \times (\text{Sum of paths from } (x, D) \text{ to any valid } E)$
$- (\text{Overlap for } (L, D))$.

The term "Sum of paths from $P$ to any valid $E$" is the number of paths starting at $P$ and ending at any valid block $E \ge P$.
Note: $P$ is not a block, but in the "Full Grid" subtraction method, we count paths that *visit* $P$. The suffix of the path from $P$ to $E$ can go anywhere valid.
So we need $SuffixSum(P) = \sum_{E \in Valid, E \ge P} N(P, E)$.

This approach is $O(W+H)$ with precomputed binomial coefficients and prefix sums.

## worker: Implement modular arithmetic and precompute factor
The problem asks for the number of valid paths in a grid with a rectangular hole. A valid path consists of a sequence of blocks (lattice points not in the hole) starting at a block and moving only right or up.

1.  **Total Paths in Full Grid**: We first calculate the total number of paths in the full grid $[0, W] \times [0, H]$, ignoring the hole. This is done by summing the number of paths from any start point $S$ to any end point $E$ ($S \le E$). The number of paths from $S$ to $E$ is $\binom{\Delta x + \Delta y}{\Delta x}$. The sum over all $S \le E$ for a fixed $E$ can be computed using the identity $\sum_{dx=0}^x \sum_{dy=0}^y \binom{dx+dy}{dx} = \binom{x+y+2}{x+1} - 1$. Summing this over all $E$ gives the total.

2.  **Invalid Paths (Touching the Hole)**: We subtract the number of paths that visit at least one point in the hole $[L, R] \times [D, U]$. Using the "first hit" principle, we sum over all possible first points $P$ in the hole that a path can visit. The first hit must be on the "entry boundary": the left edge $(L, y)$ for $y \in [D, U]$ or the bottom edge $(x, D)$ for $x \in [L, R]$.

3.  **First Hit Calculation**: For each entry point $P$, we calculate $WaysToHit(P)$, the number of paths from any valid start $S$ to $P$ such that $P$ is the first point in the hole visited. This is computed using a DP-like recurrence on the boundary:
    *   $A_L[y] = T_L[y] - \sum_{y'=D}^{y-1} A_L[y']$, where $T_L[y]$ is the total paths to $(L, y)$ from any $S \le (L, y)$.
    *   Similarly for $A_B[x]$ on the bottom edge.

4.  **Suffix Paths**: For each first hit $P$, we multiply $WaysToHit(P)$ by the number of paths from $P$ to any valid end point $E \ge P$. This is the total paths from $P$ to the full grid minus paths from $P$ to the hole part "above/right" of $P$.

5.  **Overlap Correction**: The point $(L, D)$ is on both boundaries. It is counted in both $A_L$ and $A_B$ sums, so we subtract one instance of its contribution to avoid double counting.

6.  **Complexity**: Precomputing factorials is $O(W+H)$. The loops for $A_L$ and $A_B$ are $O(U-D)$ and $O(R-L)$ respectively. The total complexity is $O(W+H)$, which fits within the constraints.
