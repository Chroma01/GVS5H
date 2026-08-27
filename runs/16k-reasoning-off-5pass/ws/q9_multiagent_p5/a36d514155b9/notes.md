
## ideation
The core difficulty lies in efficiently calculating the sum of Manhattan distances over all pairs of cells, weighted by the number of ways to complete the arrangement with the remaining pieces. The key insight is that the problem can be decomposed into independent row and column contributions due to the properties of Manhattan distance ($|x_1 - x_2| + |y_1 - y_2|$).

1.  **Decomposition**: The total sum is the sum of row distances plus the sum of column distances.
    *   **Row Contribution**: For any two rows $i$ and $j$, the distance is $|i - j|$. There are $n$ columns, so there are $n^2$ pairs of cells between row $i$ and row $j$ (one in row $i$, one in row $j$). The total row distance sum over all cell pairs is $n^2 \times \sum_{1 \le i < j \le m} (j - i)$.
    *   **Column Contribution**: Similarly, for any two columns $i$ and $j$, the distance is $|i - j|$. There are $m$ rows, so there are $m^2$ pairs of cells between column $i$ and column $j$. The total column distance sum over all cell pairs is $m^2 \times \sum_{1 \le i < j \le n} (j - i)$.

2.  **Combinatorial Weighting**:
    *   The problem asks for the sum over all *valid arrangements* of $k$ pieces.
    *   Consider a specific pair of distinct cells $(u, v)$. How many arrangements include pieces at both $u$ and $v$?
        *   We fix pieces at $u$ and $v$.
        *   We need to place the remaining $k-2$ pieces in the remaining $mn - 2$ cells.
        *   The number of ways is $\binom{mn - 2}{k - 2}$.
    *   This count is constant for *every* pair of distinct cells $(u, v)$.
    *   Therefore, the total answer is:
        $$ \text{Total Sum} = \binom{mn - 2}{k - 2} \times \left( \sum_{\text{all pairs } (u, v)} \text{dist}(u, v) \right) $$
    *   Note: If $k < 2$, the answer is 0, but constraints say $k \ge 2$.

3.  **Efficient Calculation**:
    *   Calculate $S_m = \sum_{1 \le i < j \le m} (j - i)$. This can be derived using summation formulas:
        $$ S_m = \sum_{d=1}^{m-1} d \times (m - d) = m \sum d - \sum d^2 $$
        Using $\sum_{i=1}^N i = \frac{N(N+1)}{2}$ and $\sum_{i=1}^N i^2 = \frac{N(N+1)(2N+1)}{6}$.
    *   Similarly calculate $S_n$ for columns.
    *   Total Cell Distance Sum = $n^2 S_m + m^2 S_n$.
    *   Multiply by $\binom{mn - 2}{k - 2} \pmod{10^9+7}$.

4.  **Pitfalls**:
    *   **Modulo Arithmetic**: All intermediate calculations (sums, combinations) must be done modulo $10^9 + 7$. Division for combinations requires modular inverse.
    *   **Large Inputs**: $m, n$ up to $10^5$, so $O(m+n)$ or $O(1)$ calculation is required. The formula approach is $O(1)$.
    *   **Edge Cases**: $k=2$ (then we choose 0 from remaining), $k > mn$ (impossible by constraints), $m=1$ or $n=1$ (one dimension sum is 0).
    *   **Integer Overflow**: Python handles large integers automatically, but we must apply modulo at each step to keep numbers manageable if porting to other languages, and strictly for the problem requirement.

## worker: Implement the helper functions for modular inverse
1.  **Decomposition**: The Manhattan distance $|x_1 - x_2| + |y_1 - y_2|$ allows us to separate the problem into row and column components.
2.  **Combinatorial Logic**: For any specific pair of distinct cells $(u, v)$, the number of valid arrangements containing pieces at both $u$ and $v$ is $\binom{mn-2}{k-2}$. This value is constant for all pairs. Thus, the total sum is $\binom{mn-2}{k-2} \times \sum_{u, v} \text{dist}(u, v)$.
3.  **Sum of Differences**: The sum of distances between all pairs of indices in a range $[1, L]$ is calculated efficiently using the formula $\sum_{d=1}^{L-1} d(L-d) = L \sum d - \sum d^2$. This avoids an $O(L^2)$ loop.
4.  **Modulo Arithmetic**: All calculations involving large numbers are performed modulo $10^9 + 7$. Modular inverse is used for division in the combination formula.
5.  **Complexity**: The solution runs in $O(1)$ time (excluding the modular inverse which is $O(\log MOD)$) and $O(1)$ space, satisfying the constraints where $m, n \le 10^5$.
