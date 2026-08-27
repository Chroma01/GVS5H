
## ideation
**Core Difficulty:**
The problem requires summing Manhattan distances over all $\binom{m \times n}{k}$ valid arrangements. A brute-force enumeration of arrangements is impossible due to the large constraints ($m \times n \le 10^5$, but the number of arrangements can be huge). The key is to use linearity of expectation (or summation) to decompose the 2D problem into independent 1D problems for rows and columns.

**Candidate Approaches:**
1.  **Decomposition**: Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ allows us to calculate the total sum as:
    $$ \text{Total} = \text{Sum}_{\text{rows}} + \text{Sum}_{\text{cols}} $$
    where $\text{Sum}_{\text{rows}}$ considers only the difference in row indices, and $\text{Sum}_{\text{cols}}$ considers only the difference in column indices.

2.  **1D Reduction**:
    For a 1D line of length $L$ (say, $m$ rows), we need to choose $k$ positions.
    -   Total ways to choose $k$ positions from $L$ is $\binom{L}{k}$.
    -   For a specific pair of positions at indices $i$ and $j$ ($i < j$), the distance is $j - i$.
    -   The number of ways to place the remaining $k-2$ pieces in the remaining $L-2$ spots is $\binom{L-2}{k-2}$.
    -   However, iterating over all pairs $(i, j)$ is $O(L^2)$, which is too slow if $L$ is up to $10^5$.

