
## ideation
The core difficulty lies in efficiently finding a pair $(x, y)$ for very large $N$ ($10^{18}$). A brute-force search for $x$ or $y$ is impossible. The algebraic identity $x^3 - y^3 = (x-y)(x^2+xy+y^2) = N$ allows us to iterate over the difference $d = x-y$.

Key observations:
1. $N = d \cdot s$, where $s = x^2 + xy + y^2$.
2. Substituting $x = y+d$ into $s$ yields $3y^2 + 3dy + d^2 = s = N/d$.
3. This is a quadratic in $y$: $3y^2 + 3dy + (d^2 - N/d) = 0$.
4. The discriminant is $\Delta = 9d^2 - 12(d^2 - N/d) = 12N/d - 3d^2$.
5. For $y$ to be real, $\Delta \ge 0 \implies 12N/d \ge 3d^2 \implies d^3 \le 4N \implies d \le \sqrt[3]{4N}$.
6. For $N=10^{18}$, $\sqrt[3]{4 \cdot 10^{18}} \approx 1.59 \cdot 10^6$. This is small enough to iterate.
7. We can iterate $d$ from 1 up to $\approx 1.6 \cdot 10^6$.
8. For each $d$, we check if $N$ is divisible by $d$. If not, skip.
9. If $N \% d == 0$, let $S = N/d$. Check if $\Delta = 12S - 3d^2$ is a perfect square.
10. If $\Delta = k^2$ for some integer $k$, then $y = (-3d + k) / 6$. We must check if $(-3d + k)$ is divisible by 6 and if $y > 0$.
11. If valid, $x = y + d$. Output and exit.
12. If loop finishes without solution, output -1.

Pitfalls:
- Floating point precision when checking for perfect squares. Use integer square root.
- Large numbers: Python handles them automatically, but intermediate calculations like $12N/d$ can be large ($10^{19}$), which is fine.
- The condition $d^3 \le 4N$ is derived from $\Delta \ge 0$. We must ensure we don't miss solutions where $d$ is slightly larger due to precision, but the inequality is strict for real roots. Since we require integer roots, checking up to $\lfloor \sqrt[3]{4N} \rfloor$ is sufficient. Actually, if $\Delta < 0$, no real solution. If $\Delta = 0$, $y = -3d/6 = -d/2$, which is not positive for $d>0$. So we strictly need $\Delta > 0$ and a perfect square.
- Wait, if $d$ is a divisor, $d$ can be larger than $\sqrt[3]{N}$. But the bound $d \le \sqrt[3]{4N}$ covers all possible $d$ that yield non-negative discriminant. Since $x,y \ge 1$, we need $y > 0$, which implies $-3d + \sqrt{\Delta} > 0 \implies \sqrt{\Delta} > 3d \implies \Delta > 9d^2$.
  $\Delta = 12N/d - 3d^2 > 9d^2 \implies 12N/d > 12d^2 \implies N/d > d^2 \implies d^3 < N$.
  So actually, we only need to check $d < \sqrt[3]{N}$. Let's re-verify.
  $y = \frac{-3d + \sqrt{12N/d - 3d^2}}{6} > 0 \implies \sqrt{12N/d - 3d^2} > 3d \implies 12N/d - 3d^2 > 9d^2 \implies 12N/d > 12d^2 \implies N > d^3$.
  So yes, we only need to iterate $d$ from 1 up to $\lfloor (N-1)^{1/3} \rfloor$. For $N=10^{18}$, this is $10^6$. This is even smaller and safer.

Plan:
1. Read N.
2. Iterate $d$ from 1 to $\lfloor N^{1/3} \rfloor$.
3. If $N \% d == 0$:
   a. Calculate $S = N // d$.
   b. Calculate $\Delta = 12*S - 3*d*d$.
   c. If $\Delta \le 0$, continue (shouldn't happen if $d < N^{1/3}$, but good for safety).
   d. Check if $\Delta$ is a perfect square. Let $k = \text{isqrt}(\Delta)$. If $k*k \ne \Delta$, continue.
   e. Check if $(-3d + k)$ is divisible by 6. Let $num = -3d + k$. If $num \% 6 != 0$, continue.
   f. $y = num // 6$. If $y \le 0$, continue.
   g. $x = y + d$.
   h. Print $x, y$ and exit.
4. If no solution found, print -1.

## worker: (None)
The solution leverages the algebraic identity $x^3 - y^3 = (x-y)(x^2+xy+y^2)$. By setting $d = x-y$, we derive a quadratic equation in $y$ for each divisor $d$ of $N$. The condition that $y$ must be a positive integer restricts the search space for $d$ to $d < N^{1/3}$. For $N=10^{18}$, this means iterating up to $10^6$, which is computationally feasible. We check if the discriminant is a perfect square and if the resulting $y$ is a valid positive integer.
