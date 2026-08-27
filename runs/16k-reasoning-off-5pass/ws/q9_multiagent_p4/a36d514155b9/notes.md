
## ideation
**Core Difficulty:**
The problem requires summing Manhattan distances over *all* valid arrangements of $k$ identical pieces on an $m \times n$ grid. A naive simulation is impossible because the number of arrangements is $\binom{mn}{k}$, which can be astronomically large even for moderate $m, n$. The constraints $m, n \le 10^5$ but $m \times n \le 10^5$ suggest an $O(m \times n)$ or $O((m+n)\log(\dots))$ solution is needed.

**Key Insight:**
1.  **Linearity of Expectation / Decomposition:** The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ can be split into horizontal $|x_1 - x_2|$ and vertical $|y_1 - y_2|$ components. The total sum is the sum of horizontal contributions plus the sum of vertical contributions.
2.  **Symmetry:** The horizontal and vertical problems are independent and structurally identical. We can solve for a 1D line of length $L$ (where $L=m$ for rows, $L=n$ for columns) and multiply the result by the number of cells in the other dimension.
    *   Horizontal contribution: Consider two cells in the same row. There are $n$ choices for the column index for each of the two cells. Actually, it's simpler: Fix two distinct cells $(r, c_1)$ and $(r, c_2)$. The distance is $|c_1 - c_2|$. How many arrangements include these two specific cells?
    *   If we fix a pair of cells, the number of ways to place the remaining $k-2$ pieces in the remaining $N-2$ cells (where $N = m \times n$) is $\binom{N-2}{k-2}$.
    *   Therefore, Total Sum = $\sum_{\text{all pairs } \{u, v\}} \text{dist}(u, v) \times \binom{N-2}{k-2}$.
    *   This simplifies to: $\binom{N-2}{k-2} \times \sum_{\text{all pairs } \{u, v\}} \text{dist}(u, v)$.
3.  **Reducing to 1D:**
    *   Total Sum = $\binom{N-2}{k-2} \times [ \text{Sum of horizontal distances between all pairs of cells} + \text{Sum of vertical distances between all pairs of cells} ]$.
    *   Let's analyze the sum of horizontal distances between all pairs of cells in the grid.
        *   For any two cells $(r_1, c_1)$ and $(r_2, c_2)$, the horizontal distance is $|c_1 - c_2|$.
        *   This value depends only on the column indices.
        *   We can iterate over all pairs of columns $(c_1, c_2)$ with $1 \le c_1 < c_2 \le n$. The distance is $d = c_2 - c_1$.
        *   For a fixed pair of columns, how many pairs of cells have these column indices?
            *   We can choose any row for the first cell ($m$ choices) and any row for the second cell ($m$ choices). So $m^2$ pairs of cells share these column indices.
        *   Wait, the pair of cells must be distinct. Since $c_1 \neq c_2$, the cells are automatically distinct regardless of rows.
        *   So, for a fixed column distance $d$, there are $m^2$ pairs of cells with that horizontal separation.
        *   The sum of horizontal distances over all pairs of cells in the grid is: $m^2 \times \sum_{1 \le c_1 < c_2 \le n} (c_2 - c_1)$.
    *   Similarly, for vertical distances: $n^2 \times \sum_{1 \le r_1 < r_2 \le m} (r_2 - r_1)$.

**Algorithm Steps:**
1.  Calculate $N = m \times n$.
2.  Check if $k < 2$. If so, return 0 (though constraints say $k \ge 2$).
3.  Calculate the combinatorial factor $C = \binom{N-2}{k-2} \pmod{10^9+7}$. This requires modular inverse.
4.  Define a helper function `calc_1D_sum(L)` which computes $\sum_{1 \le i < j \le L} (j - i)$.
    *   Mathematical derivation: $\sum_{d=1}^{L-1} d \times (L-d)$.
    *   This sum can be computed in $O(1)$ using formulas for sums of integers and squares.
        *   $\sum_{d=1}^{L-1} d(L-d) = L \sum d - \sum d^2 = L \frac{(L-1)L}{2} - \frac{(L-1)L(2L-1)}{6}$.
