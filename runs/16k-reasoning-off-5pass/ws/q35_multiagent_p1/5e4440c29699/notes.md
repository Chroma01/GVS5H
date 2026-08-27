
## ideation
The core difficulty lies in correctly applying the Principle of Inclusion-Exclusion (PIE) to the union of four overlapping rectangular regions, and efficiently calculating the number of paths within any given rectangular sub-region.

1.  **Region Definition**: The valid blocks are those in $[0, W] \times [0, H]$ EXCEPT the hole $[L, R] \times [D, U]$. This valid set $S$ can be decomposed into the union of four simpler rectangular regions:
    *   $S_L$: $x < L$ (Left strip)
    *   $S_R$: $x > R$ (Right strip)
    *   $S_D$: $y < D$ (Bottom strip)
    *   $S_U$: $y > U$ (Top strip)
    Note: The boundaries are inclusive/exclusive carefully. $S_L$ is $0 \le x \le L-1$, $S_R$ is $R+1 \le x \le W$, etc. If $L=0$, $S_L$ is empty. If $R=W$, $S_R$ is empty. Same for $D, U$.

2.  **PIE Application**: We need to calculate $\sum_{\emptyset \neq I \subseteq \{L,R,D,U\}} (-1)^{|I|-1} \text{Paths}(\bigcap_{i \in I} S_i)$.
    The intersection of any subset of these regions is itself a rectangle (possibly empty). For example, $S_L \cap S_D$ is $[0, L-1] \times [0, D-1]$. $S_L \cap S_R$ is empty. We iterate through all $2^4 - 1 = 15$ non-empty subsets. For each subset, we determine the bounding box of the intersection. If the bounding box is invalid (e.g., $x_{min} > x_{max}$), the count is 0.

