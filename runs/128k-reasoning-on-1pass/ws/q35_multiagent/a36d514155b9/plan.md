1. Derive a closed-form expression for the sum of Manhattan distances between all distinct pairs of cells in an $m \times n$ grid, which simplifies to $D = \frac{N(m+n)(N-1)}{6}$ where $N = m \times n$.
2. Observe that each specific pair of cells appears in exactly $\binom{N-2}{k-2}$ valid arrangements of $k$ pieces.
3. The total answer is the product of $D$ and $\binom{N-2}{k-2}$, computed modulo $10^9 + 7$.
4. Implement modular arithmetic to handle division by 6 via modular inverse, and compute combinations efficiently using precomputed modular inverses or iterative multiplication.
5. Ensure all intermediate multiplications are taken modulo $10^9 + 7$ to prevent overflow and maintain $O(k)$ time complexity, which fits well within the constraints.