5.  Total Horizontal Contribution = $m^2 \times \text{calc\_1D\_sum}(n)$.
6.  Total Vertical Contribution = $n^2 \times \text{calc\_1D\_sum}(m)$.
7.  Final Answer = $(C \times (\text{Horizontal} + \text{Vertical})) \pmod{10^9+7}$.

**Pitfalls:**
*   **Modulo Arithmetic:** All additions and multiplications must be done modulo $10^9+7$. Division (for combinations) must be done using modular inverse (Fermat's Little Theorem since the modulus is prime).
*   **Large Numbers:** Intermediate calculations like $m^2$ or the combinatorial sums can exceed 64-bit integers before modulo, so apply modulo at each step.
*   **Constraints:** $m \times n \le 10^5$ is small enough for $O(N)$ or $O(1)$ math, but $m, n$ individually can be up to $10^5$. The $O(1)$ math formula is crucial.
*   **Edge Cases:** $k=2$ (then $\binom{N-2}{0}=1$), $k=N$ (then $\binom{N-2}{N-2}=1$). The formula should hold.

**Candidate Approaches:**
1.  **Mathematical Derivation (Preferred):** Use the linearity of expectation and the closed-form sum formula derived above. Complexity: $O(1)$ or $O(\log MOD)$ for modular inverse.
2.  **Iterative Summation:** Iterate $d$ from 1 to $\max(m, n)$ and sum up. Since $m \times n \le 10^5$, $\max(m, n)$ can be $10^5$. This is $O(\max(m, n))$, which is acceptable but less elegant than $O(1)$. Given the constraints, $O(1)$ is safer and preferred.

## worker: Implement the `distanceSum` method using the deriv
The solution leverages the linearity of expectation and the symmetry of the grid to decompose the problem into two independent 1D problems (horizontal and vertical distances). 
1.  **Combinatorial Factor**: The number of valid arrangements where a specific pair of cells is occupied is $\binom{mn-2}{k-2}$. This factor is constant for all pairs of cells.
2.  **1D Summation**: The sum of distances between all pairs of cells in a 1D line of length $L$ is derived as $\sum_{d=1}^{L-1} d(L-d)$. This simplifies to $L \cdot \frac{L(L-1)}{2} - \frac{L(L-1)(2L-1)}{6}$.
3.  **Grid Scaling**: In a 2D grid, for any pair of columns separated by distance $d$, there are $m^2$ pairs of cells (since rows can be chosen independently). Similarly, for rows, there are $n^2$ pairs.
4.  **Modular Arithmetic**: All calculations are performed modulo $10^9 + 7$. Division is handled using modular inverse via Fermat's Little Theorem since the modulus is prime.
5.  **Complexity**: The solution runs in $O(\log MOD)$ time due to the modular exponentiation for inverses, which is extremely efficient given the constraints.

## worker: Verify edge cases (e.g., $k=2$, $k=mn$, $m=1$ or $
The solution implements the mathematical derivation discussed in the plan:
1.  **Decomposition**: The Manhattan distance is split into horizontal and vertical components.
2.  **Combinatorics**: The number of valid arrangements containing any specific pair of cells is $\binom{mn-2}{k-2}$. This is calculated using modular arithmetic and Fermat's Little Theorem for the inverse.
3.  **1D Summation**: The sum of distances between all pairs in a 1D line of length $L$ is derived in $O(1)$ using the formula $\sum_{d=1}^{L-1} d(L-d)$.
4.  **Scaling**: The 1D sum is scaled by $m^2$ for horizontal distances (since there are $m$ choices for the row of each cell in a pair of columns) and by $n^2$ for vertical distances.
5.  **Edge Cases**:
    *   $k=2$: $\binom{N-2}{0} = 1$, which is correct (we just sum distances over all pairs).
    *   $k=mn$: $\binom{N-2}{N-2} = 1$, correct (only one arrangement, sum over all pairs).
    *   $m=1$ or $n=1$: The grid becomes a line. One of the sums (horizontal or vertical) will be 0 because the dimension length is 1, and `calc_1D_sum(1)` returns 0. The other sum is scaled by $1^2$, effectively solving the 1D problem correctly.
    *   Large inputs: All intermediate calculations are modulo $10^9+7$, preventing overflow. The complexity is dominated by the modular inverse calculation, which is $O(\log MOD)$, well within time limits.