3.  **Path Counting in a Rectangle**: For a rectangle $[x_1, x_2] \times [y_1, y_2]$, we need to sum $\binom{(ex-sx) + (ey-sy)}{ex-sx}$ over all $x_1 \le sx \le ex \le x_2$ and $y_1 \le sy \le ey \le y_2$.
    Let $dx = ex - sx$ and $dy = ey - sy$. The term is $\binom{dx+dy}{dx}$.
    We can rewrite the sum by iterating over possible start points $(sx, sy)$ and end points $(ex, ey)$.
    Alternatively, we can use the identity: The number of paths from any point in $[x_1, x_2] \times [y_1, y_2]$ to any point in $[x_1, x_2] \times [y_1, y_2]$ (moving only right/up) can be computed using prefix sums of binomial coefficients or by transforming the problem.
    A standard trick for "sum of paths in a rectangle" is:
    Total paths = $\sum_{sx=x_1}^{x_2} \sum_{sy=y_1}^{y_2} \sum_{ex=sx}^{x_2} \sum_{ey=sy}^{y_2} \binom{(ex-sx)+(ey-sy)}{ex-sx}$.
    Let $u = ex-sx, v = ey-sy$. Then $0 \le u \le x_2-sx$ and $0 \le v \le y_2-sy$.
    Sum becomes $\sum_{sx, sy} \sum_{u=0}^{x_2-sx} \sum_{v=0}^{y_2-sy} \binom{u+v}{u}$.
    We know $\sum_{v=0}^{M} \binom{u+v}{u} = \binom{u+M+1}{u+1}$.
    So inner sum over $v$ is $\binom{u + (y_2-sy) + 1}{u+1}$.
    Then sum over $u$: $\sum_{u=0}^{x_2-sx} \binom{u + K}{u+1}$ where $K = y_2-sy+1$.
    This looks complicated to sum directly for each start point.
    
    Better approach: Use the property that the number of paths from $(sx, sy)$ to $(ex, ey)$ is the coefficient of $x^{ex-sx} y^{ey-sy}$ in some generating function, or simply use the fact that:
    $\sum_{sx=x_1}^{x_2} \sum_{sy=y_1}^{y_2} \sum_{ex=sx}^{x_2} \sum_{ey=sy}^{y_2} \binom{ex-sx+ey-sy}{ex-sx} = \sum_{dx=0}^{x_2-x_1} \sum_{dy=0}^{y_2-y_1} \binom{dx+dy}{dx} \times (\text{count of pairs } (sx, sy) \text{ such that } sx+dx \le x_2, sy+dy \le y_2)$.
    The number of valid start points $(sx, sy)$ for a given displacement $(dx, dy)$ is $(x_2 - x_1 - dx + 1) \times (y_2 - y_1 - dy + 1)$.
    So, `count_paths_rect(x1, x2, y1, y2)` = 
    $\sum_{dx=0}^{x_2-x_1} \sum_{dy=0}^{y_2-y_1} \binom{dx+dy}{dx} (x_2 - x_1 - dx + 1) (y_2 - y_1 - dy + 1)$.
    
    Since $W, H \le 10^6$, a double loop is $O(W \cdot H)$ which is too slow ($10^{12}$). We need a faster way.
    
    Let $W' = x_2 - x_1$ and $H' = y_2 - y_1$.
    Sum = $\sum_{dx=0}^{W'} \sum_{dy=0}^{H'} \binom{dx+dy}{dx} (W' - dx + 1) (H' - dy + 1)$.
    Expand: $(W' + 1)(H' + 1) \sum \binom{dx+dy}{dx} - (W' + 1) \sum dx \binom{dx+dy}{dx} - (H' + 1) \sum dy \binom{dx+dy}{dx} + \sum dx \cdot dy \binom{dx+dy}{dx}$.
    
    We can precompute prefix sums of binomial coefficients to answer these queries in $O(1)$ or $O(\log MOD)$?
    Actually, there is a known identity:
    $\sum_{i=0}^n \sum_{j=0}^m \binom{i+j}{i} = \binom{n+m+2}{n+1} - 1$? No, that's not quite right.
    Identity: $\sum_{i=0}^n \binom{i+k}{i} = \binom{n+k+1}{n}$.
    
    Let's use the "grid path" interpretation. The sum $\sum_{sx, sy, ex, ey} \text{paths}(sx,sy \to ex,ey)$ is equivalent to counting pairs of points $(A, B)$ in the rectangle such that $A \le B$ (coordinate-wise) with weight 1.
    This is equal to the number of paths from a "super-source" to a "super-sink"?
    
    Actually, consider the transformation:
    Let $N(W', H')$ be the answer for rectangle of size $W' \times H'$ (width $W'$, height $H'$, so $W'+1$ points, $H'+1$ points).
    $N(W', H') = \sum_{dx=0}^{W'} \sum_{dy=0}^{H'} \binom{dx+dy}{dx} (W' - dx + 1) (H' - dy + 1)$.
    
    We can compute this in $O(W' + H')$ or $O(1)$ with precomputation.
    Note that $\sum_{dx=0}^{W'} \sum_{dy=0}^{H'} \binom{dx+dy}{dx} = \binom{W'+H'+2}{W'+1} - 1$ is incorrect.
    Correct identity: $\sum_{i=0}^n \sum_{j=0}^m \binom{i+j}{i} = \binom{n+m+2}{n+1} - 1$? Let's check small case. $n=1, m=1$.
    Terms: $i=0,j=0: 1$. $i=0,j=1: 1$. $i=1,j=0: 1$. $i=1,j=1: 2$. Sum = 5.
    Formula: $\binom{1+1+2}{1+1} - 1 = \binom{4}{2} - 1 = 6 - 1 = 5$. Correct.
    So $\sum_{dx=0}^{W'} \sum_{dy=0}^{H'} \binom{dx+dy}{dx} = \binom{W'+H'+2}{W'+1} - 1$.
    
    What about $\sum dx \binom{dx+dy}{dx}$?
    $dx \binom{dx+dy}{dx} = (dx+dy) \binom{dx+dy-1}{dx-1}$? No.
    $dx \binom{n}{k} = n \binom{n-1}{k-1}$. Here $n=dx+dy, k=dx$.
    $dx \binom{dx+dy}{dx} = (dx+dy) \binom{dx+dy-1}{dx-1}$.
    This seems messy.
    
    Alternative: Use dynamic programming or precomputed tables for the sums $S_0(W', H')$, $S_1(W', H')$, etc.
    Given constraints $10^6$, we can precompute factorials. We need to evaluate sums of form $\sum_{dx, dy} \binom{dx+dy}{dx} dx^a dy^b$.
    Since max $W', H'$ is $10^6$, we can't do $O(W'H')$. But we can do $O(W'+H')$ per query if we use prefix sums of binomials.
    
    Let $C(n, k) = \binom{n}{k}$.
    We need:
    $T_0 = \sum_{dx=0}^{W'} \sum_{dy=0}^{H'} C(dx+dy, dx)$
    $T_1 = \sum_{dx=0}^{W'} \sum_{dy=0}^{H'} dx \cdot C(dx+dy, dx)$
    $T_2 = \sum_{dx=0}^{W'} \sum_{dy=0}^{H'} dy \cdot C(dx+dy, dx)$
    $T_3 = \sum_{dx=0}^{W'} \sum_{dy=0}^{H'} dx \cdot dy \cdot C(dx+dy, dx)$
    
    Then Ans = $(W'+1)(H'+1) T_0 - (W'+1) T_2 - (H'+1) T_1 + T_3$. (Note: $dx$ corresponds to x-displacement, so it multiplies the term with $H'-dy+1$? Wait.
    Expansion: $(W'-dx+1)(H'-dy+1) = (W'+1)(H'+1) - (W'+1)dy - (H'+1)dx + dx \cdot dy$.
    So:
    Term 1: $(W'+1)(H'+1) \sum C$
    Term 2: $-(W'+1) \sum dy \cdot C$
    Term 3: $-(H'+1) \sum dx \cdot C$
    Term 4: $+ \sum dx \cdot dy \cdot C$
    
    We can compute $T_0, T_1, T_2, T_3$ efficiently.
    $T_0(W', H') = \binom{W'+H'+2}{W'+1} - 1$.
    
    For $T_1(W', H') = \sum_{dx=0}^{W'} dx \sum_{dy=0}^{H'} \binom{dx+dy}{dx}$.
    Let $S(dy, dx) = \sum_{j=0}^{dy} \binom{dx+j}{dx} = \binom{dx+dy+1}{dx+1}$.
    So inner sum is $\binom{dx+H'+1}{dx+1}$.
    $T_1 = \sum_{dx=0}^{W'} dx \binom{dx+H'+1}{dx+1}$.
    Let $k = dx+1$. Sum $k=1$ to $W'+1$: $(k-1) \binom{k+H'}{k}$.
    $\binom{k+H'}{k} = \binom{k+H'}{H'}$.
    Sum $(k-1) \binom{k+H'}{H'}$.
    This can be computed using precomputed prefix sums of binomial coefficients $\sum_{k} \binom{k+H'}{H'}$ and $\sum_{k} k \binom{k+H'}{H'}$.
    Since $H'$ varies per query, we can't precompute all. But we can compute $\sum_{k=1}^{M} \binom{k+N}{N}$ and $\sum_{k=1}^{M} k \binom{k+N}{N}$ in $O(1)$ using identities?
    Identity: $\sum_{i=0}^n \binom{i+k}{k} = \binom{n+k+1}{k+1}$.
    So $\sum_{k=1}^{W'+1} \binom{k+H'}{H'} = \binom{W'+1+H'+1}{H'+1} - \binom{0+H'}{H'} = \binom{W'+H'+2}{H'+1} - 1$.
    
    For $\sum k \binom{k+N}{N}$:
    $k \binom{k+N}{N} = (k+N-N) \binom{k+N}{N} = (k+N) \binom{k+N}{N} - N \binom{k+N}{N} = (N+1) \binom{k+N+1}{N+1} - N \binom{k+N}{N}$.
    Summing this telescopes or uses standard sums.
    $\sum_{k=1}^{M} k \binom{k+N}{N} = (N+1) \sum \binom{k+N+1}{N+1} - N \sum \binom{k+N}{N}$.
    Both sums are of the form $\sum \binom{i+C}{C}$, which we know.
    
    Thus, all $T_i$ can be computed in $O(1)$ with precomputed factorials.

## worker: Implement modular arithmetic utilities (modular in
1.  **Problem Decomposition**: The valid blocks form a rectangle $[0, W] \times [0, H]$ with a central hole $[L, R] \times [D, U]$. This shape is the union of four rectangular regions: Left ($x < L$), Right ($x > R$), Down ($y < D$), and Up ($y > U$).
2.  **Inclusion-Exclusion Principle (PIE)**: To count paths in the union of these regions, we use PIE. We iterate through all non-empty subsets of these 4 regions. For each subset, we find the intersection (which is also a rectangle) and calculate the number of paths within that intersection. We add the count if the subset size is odd and subtract if even.
3.  **Path Counting in a Rectangle**: The core function `count_paths_rect(x1, x2, y1, y2)` calculates the total number of valid paths starting and ending within the rectangle. This is equivalent to summing $\binom{dx+dy}{dx}$ weighted by the number of valid start points for each displacement $(dx, dy)$.
4.  **Efficient Summation**: Direct summation is $O(W \cdot H)$, which is too slow. We expanded the weight $(W'-dx+1)(H'-dy+1)$ into four terms involving sums of binomial coefficients multiplied by $dx$ and $dy$.
5.  **Combinatorial Identities**:
    *   $\sum_{i=0}^n \sum_{j=0}^m \binom{i+j}{i} = \binom{n+m+2}{n+1} - 1$.
    *   Sums involving $k \binom{k+N}{N}$ were derived using the identity $k \binom{k+N}{N} = (N+1)\binom{k+N+1}{N+1} - N\binom{k+N}{N}$, allowing $O(1)$ calculation using precomputed factorials.
6.  **Complexity**: Precomputation of factorials is $O(MAX\_VAL)$. Each query for `count_paths_rect` is $O(1)$. There are at most 15 subsets in PIE. Total time complexity is dominated by precomputation, $O(W+H)$, which fits well within limits for $10^6$.
