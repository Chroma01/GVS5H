
## ideation
The core difficulty lies in efficiently solving the equation $x^3 - y^3 = N$ for large $N$ ($10^{18}$). A brute-force search for $x$ or $y$ is impossible because they can be up to $10^6$.

The key insight is the algebraic factorization:
$x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$.

Let $d = x - y$ and $s = x^2 + xy + y^2$. Then $d \cdot s = N$.
Since $x, y \ge 1$, we have $x > y$, so $d \ge 1$. Also, $s = x^2 + xy + y^2 > 0$.
From $d = x - y$, we get $x = y + d$.
Substituting $x$ into the expression for $s$:
$s = (y+d)^2 + (y+d)y + y^2$
$s = y^2 + 2dy + d^2 + y^2 + dy + y^2$
$s = 3y^2 + 3dy + d^2$

This gives us a quadratic equation in terms of $y$:
$3y^2 + 3dy + (d^2 - s) = 0$

For a given divisor $d$ of $N$, we can calculate $s = N/d$. We then check if this quadratic equation yields a positive integer solution for $y$.
The discriminant of this quadratic is:
$D = (3d)^2 - 4(3)(d^2 - s) = 9d^2 - 12d^2 + 12s = 12s - 3d^2$

For $y$ to be an integer, $D$ must be a perfect square, say $k^2$, and the numerator $-3d + k$ must be divisible by $2 \cdot 3 = 6$ (and result in a positive $y$).
Specifically, $y = \frac{-3d + \sqrt{12s - 3d^2}}{6}$.

Algorithm:
1. Iterate through all divisors $d$ of $N$. Since $N \le 10^{18}$, we can find divisors by iterating $i$ from $1$ up to $\lfloor \sqrt{N} \rfloor$. If $i$ divides $N$, then both $i$ and $N/i$ are divisors.
2. For each divisor $d$:
   a. Calculate $s = N / d$.
   b. Calculate discriminant $D = 12s - 3d^2$.
   c. If $D < 0$, skip.
   d. Check if $D$ is a perfect square. Let $k = \sqrt{D}$. If $k^2 \neq D$, skip.
   e. Check if $(-3d + k)$ is divisible by $6$ and positive.
      $y = (-3d + k) / 6$.
      If $y$ is a positive integer, then $x = y + d$ is a solution.
   f. If valid, print $x$ and $y$ and exit.
3. If no divisor yields a solution, print -1.

Pitfalls:
- Floating point precision issues when checking for perfect squares for large numbers ($10^{18}$). Use integer square root algorithms.
- Ensuring $y$ is a positive integer ($y \ge 1$).
- Efficiency: Iterating up to $10^9$ for $\sqrt{10^{18}}$ is too slow in Python if not optimized, but typically the number of divisors is small. However, iterating up to $10^9$ is definitely TLE. We need to be careful. Wait, $10^9$ iterations is too many.
- Actually, we don't need to iterate all numbers up to $\sqrt{N}$. We can iterate $d$ from $1$ to $\lfloor N^{1/3} \rfloor$? No, $d$ can be larger than $N^{1/3}$.
- But note that $s = x^2 + xy + y^2 \approx 3y^2$ and $d = x-y$. Also $N = d \cdot s$.
- Since $x > y \ge 1$, $d \ge 1$.
- Is there a bound on $d$?
  $s = 3y^2 + 3dy + d^2$. Since $y \ge 1$, $s \ge 3 + 3d + d^2$.
  So $N = d \cdot s \ge d(3 + 3d + d^2) = d^3 + 3d^2 + 3d$.
  This implies $d^3 < N$, so $d < N^{1/3}$.
  Therefore, we only need to iterate $d$ from $1$ to $\lfloor N^{1/3} \rfloor$.
  For $N=10^{18}$, $N^{1/3} = 10^6$, which is very fast.
  Wait, let's verify.
  $x^3 - y^3 = N$.
  If $d = x-y$, then $x = y+d$.
  $N = (y+d)^3 - y^3 = 3y^2d + 3yd^2 + d^3$.
  Since $y \ge 1$, $N \ge 3d + 3d^2 + d^3 > d^3$.
  So $d < N^{1/3}$.
  This is a crucial optimization. We only iterate $d$ from $1$ to $\lfloor N^{1/3} \rfloor$.

Corrected Algorithm:
1. Read $N$.
2. Iterate $d$ from $1$ to $\lfloor N^{1/3} \rfloor$ (inclusive, using integer arithmetic).
3. For each $d$, check if $N$ is divisible by $d$. If not, continue.
4. If divisible, let $s = N // d$.
5. Calculate $D = 12s - 3d^2$.
6. If $D < 0$, continue.
7. Check if $D$ is a perfect square. Let $k = \text{isqrt}(D)$. If $k^2 \neq D$, continue.
8. Check if $(-3d + k)$ is divisible by $6$ and positive.
   Let $num = -3d + k$.
   If $num > 0$ and $num \% 6 == 0$:
     $y = num // 6$
     $x = y + d$
     Print $x, y$ and exit.
9. If loop finishes without solution, print -1.

## worker: (None)
The solution leverages the algebraic identity $x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$. By setting $d = x-y$, we derived that $d$ must satisfy $d^3 < N$, limiting the search space for $d$ to approximately $N^{1/3}$. For $N \le 10^{18}$, this means iterating up to $10^6$, which is computationally efficient. For each divisor $d$ of $N$, we solve a quadratic equation for $y$ and check for integer solutions. The use of integer square root (`math.isqrt`) ensures precision for large numbers.
