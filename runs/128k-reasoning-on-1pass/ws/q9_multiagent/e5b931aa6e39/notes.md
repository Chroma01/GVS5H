
## ideation
- **Core Difficulty**: The problem requires finding positive integers $x, y$ satisfying $x^3 - y^3 = N$ for $N$ up to $10^{18}$. A naive iteration over $x$ or $y$ is infeasible ($O(N)$ or $O(N^{1/3})$ with large constant).
- **Mathematical Insight**: Factorize the expression as $(x-y)(x^2+xy+y^2) = N$. Let $d = x-y$. Since $x > y \ge 1$, $d \ge 1$. Substituting $x = y+d$ yields a quadratic equation in $y$: $3dy^2 + 3d^2y + (d^3 - N) = 0$.
- **Algorithm**: Iterate over possible values of $d$. From the equation, $N = d(3y^2 + 3yd + d^2) \ge d(3 + 3d + d^2) > d^3$. Thus, $d < N^{1/3}$. For $N=10^{18}$, $d$ goes up to $10^6$, which is computationally feasible.
- **Validation**: For each $d$, calculate the discriminant of the quadratic. It must be a perfect square. The resulting $y$ must be a positive integer.
- **Constraints**: $N$ fits in 64-bit integer, but intermediate calculations (discriminant) can reach $\approx 10^{25}$, requiring arbitrary precision arithmetic (Python handles this natively). Floating-point `sqrt` may lose precision, so integer square root is necessary.
- **Pitfalls**: 
  - Floating point precision errors when checking for perfect squares.
  - Incorrect loop bound for $d$ (must ensure $d^3 < N$).
  - Checking $y \ge 1$ (since $y$ must be positive).

## worker: Read the integer $N$ from standard input.
- The problem asks for positive integers $x, y$ such that $x^3 - y^3 = N$.
- We factor the equation as $(x-y)(x^2+xy+y^2) = N$. Let $d = x-y$.
- Substituting $x = y+d$ yields a quadratic equation in $y$: $3dy^2 + 3d^2y + (d^3 - N) = 0$.
- For $y$ to be a positive integer, the discriminant $\Delta = 12dN - 3d^4$ must be a perfect square, and the resulting $y$ must be a positive integer.
- Since $y \ge 1$, $N > d^3$, so $d < N^{1/3}$. For $N=10^{18}$, $d < 10^6$, allowing iteration.
- Used integer square root to avoid floating point precision issues with large numbers.
- Time complexity $O(N^{1/3})$, space $O(1)$.
