
## ideation
**Core Difficulty**: The problem requires calculating the sum of Manhattan distances between all pairs of pieces across all possible valid arrangements. A naive simulation or iterating over all pairs of cells is impossible due to constraints ($m \times n \le 10^5$, but the number of pairs can be up to $O((mn)^2)$). The key is to use combinatorial properties and linearity of expectation (or summation) to decouple the row and column contributions.

**Candidate Approaches**:
1.  **Decomposition**: Split Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ into row distance and column distance.
    *   Total Sum = (Sum of row distances over all pairs) + (Sum of column distances over all pairs).
    *   Since the grid is rectangular, the choice of rows and columns for the $k$ pieces are independent in terms of counting combinations, but the specific cells are chosen together.
    *   Actually, a more precise formulation: The total sum is $\sum_{\text{all arrangements}} \sum_{\{p_i, p_j\}} \text{dist}(p_i, p_j)$.
    *   By linearity, this equals $\sum_{\text{all pairs of distinct cells } (u, v)} \text{dist}(u, v) \times (\text{number of ways to place remaining } k-2 \text{ pieces})$.
    *   Number of ways to place remaining $k-2$ pieces in $mn-2$ cells is $\binom{mn-2}{k-2}$.
    *   So, Total Sum = $\binom{mn-2}{k-2} \times \left( \sum_{u, v} |u.r - v.r| + \sum_{u, v} |u.c - v.c| \right)$.

2.  **Calculating $\sum_{u, v} |u.r - v.r|$**:
    *   This sum iterates over all pairs of cells $(u, v)$ in the grid.
    *   If $u$ is in row $r_1$ and $v$ is in row $r_2$, the row distance is $|r_1 - r_2|$.
    *   For a fixed pair of rows $(r_1, r_2)$, there are $n \times n$ pairs of cells (one in each row).
    *   So, Row Sum = $\sum_{1 \le r_1 < r_2 \le m} |r_1 - r_2| \times n^2$.
    *   Similarly, Col Sum = $\sum_{1 \le c_1 < c_2 \le n} |c_1 - c_2| \times m^2$.

3.  **Efficient Calculation of $\sum_{i < j} |i - j|$**:
    *   For a line of length $L$, the sum of distances between all pairs is $\sum_{d=1}^{L-1} d \times (L-d)$.
    *   This can be derived as: Each gap of size 1 between index $i$ and $i+1$ is crossed by $(i) \times (L-i)$ pairs.
    *   Formula: $\frac{L(L^2 - 1)}{6}$.
    *   Let $S(L) = \frac{L(L^2-1)}{6}$.
    *   Row Contribution = $S(m) \times n^2$.
    *   Col Contribution = $S(n) \times m^2$.

4.  **Final Formula**:
    *   Total = $\binom{mn-2}{k-2} \times (S(m) \cdot n^2 + S(n) \cdot m^2) \pmod{10^9+7}$.
    *   Need to handle modular arithmetic for combinations and large numbers.

## worker: Implement `modInverse` using Fermat's Little Theor
1.  **Decomposition**: The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ is split into row and column components. The total sum over all arrangements is the sum of row contributions plus column contributions.
2.  **Linearity of Expectation / Summation**: Instead of iterating over arrangements, we iterate over pairs of cells $(u, v)$. For any specific pair of distinct cells, the number of valid arrangements where pieces are placed at $u$ and $v$ is $\binom{MN-2}{k-2}$.
3.  **Row/Column Contribution**:
    *   For rows: We sum $|r_1 - r_2|$ over all pairs of rows $(r_1, r_2)$. For each such pair of rows, there are $n \times n$ pairs of cells (one in each row). Thus, the contribution is $(\sum |r_1 - r_2|) \times n^2$.
    *   Similarly for columns: $(\sum |c_1 - c_2|) \times m^2$.
4.  **Efficient Calculation**: The sum of distances between all pairs in a line of length $L$ is given by $\frac{L(L^2-1)}{6}$. This is derived from the fact that a gap of size 1 between index $i$ and $i+1$ is crossed by $i \times (L-i)$ pairs. Summing $i(L-i)$ for $i=1$ to $L-1$ yields the formula.
5.  **Modular Arithmetic**: Since the result can be very large, all calculations are performed modulo $10^9 + 7$. Combinations are calculated using modular inverse for division.

## worker: [done] Implement `modInverse` using Fermat's Littl
The solution leverages the linearity of expectation and combinatorial properties to solve the problem efficiently.
1.  **Decomposition**: The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ is split into row and column components. The total sum over all arrangements is the sum of row contributions plus column contributions.
2.  **Linearity**: Instead of iterating over arrangements, we iterate over pairs of distinct cells $(u, v)$. For any specific pair of distinct cells, the number of valid arrangements where pieces are placed at $u$ and $v$ is $\binom{MN-2}{k-2}$.
3.  **Row/Column Contribution**:
    *   For rows: We sum $|r_1 - r_2|$ over all pairs of rows $(r_1, r_2)$. For each such pair of rows, there are $n \times n$ pairs of cells (one in each row). Thus, the contribution is $(\sum |r_1 - r_2|) \times n^2$.
    *   Similarly for columns: $(\sum |c_1 - c_2|) \times m^2$.
4.  **Efficient Calculation**: The sum of distances between all pairs in a line of length $L$ is given by $\frac{L(L^2-1)}{6}$. This is derived from the fact that a gap of size 1 between index $i$ and $i+1$ is crossed by $i \times (L-i)$ pairs. Summing $i(L-i)$ for $i=1$ to $L-1$ yields the formula.
5.  **Modular Arithmetic**: Since the result can be very large, all calculations are performed modulo $10^9 + 7$. Combinations are calculated using modular inverse for division.

The implementation includes:
- `modInverse`: Uses Fermat's Little Theorem ($a^{MOD-2} \pmod{MOD}$) since $MOD$ is prime.
- `nCr_mod`: Computes combinations modulo $MOD$ iteratively.
- `sum_dist_pairs`: Computes the sum of distances for a line of length $L$ using the closed-form formula.
- Main logic combines these to compute the final answer.

## worker: Return the final calculated result using the formu
The solution correctly implements the combinatorial logic derived in the plan:
1.  **Decomposition**: Manhattan distance is split into row and column components.
2.  **Linearity**: The total sum is the sum over all pairs of distinct cells $(u, v)$ of their distance multiplied by the number of ways to place the remaining $k-2$ pieces.
3.  **Combinatorics**: The number of ways to place remaining pieces is $\binom{MN-2}{k-2}$.
4.  **Distance Summation**:
    *   Row contribution: Sum of $|r_1 - r_2|$ over all row pairs multiplied by $n^2$ (since any column pair can be chosen). The sum of distances for a line of length $L$ is $L(L^2-1)/6$.
    *   Column contribution: Sum of $|c_1 - c_2|$ over all column pairs multiplied by $m^2$.
5.  **Modular Arithmetic**: All intermediate calculations are performed modulo $10^9 + 7$. Division by 6 is handled using modular inverse (Fermat's Little Theorem).
6.  **Edge Cases**: The code handles cases where $L < 2$ (returning 0) and ensures $nCr$ returns 0 if $r > n$.

The formula used is:
$$ \text{Result} = \binom{mn-2}{k-2} \times \left( \frac{m(m^2-1)}{6} \cdot n^2 + \frac{n(n^2-1)}{6} \cdot m^2 \right) \pmod{10^9+7} $$