3.  **Optimized 1D Calculation**:
    Instead of iterating over pairs, we can iterate over the *gap* size or the position of the $p$-th piece.
    -   Let's consider the contribution of each unit distance in the 1D line.
    -   Alternatively, fix a position $x$ in the 1D line. How many arrangements have exactly $a$ pieces to the left of $x$ and $b$ pieces to the right?
    -   Actually, a simpler combinatorial identity exists: The sum of distances between all pairs of $k$ points chosen uniformly from $L$ points can be calculated by summing the contribution of each interval between adjacent grid points.
    -   Let the grid points be $1, 2, \dots, L$. The distance between point $i$ and point $j$ ($i<j$) is $\sum_{p=i}^{j-1} 1$.
    -   We can swap the summation order: Sum over all intervals $(p, p+1)$ of the number of pairs $(i, j)$ such that $i \le p < p+1 \le j$.
    -   For an interval between index $p$ and $p+1$ (where $1 \le p < L$), the number of ways to choose $k$ points such that some are $\le p$ and some are $> p$ is:
        -   Choose $i$ points from the left side ($1 \dots p$): $\binom{p}{i}$
        -   Choose $k-i$ points from the right side ($p+1 \dots L$): $\binom{L-p}{k-i}$
        -   Sum over all valid $i$ (from $\max(0, k-(L-p))$ to $\min(k, p)$).
    -   The contribution of this interval to the total distance sum for one specific arrangement is 1 if the pair spans this interval. Summing over all arrangements, the total contribution of this interval is:
        $$ \left( \sum_{i} \binom{p}{i} \binom{L-p}{k-i} \right) \times \binom{L-2}{k-2} \times \text{something?} $$
        Wait, the standard formula for the sum of distances for one set of $k$ points is $\sum_{p=1}^{L-1} (\text{# pairs crossing } p)$.
        The number of pairs crossing $p$ in a single arrangement is $i \times (k-i)$ where $i$ is the number of points on the left.
        So for one arrangement, the expected sum of distances is $\sum_{p} \sum_{i} \frac{i(k-i)}{\binom{L}{k}} \binom{p}{i}\binom{L-p}{k-i}$.
        But we need the sum over *all* arrangements.
        Total Sum = $\sum_{\text{arrangements}} \sum_{\text{pairs}} \text{dist} = \sum_{p=1}^{L-1} (\text{Total # of pairs crossing } p \text{ across all arrangements})$.
        Total # of pairs crossing $p$ = $\sum_{i=1}^{k-1} (\text{ways to choose } i \text{ left}) \times (\text{ways to choose } k-i \text{ right}) \times (\text{ways to choose remaining } k-2 \text{ from remaining } L-2 \text{ spots?})$.
        Actually, simpler:
        To form a pair crossing $p$, we pick one point from $1..p$ and one from $p+1..L$.
        Number of ways to pick such a pair: $p \times (L-p)$.
        Number of ways to pick the remaining $k-2$ points from the remaining $L-2$ points: $\binom{L-2}{k-2}$.
        So, total pairs crossing $p$ across all arrangements = $p(L-p) \times \binom{L-2}{k-2}$.
        Wait, this counts pairs. We need the sum of distances.
        Distance = sum of 1s for each interval crossed.
        So Total Sum = $\sum_{p=1}^{L-1} [ \text{Number of arrangements where a specific pair crosses } p ] \times (\text{number of pairs})$.
        Let's re-evaluate:
        Total Sum = $\sum_{\text{all arrangements}} \sum_{1 \le a < b \le k} \text{dist}(pos_a, pos_b)$.
        Swap sums: $\sum_{p=1}^{L-1} \sum_{\text{all arrangements}} (\text{number of pairs crossing } p)$.
        For a fixed $p$, the number of pairs crossing $p$ in a specific arrangement with $i$ points on the left is $i(k-i)$.
        Sum over all arrangements: $\sum_{i=0}^k \binom{p}{i} \binom{L-p}{k-i} \times i(k-i)$.
        Note: $\binom{p}{i} \binom{L-p}{k-i}$ is the number of arrangements with exactly $i$ points on the left.
        So the term for $p$ is $\sum_{i} \binom{p}{i} \binom{L-p}{k-i} i(k-i)$.
        This can be simplified using combinatorial identities.
        Identity: $\sum_{i} \binom{p}{i} \binom{L-p}{k-i} = \binom{L}{k}$.
        Identity for $i \binom{p}{i} = p \binom{p-1}{i-1}$.
        Term = $p \sum_{i} \binom{p-1}{i-1} \binom{L-p}{k-i} (k-i)$.
        Let $j = i-1$. Then $k-i = k-1-j$.
        Term = $p \sum_{j} \binom{p-1}{j} \binom{L-p}{k-1-j} (k-1-j)$.
        Similarly, $(k-i) \binom{L-p}{k-i} = (k-i) \frac{L-p}{k-i} \binom{L-p-1}{k-i-1} = (L-p) \binom{L-p-1}{k-i-1}$.
        So Term = $\sum_{i} \binom{p}{i} \binom{L-p}{k-i} i(k-i) = p(L-p) \sum_{i} \binom{p-1}{i-1} \binom{L-p-1}{k-i-1}$.
        The sum $\sum_{i} \binom{p-1}{i-1} \binom{L-p-1}{k-i-1}$ is exactly $\binom{(p-1)+(L-p-1)}{(i-1)+(k-i-1)} = \binom{L-2}{k-2}$.
        So, the contribution of interval $p$ is $p(L-p) \binom{L-2}{k-2}$.
        This is remarkably simple!
        Total Sum for dimension $L$ = $\binom{L-2}{k-2} \times \sum_{p=1}^{L-1} p(L-p)$.
        
        Let's verify with Example 1: m=2, n=2, k=2.
        Rows ($L=2$): $\binom{0}{0} \times \sum_{p=1}^{1} p(2-p) = 1 \times (1 \times 1) = 1$.
        Cols ($L=2$): Same = 1.
        Total = 2? But example output is 8.
        Wait, the example says "sum of Manhattan distances between every pair of pieces over all valid arrangements".
        In Example 1, there are $\binom{4}{2} = 6$ arrangements.
        Arrangements:
        (0,0)-(0,1): dist 1
        (0,0)-(1,0): dist 1
        (0,0)-(1,1): dist 2
        (0,1)-(1,0): dist 2
        (0,1)-(1,1): dist 1
        (1,0)-(1,1): dist 1
        Sum = 1+1+2+2+1+1 = 8.
        
        My formula gave 2. Why?
        Ah, the formula $\sum_{p} p(L-p) \binom{L-2}{k-2}$ calculates the sum of distances for ONE dimension assuming we are summing over ALL pairs in that dimension.
        But in the 2D case, the distance is $|x_1-x_2| + |y_1-y_2|$.
        The sum over all arrangements is (Sum of row diffs) + (Sum of col diffs).
        My calculation for rows ($L=2, k=2$):
        $\binom{2-2}{2-2} \times \sum_{p=1}^{1} p(2-p) = 1 \times 1 = 1$.
        This means the sum of row differences over all 6 arrangements is 1?
        Let's check row diffs manually:
        (0,0)-(0,1): 0
        (0,0)-(1,0): 1
        (0,0)-(1,1): 1
        (0,1)-(1,0): 1
        (0,1)-(1,1): 1
        (1,0)-(1,1): 0
        Sum = 0+1+1+1+1+0 = 4.
        My formula gave 1. Where is the factor of 4?
        Ah, $\binom{L-2}{k-2}$ is the number of ways to place the *remaining* $k-2$ pieces.
        But in the derivation:
        Total Sum = $\sum_{p} (\text{# pairs crossing } p \text{ across all arrangements})$.
        # pairs crossing $p$ = (ways to pick 1 left) * (ways to pick 1 right) * (ways to pick remaining $k-2$).
        Ways to pick 1 left from $p$: $\binom{p}{1} = p$.
        Ways to pick 1 right from $L-p$: $\binom{L-p}{1} = L-p$.
        Ways to pick remaining $k-2$: $\binom{L-2}{k-2}$.
        So count = $p(L-p) \binom{L-2}{k-2}$.
        For $L=2, k=2$: $p=1$. Count = $1(1) \binom{0}{0} = 1$.
        This implies there is only 1 pair crossing the boundary between row 0 and 1 across all arrangements?
        But there are 4 arrangements with row diff 1. Each has 1 pair. So 4 pairs.
        Why did the formula give 1?
        Because $\binom{L-2}{k-2} = \binom{0}{0} = 1$.
        The issue is that when $k=2$, "remaining $k-2$" is 0.
        The logic holds: Pick 1 left, 1 right. That's 2 pieces. Remaining 0.
        So for each $p$, we count how many arrangements have a pair crossing $p$.
        For $L=2, k=2$, pairs crossing $p=1$:
        Left set: {0}, Right set: {1}.
        We must pick one from left (only 0) and one from right (only 1).
        So the pair is (0,1).
        Number of ways to pick remaining 0 pieces from remaining 0 spots: 1.
        So there is 1 arrangement where the pair crosses $p=1$?
        No! The arrangement is defined by the set of $k$ positions.
        If $k=2$, the arrangement IS the pair.
        The pair (0,1) crosses $p=1$.
        Is there only 1 such pair? Yes, in 1D with 2 points, there is only 1 pair.
        But in 2D, we have $m \times n$ cells.
        The row dimension has $m$ slots. We choose $k$ rows.
        For $m=2, n=2, k=2$:
        We choose 2 rows out of 2. Only 1 way to choose rows: {0, 1}.
        So for every arrangement, the set of rows is {0, 1}.
        The row distance is always $|0-1| = 1$.
        There are $\binom{4}{2} = 6$ arrangements.
        So sum of row distances = $6 \times 1 = 6$.
        My formula gave 1.
        The formula $\binom{L-2}{k-2}$ assumes we are summing over arrangements of the 1D line ONLY.
        But the problem is 2D. The number of arrangements in 2D is $\binom{mn}{k}$.
        The row configuration is independent of the column configuration?
        No, we choose $k$ cells from $mn$.
        However, we can think of it as:
        Total Sum = $\sum_{\text{arrangements}} \sum_{\text{pairs}} (|r_1-r_2| + |c_1-c_2|)$.
        = $\sum_{\text{arrangements}} \sum_{\text{pairs}} |r_1-r_2| + \sum_{\text{arrangements}} \sum_{\text{pairs}} |c_1-c_2|$.
        Consider the first term.
        For a fixed pair of rows $r_a, r_b$, how many arrangements have pieces at $(r_a, c_x)$ and $(r_b, c_y)$?
        This seems complicated because the columns matter for the count.
        
        Alternative View:
        The set of chosen cells is $S \subset \text{Grid}, |S|=k$.
        Sum = $\sum_{S} \sum_{\{u,v\} \subset S} (|u_r - v_r| + |u_c - v_c|)$.
        By symmetry, the contribution of row differences and column differences are independent in terms of counting?
        Actually, we can iterate over all pairs of cells $(u, v)$ in the grid.
        Let $u = (r_u, c_u)$ and $v = (r_v, c_v)$.
        Distance $D(u,v) = |r_u - r_v| + |c_u - c_v|$.
        How many arrangements contain both $u$ and $v$?
        We need to choose $k-2$ more cells from the remaining $mn-2$ cells.
        Count = $\binom{mn-2}{k-2}$.
        Total Sum = $\sum_{u, v} \binom{mn-2}{k-2} D(u,v)$.
        = $\binom{mn-2}{k-2} \sum_{u, v} (|r_u - r_v| + |c_u - c_v|)$.
        = $\binom{mn-2}{k-2} [ \sum_{u, v} |r_u - r_v| + \sum_{u, v} |c_u - c_v| ]$.
        
        Now, $\sum_{u, v} |r_u - r_v|$ sums over all pairs of cells in the grid.
        This is equivalent to: for each pair of rows $(i, j)$, how many pairs of cells have row indices $i$ and $j$?
        For a fixed pair of rows $i, j$ ($i \neq j$), there are $n$ cells in row $i$ and $n$ cells in row $j$.
        Number of pairs $(u, v)$ with $u \in \text{row } i, v \in \text{row } j$ is $n \times n = n^2$.
        Also pairs where both are in row $i$? Distance is 0.
        So $\sum_{u, v} |r_u - r_v| = \sum_{i=0}^{m-1} \sum_{j=0}^{m-1} n^2 |i - j|$.
        = $2 n^2 \sum_{0 \le i < j < m} (j - i)$.
        Similarly for columns: $\sum_{u, v} |c_u - c_v| = 2 m^2 \sum_{0 \le c_1 < c_2 < n} (c_2 - c_1)$.
        
        Let $S_m = \sum_{0 \le i < j < m} (j - i)$.
        This is a standard sum.
        $\sum_{i=0}^{m-1} \sum_{j=i+1}^{m-1} (j-i) = \sum_{d=1}^{m-1} d \times (m-d)$.
        Because there are $m-d$ pairs with difference $d$.
        So Total Sum = $\binom{mn-2}{k-2} \times 2 [ n^2 S_m + m^2 S_n ]$.
        Where $S_L = \sum_{d=1}^{L-1} d(L-d)$.
        
        Let's re-verify with Example 1: m=2, n=2, k=2.
        $mn=4, k=2$. $\binom{2}{0} = 1$.
        $S_2 = \sum_{d=1}^{1} d(2-d) = 1(1) = 1$.
        Term rows: $n^2 S_m = 2^2 \times 1 = 4$.
        Term cols: $m^2 S_n = 2^2 \times 1 = 4$.
        Total = $1 \times 2 \times (4 + 4) = 16$.
        Expected 8.
        Why 16?
        Ah, the sum $\sum_{u, v}$ includes both $(u,v)$ and $(v,u)$.
        The problem says "every pair of pieces". Usually "pair" implies unordered pair $\{u, v\}$.
        My sum $\sum_{u, v}$ iterates over ordered pairs.
        So I should divide by 2.
        Total = $\binom{mn-2}{k-2} \times [ n^2 S_m + m^2 S_n ]$.
        Recalculate: $1 \times (4 + 4) = 8$. Matches!
        
        Example 2: m=1, n=4, k=3.
        $mn=4, k=3$. $\binom{2}{1} = 2$.
        $S_1 = 0$ (sum from 1 to 0).
        $S_4 = \sum_{d=1}^{3} d(4-d) = 1(3) + 2(2) + 3(1) = 3 + 4 + 3 = 10$.
        Term rows: $n^2 S_m = 4^2 \times 0 = 0$.
        Term cols: $m^2 S_n = 1^2 \times 10 = 10$.
        Total = $2 \times (0 + 10) = 20$. Matches!
        
        **Algorithm:**
        1. Calculate $N = m \times n$.
        2. Calculate $W = \binom{N-2}{k-2} \pmod{10^9+7}$.
        3. Calculate $S_m = \sum_{d=1}^{m-1} d(m-d) \pmod{MOD}$.
           - This is $\sum_{d=1}^{m-1} (md - d^2) = m \frac{(m-1)m}{2} - \frac{(m-1)m(2m-1)}{6}$.
           - Can use formula for sum of first $k$ integers and squares.
           - $S_m = \frac{m(m-1)(m-2)}{6}$? Let's check.
             $\sum_{d=1}^{m-1} (md - d^2) = m \binom{m}{2} - \sum_{d=1}^{m-1} d^2$.
             $\sum_{d=1}^{m-1} d = \frac{(m-1)m}{2}$.
             $\sum_{d=1}^{m-1} d^2 = \frac{(m-1)m(2m-1)}{6}$.
             $S_m = \frac{m^2(m-1)}{2} - \frac{(m-1)m(2m-1)}{6} = \frac{m(m-1)}{6} [3m - (2m-1)] = \frac{m(m-1)(m+1)}{6} = \frac{m(m^2-1)}{6}$.
             Check $m=2$: $2(3)/6 = 1$. Correct.
             Check $m=4$: $4(15)/6 = 10$. Correct.
        4. Calculate $S_n = \frac{n(n^2-1)}{6}$.
        5. Result = $W \times (n^2 S_m + m^2 S_n) \pmod{MOD}$.
        6. Handle modular inverse for division by 6.
        
        **Constraints:**
        $m, n \le 10^5$, $mn \le 10^5$.
        Wait, if $mn \le 10^5$, then $m$ and $n$ cannot both be large. One is small, or both are $\sqrt{10^5} \approx 316$.
        So $O(m+n)$ or $O(1)$ is fine.
        We need combinations $\binom{N-2}{k-2}$. Since $N \le 10^5$, we can precompute factorials or compute on the fly.
        Modulo is $10^9+7$.
        
        **Pitfalls:**
        - $k=2$: $\binom{N-2}{0} = 1$. Formula works.
        - $k > N$: Problem constraints say $k \le mn$, so valid.
        - $m=1$ or $n=1$: Sum formula gives 0, which is correct.
        - Modular arithmetic for negative numbers (not an issue here as terms are positive).
        - Division by 6 requires modular inverse.
        - Large numbers before modulo? Python handles large ints automatically, so just apply mod at the end or intermediate steps.
        
        **Complexity:**
        Time: $O(1)$ with precomputed factorials or $O(N)$ to compute factorial if not precomputed. Given constraints, $O(N)$ is trivial.
        Space: $O(N)$ for factorials or $O(1)$ if computed directly.

## worker: Implement the solution using the derived formula: 
1.  **Formula Derivation**:
    *   The problem asks for the sum of Manhattan distances over all $\binom{mn}{k}$ arrangements.
    *   By linearity of expectation (or summation), the total sum is the sum of distances for each pair of cells $(u, v)$ multiplied by the number of arrangements containing both $u$ and $v$.
    *   The number of arrangements containing a specific pair of distinct cells is $\binom{mn-2}{k-2}$.
    *   The sum of Manhattan distances over all ordered pairs of cells in the grid is $\sum_{u, v} (|r_u - r_v| + |c_u - c_v|)$.
    *   Due to symmetry, this splits into row contributions and column contributions.
    *   Row contribution: For every pair of rows $i, j$, there are $n^2$ pairs of cells with these row indices. The sum of $|i-j|$ over all pairs of rows is $S_m = \sum_{0 \le i < j < m} (j-i) = \frac{m(m^2-1)}{6}$. Total row sum over all cell pairs is $n^2 \times 2 \times S_m$ (factor of 2 for ordered pairs).
    *   Similarly, column contribution is $m^2 \times 2 \times S_n$.
    *   Since the problem asks for unordered pairs ("every pair of pieces"), we divide the ordered sum by 2.
    *   Final Formula: $\binom{mn-2}{k-2} \times (n^2 S_m + m^2 S_n)$.
    *   Where $S_L = \frac{L(L^2-1)}{6}$.

2.  **Implementation Details**:
    *   **Modular Arithmetic**: All calculations are performed modulo $10^9 + 7$.
    *   **Combinations**: Since $mn \le 10^5$, we precompute factorials and their modular inverses in $O(mn)$ time to compute $\binom{n}{r}$ in $O(1)$.
    *   **Edge Cases**:
        *   If $m=1$ or $n=1$, the sum for that dimension is 0 (handled by the formula $L(L^2-1)/6$ which yields 0 for $L=1$).
        *   If $k=2$, $\binom{mn-2}{0} = 1$.
        *   Constraints ensure $mn \ge 2$ and $k \ge 2$.

3.  **Complexity**:
    *   Time: $O(mn)$ for precomputing factorials. Given $mn \le 10^5$, this is well within limits.
    *   Space: $O(mn)$ for storing factorials.

## worker: Implement the `distanceSum` method in Python, incl
The solution leverages the linearity of expectation and combinatorial identities to solve the problem in $O(mn)$ time (dominated by factorial precomputation) and $O(1)$ space relative to the grid dimensions after precomputation.

1.  **Decomposition**: The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ allows us to calculate the total sum by independently summing the contributions of row differences and column differences.
2.  **Pair Contribution**: Instead of iterating over all arrangements, we iterate over all possible pairs of cells $(u, v)$ in the grid. For any specific pair of cells, the number of valid arrangements containing both is $\binom{mn-2}{k-2}$.
3.  **Summation**:
    *   The sum of row differences $|r_u - r_v|$ over all pairs of cells $(u, v)$ is $n^2 \times \sum_{0 \le i < j < m} (j-i)$.
    *   The sum of column differences $|c_u - c_v|$ over all pairs of cells $(u, v)$ is $m^2 \times \sum_{0 \le c_1 < c_2 < n} (c_2-c_1)$.
    *   The inner sums $\sum_{0 \le i < j < L} (j-i)$ simplify to $\frac{L(L^2-1)}{6}$.
4.  **Final Formula**: Total Sum = $\binom{mn-2}{k-2} \times (n^2 S_m + m^2 S_n)$, where $S_L = \frac{L(L^2-1)}{6}$.
5.  **Modular Arithmetic**: All calculations are performed modulo $10^9 + 7$. Modular inverse is used for division by 6 and for computing combinations.

## worker: Test the solution against the provided examples (m
The solution implements the derived combinatorial formula:
$$ \text{Total Sum} = \binom{mn-2}{k-2} \times \left( n^2 \frac{m(m^2-1)}{6} + m^2 \frac{n(n^2-1)}{6} \right) $$

**Reasoning:**
1.  **Decomposition**: The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ allows separating the problem into row and column contributions.
2.  **Pair Contribution**: Instead of summing over all $\binom{mn}{k}$ arrangements, we sum over all possible pairs of cells $(u, v)$ in the grid. For any specific pair of distinct cells, there are $\binom{mn-2}{k-2}$ ways to complete the arrangement with the remaining $k-2$ pieces.
3.  **Sum of Distances**:
    *   The sum of row differences $|r_u - r_v|$ over all pairs of cells is $n^2 \times \sum_{0 \le i < j < m} (j-i)$.
    *   The sum of column differences $|c_u - c_v|$ over all pairs of cells is $m^2 \times \sum_{0 \le c_1 < c_2 < n} (c_2-c_1)$.
    *   The inner sum $\sum_{0 \le i < j < L} (j-i)$ simplifies to $\frac{L(L^2-1)}{6}$.
4.  **Implementation**:
    *   Precompute factorials and modular inverses to compute combinations in $O(1)$.
    *   Compute the row and column sums using the closed-form formula.
    *   Combine terms modulo $10^9 + 7$.

**Edge Cases Handled**:
*   $m=1$ or $n=1$: The formula $L(L^2-1)/6$ correctly yields 0.
*   $k=2$: $\binom{mn-2}{0} = 1$, which is correct.
*   Large inputs: Modular arithmetic ensures no overflow.

## worker: Implement the `distanceSum` method in Python, incl
The solution uses a combinatorial approach to solve the problem efficiently.
1.  **Decomposition**: The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ allows us to separate the problem into row and column contributions.
2.  **Pair Contribution**: Instead of iterating over all $\binom{mn}{k}$ arrangements, we iterate over all possible pairs of cells $(u, v)$ in the grid. For any specific pair of distinct cells, there are $\binom{mn-2}{k-2}$ ways to complete the arrangement with the remaining $k-2$ pieces.
3.  **Sum of Distances**:
    *   The sum of row differences $|r_u - r_v|$ over all pairs of cells is $n^2 \times \sum_{0 \le i < j < m} (j-i)$.
    *   The sum of column differences $|c_u - c_v|$ over all pairs of cells is $m^2 \times \sum_{0 \le c_1 < c_2 < n} (c_2-c_1)$.
    *   The inner sum $\sum_{0 \le i < j < L} (j-i)$ simplifies to $\frac{L(L^2-1)}{6}$.
4.  **Implementation**:
    *   Precompute factorials and modular inverse factorials to compute combinations in $O(1)$.
    *   Compute the row and column sums using the closed-form formula.
    *   Combine terms modulo $10^9 + 7$.

**Edge Cases Handled**:
*   $m=1$ or $n=1$: The formula $L(L^2-1)/6$ correctly yields 0.
*   $k=2$: $\binom{mn-2}{0} = 1$, which is correct.
*   Large inputs: Modular arithmetic ensures no overflow.

## worker: finalize
The solution derives the total sum of Manhattan distances by considering the contribution of every possible pair of cells in the grid.
1.  **Combinatorial Logic**: Instead of iterating over all $\binom{mn}{k}$ arrangements, we iterate over all pairs of cells $(u, v)$. For any specific pair of distinct cells, the number of valid arrangements containing both is $\binom{mn-2}{k-2}$.
2.  **Distance Summation**: The sum of Manhattan distances over all pairs of cells is decomposed into row and column components.
    *   Row component: Sum of $|r_u - r_v|$ over all pairs. This equals $n^2 \times \sum_{0 \le i < j < m} (j-i)$.
    *   Column component: Sum of $|c_u - c_v|$ over all pairs. This equals $m^2 \times \sum_{0 \le c_1 < c_2 < n} (c_2-c_1)$.
3.  **Closed Form**: The inner sum $\sum_{0 \le i < j < L} (j-i)$ simplifies to $\frac{L(L^2-1)}{6}$.
4.  **Final Formula**: Total Sum = $\binom{mn-2}{k-2} \times (n^2 S_m + m^2 S_n)$.
5.  **Implementation**: Precomputes factorials for $O(1)$ combination calculation. Handles modular arithmetic for large numbers.
