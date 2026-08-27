1. Use the identity $x^3 - y^3 = (x-y)(x^2 + xy + y^2)$. Let $d = x - y$, then $x = y + d$.
2. Substitute to get $N = d((y+d)^2 + (y+d)y + y^2) = d(3y^2 + 3dy + d^2)$.
3. Iterate over all divisors $d$ of $N$. For each $d$, we need to solve $3y^2 + 3dy + d^2 = N/d$ for positive integer $y$.
4. This is a quadratic in $y$: $3y^2 + 3dy + (d^2 - N/d) = 0$. Use the quadratic formula and check if the discriminant is a perfect square and yields a positive integer solution.
5. Since $N \le 10^{18}$, we can iterate $d$ up to $\sqrt{N}$ to find all divisors. For each divisor $d$, check if it yields a valid $y$. If found, output $x = y+d$ and $y$. If no solution found after checking all divisors, output -1.