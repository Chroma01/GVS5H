1. Use the factorization $x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$. Let $d = x-y$ and $S = x^2 + xy + y^2$, so $d \cdot S = N$.
2. Iterate over all divisors $d$ of $N$. For each $d$, compute $S = N/d$.
3. From $d = x-y$, we have $x = y+d$. Substitute into $S$: $S = (y+d)^2 + (y+d)y + y^2 = 3y^2 + 3dy + d^2$.
4. Solve the quadratic equation $3y^2 + 3dy + (d^2 - S) = 0$ for $y$. Check if the discriminant is a perfect square and if the resulting $y$ is a positive integer.
5. If valid $y$ is found, compute $x = y+d$ and output $(x, y)$. If no divisor yields a solution, output -1.
6. Since $N \le 10^{18}$, iterate divisors up to $\sqrt{N}$ to keep complexity manageable ($O(\sqrt{N})$).