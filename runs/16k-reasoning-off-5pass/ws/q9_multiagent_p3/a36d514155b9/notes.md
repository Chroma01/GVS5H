
## ideation
**Core Difficulty**:
The problem requires calculating the sum of Manhattan distances between all pairs of $k$ pieces over all $\binom{N}{k}$ valid arrangements, where $N = m \times n$. A naive simulation or iterating over all arrangements is impossible due to constraints ($N$ up to $10^5$, so $\binom{N}{k}$ is huge). The key is to use linearity of expectation (or contribution technique) to separate the problem into independent X and Y dimensions.

**Key Insight**:
Manhattan Distance $D = |x_i - x_j| + |y_i - y_j|$.
The total sum over all arrangements is:
$$ \text{Total} = \sum_{\text{arrangements}} \sum_{1 \le i < j \le k} (|x_i - x_j| + |y_i - y_j|) $$
By symmetry and linearity, this equals:
$$ \binom{N-2}{k-2} \times \left( \sum_{\text{all pairs of cells } (c_1, c_2)} |x_{c_1} - x_{c_2}| + \sum_{\text{all pairs of cells } (c_1, c_2)} |y_{c_1} - y_{c_2}| \right) $$
Wait, strictly speaking, if we fix two specific cells $A$ and $B$, they contribute $|x_A - x_B| + |y_A - y_B|$ to the sum. How many arrangements contain both $A$ and $B$? Exactly $\binom{N-2}{k-2}$.
So, Total Sum = $\binom{N-2}{k-2} \times \sum_{A, B \in \text{Grid}, A \neq B} (|x_A - x_B| + |y_A - y_B|) / 2$ (since pairs are unordered).

## worker: Implement the `Solution` class with precomputed fa
1.  **Decomposition**: The Manhattan distance $|x_i - x_j| + |y_i - y_j|$ allows us to separate the problem into X and Y dimensions.
2.  **Linearity of Expectation / Contribution**: Instead of iterating over arrangements, we count how many times a specific pair of cells $(A, B)$ appears in all valid arrangements. This count is $\binom{N-2}{k-2}$, where $N = m \times n$.
3.  **Sum over Pairs**: We need to compute $\sum_{\{A, B\}} (|x_A - x_B| + |y_A - y_B|)$.
    *   For the X component: We sum $|x_A - x_B|$ over all unordered pairs of cells. Since the Y-coordinate doesn't affect the X-distance, we can group cells by their X-coordinate. If we pick two X-coordinates $i$ and $j$ ($i < j$), there are $n \times n$ pairs of cells with these X-coordinates. The distance is $j-i$. Summing this over all $0 \le i < j < m$ gives $S_x \times n^2$.
    *   Similarly for Y: $S_y \times m^2$.
4.  **Efficient Calculation**: $S_x$ is the sum of distances between all pairs in a 1D array of size $m$. This can be computed in $O(1)$ using the formula $\sum_{d=1}^{m-1} d(m-d)$.
5.  **Modular Arithmetic**: All calculations involving combinations and products are performed modulo $10^9 + 7$. Precomputing factorials allows $O(1)$ combination queries.

## worker: For X dimension: We sum $|x_A - x_B|$ over all uno
The solution decomposes the Manhattan distance problem into independent X and Y dimensions.
1.  **Combinatorics**: The total sum is the sum of distances for all pairs of cells multiplied by the number of ways to complete the arrangement ($\binom{N-2}{k-2}$).
2.  **1D Sum Calculation**: For a dimension of size $L$, the sum of distances between all unordered pairs of indices is calculated using the formula $\sum_{d=1}^{L-1} d(L-d)$. This is derived as $L \sum d - \sum d^2$.
3.  **Grid Scaling**: Since the grid has $n$ columns for each row (X-dimension), every pair of X-coordinates corresponds to $n \times n$ pairs of cells. Similarly, every pair of Y-coordinates corresponds to $m \times m$ pairs of cells.
4.  **Modular Arithmetic**: All intermediate calculations involving large numbers are performed modulo $10^9 + 7$. Factorials and their modular inverses are precomputed to allow $O(1)$ combination queries.
