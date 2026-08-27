
## ideation
The core difficulty lies in efficiently finding integer solutions to $x^3 - y^3 = N$ for very large $N$ ($10^{18}$). A brute-force search for $x$ or $y$ is infeasible because $x$ can be up to $\approx 10^6$, but checking all pairs is too slow if not optimized.

The key insight is using the factorization $x^3 - y^3 = (x-y)(x^2 + xy + y^2)$. Let $d = x - y$. Then $x = y + d$. Substituting this into the equation gives $N = d(3y^2 + 3dy + d^2)$. This transforms the problem into:
1. Iterating over possible values of $d$. Since $d$ is a divisor of $N$, we can find all divisors by iterating up to $\sqrt{N}$.
2. For each divisor $d$, solving the quadratic equation $3y^2 + 3dy + (d^2 - N/d) = 0$ for $y$.
3. Checking if the solution $y$ is a positive integer.

Pitfalls to avoid:
- Floating point precision errors when checking for perfect squares or solving quadratics. Use integer arithmetic (e.g., integer square root) where possible.
- Missing divisors: Must check both $d$ and $N/d$.
- Ensuring $y > 0$. The quadratic formula might yield a negative root which should be discarded.
- Performance: Iterating up to $\sqrt{N} = 10^9$ is too slow for a 2-second time limit in Python. We need a more efficient approach or careful optimization. However, note that $d$ doesn't have to be small. But wait, $d = x-y$. If $d$ is large, then $x$ and $y$ are close? No, if $d$ is large, $x$ and $y$ are far apart.
Actually, let's re-evaluate the range of $d$.
$N = d(3y^2 + 3dy + d^2)$. Since $y \ge 1$, $3y^2 + 3dy + d^2 > d^2$. So $N > d^3$, which implies $d < N^{1/3}$.
For $N=10^{18}$, $d < 10^6$. This is very small!
So we only need to iterate $d$ from 1 up to $\lfloor N^{1/3} \rfloor$. For each $d$, we check if $d$ divides $N$. If it does, we solve for $y$.
This reduces the complexity significantly. We iterate $d$ from 1 to $10^6$. For each $d$, we do constant time checks. This is extremely fast.

Algorithm refinement:
1. Read $N$.
2. Iterate $d$ from 1 to $\lfloor N^{1/3} \rfloor + 1$ (safe upper bound).
3. If $N \% d == 0$:
    a. Let $K = N // d$.
    b. We need to solve $3y^2 + 3dy + d^2 = K$ for positive integer $y$.
    c. Rearrange: $3y^2 + 3dy + (d^2 - K) = 0$.
    d. Discriminant $D = (3d)^2 - 4(3)(d^2 - K) = 9d^2 - 12d^2 + 12K = 12K - 3d^2$.
    e. Check if $D \ge 0$ and is a perfect square. Let $S = \sqrt{D}$. If $S^2 \neq D$, continue.
    f. The roots are $y = \frac{-3d \pm S}{6}$. Since $y > 0$, we need $-3d + S > 0$, i.e., $S > 3d$.
    g. Check if $(-3d + S)$ is divisible by 6. If so, $y = (-3d + S) // 6$.
    h. If $y$ is a positive integer, then $x = y + d$. Print $x$ and $y$ and exit.
4. If no solution found after loop, print -1.

## worker: Implement the algorithm described in the notes: it
The solution leverages the factorization $x^3 - y^3 = (x-y)(x^2+xy+y^2)$. By setting $d = x-y$, the equation becomes $N = d(3y^2 + 3dy + d^2)$. Since $y \ge 1$, the term $(3y^2 + 3dy + d^2)$ is strictly greater than $d^2$, implying $N > d^3$. Therefore, $d$ must be less than $N^{1/3}$. For $N \le 10^{18}$, this means $d$ is at most $10^6$, allowing us to iterate through all possible values of $d$ efficiently.

For each divisor $d$ of $N$, we solve the quadratic equation $3y^2 + 3dy + (d^2 - N/d) = 0$ for $y$. We check if the discriminant is a perfect square and if the resulting root is a positive integer. If a valid pair $(x, y)$ is found, we print it and exit. Otherwise, we print -1. This approach is $O(N^{1/3})$ which is well within the time limits for $N=10^{18}$.
