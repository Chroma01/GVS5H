
## ideation
The core difficulty lies in efficiently finding integer solutions to $x^3 - y^3 = N$ for very large $N$ (up to $10^{18}$). A brute-force search for $x$ or $y$ is infeasible because $x$ can be up to $\approx 10^6$, but checking all pairs is too slow if not optimized.

The key insight is the factorization:
$$x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$$
Let $d = x - y$ and $S = x^2 + xy + y^2$. Then $d \cdot S = N$.
Since $x, y$ are positive integers, $d$ must be a positive divisor of $N$.
Also, since $x > y$ (as $N > 0$), $d \ge 1$.
Furthermore, $S = x^2 + xy + y^2 = (y+d)^2 + (y+d)y + y^2 = 3y^2 + 3dy + d^2$.
This gives a quadratic equation in terms of $y$:
$$3y^2 + 3dy + (d^2 - S) = 0$$
For a fixed divisor $d$, we can compute $S = N/d$. We then check if this quadratic has a positive integer solution for $y$.
The discriminant of this quadratic is:
$$D = (3d)^2 - 4(3)(d^2 - S) = 9d^2 - 12d^2 + 12S = 12S - 3d^2$$
For $y$ to be an integer, $D$ must be a perfect square, say $k^2$, and $k$ must have the same parity as $3d$ (so that $-3d \pm k$ is even, allowing division by $6$ to yield an integer). Specifically, $y = \frac{-3d + k}{6}$. We require $y > 0$, so $k > 3d$.

Algorithm:
1. Find all divisors $d$ of $N$. Since $N \le 10^{18}$, we can iterate $i$ from $1$ to $\lfloor \sqrt{N} \rfloor$. If $i$ divides $N$, then both $i$ and $N/i$ are divisors.
2. For each divisor $d$:
   a. Calculate $S = N / d$.
   b. Calculate discriminant $D = 12S - 3d^2$.
   c. If $D < 0$, skip (no real solution).
   d. Check if $D$ is a perfect square. Let $k = \sqrt{D}$. If $k^2 \neq D$, skip.
   e. Check if $(-3d + k)$ is divisible by $6$ and positive.
      - Condition 1: $(-3d + k) \% 6 == 0$
      - Condition 2: $-3d + k > 0 \implies k > 3d$
   f. If conditions met, calculate $y = (-3d + k) / 6$ and $x = y + d$. Output $x, y$ and exit.
3. If no divisor yields a solution, output -1.

Pitfalls:
- Floating point precision when checking for perfect squares for large numbers ($D$ can be up to $\approx 12 \cdot 10^{18}$). Use integer square root algorithms or careful checking with `math.isqrt`.
- Performance: Iterating up to $\sqrt{N} = 10^9$ is too slow for Python in typical time limits (usually 2 seconds). We need a faster way to find divisors or optimize the search.
  - Wait, $10^9$ iterations is definitely too slow. We need a better approach.
  - Alternative approach: Since $x^3 - y^3 = N$, and $x > y$, we have $x \approx y$. Let $x = y + d$. Then $N = d(3y^2 + 3dy + d^2)$.
  - Note that $d = x - y$. Since $x^3 - y^3 = N$, we know $x \approx N^{1/3}$. The difference $d$ is usually small.
  - Actually, $d$ can be large if $y$ is small. But if $d$ is large, then $y$ must be small.
  - Let's bound $d$. Since $S = x^2 + xy + y^2 > 3y^2$, we have $N = d \cdot S > 3 d y^2$. Also $S < 3x^2$ roughly.
  - More importantly, $d$ is a divisor of $N$. The number of divisors can be large, but finding them by iterating to $\sqrt{N}$ is $O(\sqrt{N})$ which is $10^9$, too slow.
  - However, we don't need to iterate all divisors. We can iterate on $d$ directly? No, $d$ can be up to $N$.
  - Let's re-evaluate the bounds.
    $x^3 - y^3 = N$.
    If $d=1$, $3y^2 + 3y + 1 = N$. We can solve for $y$ directly.
    If $d$ is large, $y$ is small.
    Specifically, $N = d(3y^2 + 3dy + d^2)$.
    Since $y \ge 1$, $S = 3y^2 + 3dy + d^2 \ge 3 + 3d + d^2 > d^2$.
    So $N = d S > d^3 \implies d < N^{1/3}$.
    Wait, is this true?
    $S = x^2 + xy + y^2$. Since $x = y+d$, $S = 3y^2 + 3dy + d^2$.
    Clearly $S > d^2$ is not always true if $y$ is small?
    If $y=1$, $S = 3 + 3d + d^2$. Then $N = d(3 + 3d + d^2) = 3d + 3d^2 + d^3$.
    So $N > d^3$. Thus $d < N^{1/3}$.
    This is a crucial bound! $d$ ranges from $1$ to $\lfloor N^{1/3} \rfloor$.
    For $N = 10^{18}$, $N^{1/3} = 10^6$.
    Iterating $d$ from $1$ to $10^6$ is very fast.
    
    Revised Algorithm:
    1. Iterate $d$ from $1$ to $\lfloor N^{1/3} \rfloor + \text{small buffer}$. Actually, since $N > d^3$, $d$ can be at most $N^{1/3}$.
    2. For each $d$, check if $d$ divides $N$. If not, continue.
    3. If $d$ divides $N$, let $S = N // d$.
    4. Solve $3y^2 + 3dy + (d^2 - S) = 0$ for positive integer $y$.
       - Discriminant $D = 12S - 3d^2$.
       - Check if $D$ is a perfect square.
       - Check if solution $y$ is positive integer.
    5. If found, print and exit.
    6. If loop finishes without solution, print -1.

    This reduces complexity to $O(N^{1/3})$, which is $10^6$ operations, perfectly fine.

## worker: (omit)
The problem asks for positive integers $x, y$ such that $x^3 - y^3 = N$.
Using the factorization $x^3 - y^3 = (x-y)(x^2+xy+y^2) = N$, we let $d = x-y$ and $S = x^2+xy+y^2$.
Then $d \cdot S = N$.
Substituting $x = y+d$ into $S$, we get $S = 3y^2 + 3dy + d^2$.
This leads to the quadratic equation $3y^2 + 3dy + (d^2 - S) = 0$.
The discriminant is $D = 12S - 3d^2$.
For $y$ to be an integer, $D$ must be a perfect square, and $(-3d + \sqrt{D})$ must be divisible by 6 and positive.
Crucially, since $y \ge 1$, we have $S = 3y^2 + 3dy + d^2 > d^2$, which implies $N = dS > d^3$.
Thus, $d < N^{1/3}$.
For $N \le 10^{18}$, $N^{1/3} \le 10^6$. Iterating $d$ from 1 to $10^6$ is computationally feasible.
For each divisor $d$ of $N$ in this range, we check if the corresponding quadratic yields a valid positive integer $y$.
If found, we output $x=y+d$ and $y$. If no such $d$ is found, we output -1.
This approach has time complexity $O(N^{1/3})$, which is efficient enough.
