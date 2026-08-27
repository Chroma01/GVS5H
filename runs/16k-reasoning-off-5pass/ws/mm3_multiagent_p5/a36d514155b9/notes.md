
## ideation
**Core difficulty:** Compute the sum of Manhattan distances over **all** unordered pairs of pieces, summed across **all** $\binom{mn}{k}$ valid arrangements, modulo $10^9+7$.

**Key insight — linearity & symmetry:**
- Total = $\sum_{\text{arrangements}} \sum_{\{i,j\} \in \text{arr}} (|x_i-x_j| + |y_i-y_j|)$
- Swap summation: for each cell-pair $(a,b)$, count how many arrangements contain both.
- Number of arrangements containing both given cells = $\binom{mn-2}{k-2}$ (choose the remaining $k-2$ pieces from the other $mn-2$ cells).

So the total becomes:
$$T = \binom{mn-2}{k-2} \cdot \sum_{\text{all cell pairs}} \big(|x_a - x_b| + |y_a - y_b|\big)$$

**Computing the cell-pair sum:**

- **Row distance contribution** = $\sum_{0 \le a < b < m} n^2 (b-a) = n^2 \cdot \frac{m(m^2-1)}{6}$
  (pair two cells in rows $a$ and $b$: $n$ cells each, so $n^2$ pairs, distance $b-a$).
- **Column distance contribution** = $\sum_{0 \le a < b < n} m^2 (b-a) = m^2 \cdot \frac{n(n^2-1)}{6}$.

**Final formula:**
$$\text{Answer} = \binom{mn-2}{k-2} \cdot \frac{m^2 n(n^2-1) + m n^2 (m^2-1)}{6} \pmod{10^9+7}$$

**Pitfalls:**
- $m,n \le 10^5$ but $mn \le 10^5$, so factorials up to $10^5$ suffice.
- Division by 6: use modular inverse under prime $10^9+7$.
- Edge cases: $m=1$ or $n=1$ work fine (one of the bracket terms becomes 0).
- $k=2$: answer should be exactly $\binom{mn-2}{0} \cdot (\text{cell-pair sum}) = \text{cell-pair sum}$; sanity check example 1 ($m=n=2,k=2$): $mn=4$, $S=4$, row-part = $4 \cdot 2\cdot 3/6 = 4$, col-part = $4 \cdot 2\cdot 3/6 = 4$, total = 8 ✓. Example 2 ($m=1,n=4,k=3$): $S=4$, row-part = 0, col-part = $1 \cdot 4\cdot 15/6 = 10$, $\binom{2}{1}=2$, total = 20 ✓.

**Approach summary:**
1. Precompute factorials and inverse factorials up to $mn$.
2. Compute $\binom{mn-2}{k-2} \bmod p$.
3. Compute the row and column pair-sum terms.
4. Multiply and apply $\bmod\, 10^9+7$.

## worker: Write the `Solution` class with `distanceSum` meth
- Used linearity: swap order of summation so each unordered cell-pair is counted with weight $\binom{mn-2}{k-2}$ (arrangements containing both cells).
- Row distance sum: $\sum_{0\le a<b<m} n^2 (b-a) = n^2 \cdot m(m^2-1)/6$. Same for columns with $m$ and $n$ swapped.
- Multiplied by modular inverse of 6 (prime modulus $10^9+7$). Factorials cached in class-level dict to avoid recomputation across multiple test invocations.
- Verified both given examples plus edge cases $k=mn$ and $k=2$ on $3\times3$ grid.
