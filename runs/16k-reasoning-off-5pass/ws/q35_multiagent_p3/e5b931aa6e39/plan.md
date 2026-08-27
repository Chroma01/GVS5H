1. Use the factorization $x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$. Let $d = x-y$ and $s = x^2 + xy + y^2$, so $d \cdot s = N$.
2. Iterate over all divisors $d$ of $N$. For each $d$, compute $s = N/d$.
3. From $d = x-y$, we have $x = y+d$. Substitute into $s$: $s = (y+d)^2 + (y+d)y + y^2 = 3y^2 + 3dy + d^2$.
4. Solve the quadratic equation $3y^2 + 3dy + (d^2 - s) = 0$ for $y$. Check if the discriminant $D = 9d^2 - 12(d^2 - s) = 12s - 3d^2$ is a perfect square and if the resulting $y$ is a positive integer.
5. If valid $y$ is found, compute $x = y+d$ and output $(x, y)$. If no divisor yields a solution, output -1.
6. Since $N \le 10^{18}$, iterate $d$ up to $\sqrt{N}$ to find all divisors efficiently.