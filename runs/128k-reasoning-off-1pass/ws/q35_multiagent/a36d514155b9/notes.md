
## ideation
The problem asks for the sum of Manhattan distances between all pairs of pieces over all valid arrangements. The key insight is to use linearity of summation. Instead of iterating over all arrangements (which is infeasible), we consider the contribution of each pair of distinct cells $(c_1, c_2)$ to the total sum.

For any two distinct cells $c_1$ and $c_2$, the Manhattan distance $d(c_1, c_2)$ is added to the total sum for every valid arrangement that has pieces at both $c_1$ and $c_2$. The number of such arrangements is $\binom{N-2}{k-2}$, where $N = m \times n$ is the total number of cells. This is because we fix two pieces at $c_1$ and $c_2$, and choose $k-2$ positions from the remaining $N-2$ cells.

Thus, the total sum is:
$$ \text{Total Sum} = \binom{N-2}{k-2} \times \sum_{c_1 \neq c_2} d(c_1, c_2) $$

The sum $\sum_{c_1 \neq c_2} d(c_1, c_2)$ can be decomposed into x and y components:
$$ \sum_{c_1 \neq c_2} (|x_1 - x_2| + |y_1 - y_2|) = \sum_{c_1 \neq c_2} |x_1 - x_2| + \sum_{c_1 \neq c_2} |y_1 - y_2| $$

To compute $\sum_{c_1 \neq c_2} |x_1 - x_2|$:
- The x-coordinates range from $0$ to $m-1$, and each x-coordinate appears $n$ times (once for each column).
- We can compute the sum of absolute differences for all pairs of x-coordinates, considering multiplicity.
- Let $X$ be the list of x-coordinates for all $N$ cells: $[0, 0, ..., 0, 1, 1, ..., 1, ..., m-1, ..., m-1]$ where each value $i$ appears $n$ times.
- Sort $X$ (it's already sorted if generated in order).
- Use the formula: $\sum_{i<j} (x_j - x_i) = \sum_{i=0}^{N-1} x_i \cdot (2i - N + 1)$? Actually, a better way is:
  For a sorted array $A$, $\sum_{i<j} (A_j - A_i) = \sum_{i=0}^{N-1} A_i \cdot (i - (N - 1 - i)) = \sum_{i=0}^{N-1} A_i \cdot (2i - N + 1)$.
  But since we have duplicates, this formula still holds for the sum over all pairs.

Similarly for y-coordinates: each y-coordinate $j$ appears $m$ times.

So the algorithm is:
1. Compute $N = m \times n$.
2. If $k < 2$, return 0 (but constraints say $k \ge 2$).
3. Compute $\binom{N-2}{k-2} \pmod{10^9+7}$.
4. Compute sum of absolute differences for x-coordinates:
   - Generate the x-coordinate list implicitly: for row $i$ in $0..m-1$, there are $n$ cells with x-coordinate $i$.
   - Use the prefix sum technique or the formula above to compute $\sum_{c_1 < c_2} |x_1 - x_2|$.
   - Actually, the sum over all unordered pairs is what we need. The formula $\sum_{i<j} (A_j - A_i)$ gives the sum for all pairs.
5. Similarly for y-coordinates.
6. Total sum = $(\text{sum\_x} + \text{sum\_y}) \times \binom{N-2}{k-2} \pmod{10^9+7}$.

Pitfalls:
- Large numbers: use modulo arithmetic carefully. Note that the binomial coefficient and the sums can be large, so compute modulo $10^9+7$.
- The sum of absolute differences can be computed efficiently without generating the full list of $N$ coordinates if $N$ is large, but since $N \le 10^5$, generating the list is feasible.
- Ensure that the binomial coefficient is computed correctly, handling cases where $k-2 < 0$ or $k-2 > N-2$ (but constraints ensure $2 \le k \le N$).

## worker: Implement a helper function to compute combination
The solution uses linearity of summation. Instead of iterating over all arrangements, we consider the contribution of each pair of distinct cells. For any two distinct cells, the number of valid arrangements that place pieces at both cells is $\binom{N-2}{k-2}$ where $N = m \times n$. The total sum is then $\binom{N-2}{k-2} \times \sum_{c_1 \neq c_2} d(c_1, c_2)$.

The sum of Manhattan distances over all pairs of cells is decomposed into x and y components. For each component, we generate the list of coordinates for all $N$ cells. Since $N \le 10^5$, this is feasible. The sum of absolute differences for a sorted list can be computed in $O(N)$ using the formula $\sum_{i=0}^{N-1} A[i] \times (2i - N + 1)$.

We precompute factorials and inverse factorials modulo $10^9+7$ to compute combinations efficiently in $O(1)$ after $O(N)$ preprocessing.
