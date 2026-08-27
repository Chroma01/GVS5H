
## ideation
**Core Difficulty**:
The problem requires finding integer solutions to $x^3 - y^3 = N$ where $N$ can be up to $10^{18}$. A brute-force search over $x$ and $y$ is impossible ($O(N^{2/3})$ or $O(N)$). We need an algorithm with complexity around $O(N^{1/3})$ or better.

**Candidate Approaches**:
1.  **Algebraic Factorization & Iteration on Difference ($d$)**:
    -   Let $d = x - y$. Since $x, y \ge 1$, we have $d \ge 1$.
    -   Expand $x^3 - y^3 = (x-y)(x^2 + xy + y^2) = d((y+d)^2 + (y+d)y + y^2) = d(3y^2 + 3dy + d^2) = N$.
    -   This implies $d$ must be a divisor of $N$.
    -   Also, since $y \ge 1$, $3y^2 + 3dy + d^2 > d^2$, so $N = d(\dots) > d^3$, which means $d < N^{1/3}$.
    -   Since $N \le 10^{18}$, $N^{1/3} \le 10^6$. We can iterate $d$ from $1$ to $10^6$.
    -   For each $d$, check if $N \% d == 0$. If so, let $K = N/d$. We need to solve $3y^2 + 3dy + d^2 = K$ for positive integer $y$.
    -   This is a quadratic equation: $3y^2 + (3d)y + (d^2 - K) = 0$.
    -   Solve for $y$ using the quadratic formula: $y = \frac{-3d \pm \sqrt{(3d)^2 - 4(3)(d^2 - K)}}{6} = \frac{-3d \pm \sqrt{9d^2 - 12d^2 + 12K}}{6} = \frac{-3d \pm \sqrt{12K - 3d^2}}{6}$.
    -   Check if the discriminant is a perfect square and if the resulting $y$ is a positive integer.
    -   Complexity: $O(N^{1/3})$, which is $\approx 10^6$ operations. This fits well within time limits (usually 2 seconds).

2.  **Iterate on $y$**:
    -   Since $x = y + d$, $x^3 - y^3 \approx 3y^2 d$.
    -   If $d$ is small, $y$ can be large (up to $N^{1/3}$). Iterating $y$ up to $10^6$ and checking if $N + y^3$ is a perfect cube is also $O(N^{1/3})$.
    -   However, checking perfect cubes involves integer cube roots which might be slightly more expensive or require careful implementation compared to the quadratic formula approach. The $d$ iteration approach feels more direct algebraically.

3.  **Iterate on $x$**:
    -   $x$ goes up to $N^{1/3} + 10^6$ roughly? No, if $y=1$, $x \approx N^{1/3}$. So $x$ is also bounded by $10^6 + \text{small}$.
    -   Iterate $x$ from $\lfloor N^{1/3} \rfloor$ downwards? Or upwards?
    -   If we iterate $x$, we calculate $y^3 = x^3 - N$. Check if $x^3 - N$ is a perfect cube.
    -   Range of $x$: Since $y \ge 1$, $x^3 - 1 \ge N \implies x \ge (N+1)^{1/3}$.
    -   Max $x$? If $y=1

## worker: Implement the Python script following the derived 
The algorithm iterates through possible values of $d = x - y$. Since $x^3 - y^3 = (x-y)(x^2+xy+y^2)$, and $x^2+xy+y^2 > d^2$ for $y \ge 1$, we have $N > d^3$, limiting $d$ to $N^{1/3}$. For $N=10^{18}$, $d$ goes up to $10^6$, which is computationally feasible. For each $d$, we check if $d$ divides $N$. If it does, we solve the resulting quadratic equation for $y$ using the discriminant method. We verify if the discriminant is a perfect square and if the resulting $y$ is a positive integer. If a valid pair $(x, y)$ is found, it is printed immediately. If the loop completes without finding a solution, -1 is printed.

## worker: Run the code against the provided sample inputs to
The code implements the $O(N^{1/3})$ algorithm derived in the thought process.
1.  **Input Reading**: Reads $N$ from standard input.
2.  **Iteration**: Iterates $d$ (the difference $x-y$) from 1 up to $\approx N^{1/3}$. Since $N \le 10^{18}$, $d$ goes up to $10^6$, which is well within time limits.
3.  **Quadratic Solution**: For each valid $d$ (where $N \% d == 0$), it sets $k = N/d$ and solves the quadratic equation $3y^2 + 3dy + (d^2 - k) = 0$ for $y$.
4.  **Validation**: Checks if the discriminant is a perfect square and if the resulting $y$ is a positive integer. Finally, verifies the solution with integer arithmetic before printing.
5.  **Edge Cases**: Handles $N=1$ correctly (outputs -1) and large inputs efficiently.

## worker: Run the provided sample inputs (397, 1, 3997727385
The code implements the $O(N^{1/3})$ algorithm derived in the thought process.
1.  **Input Reading**: Reads $N$ from standard input.
2.  **Iteration**: Iterates $d$ (the difference $x-y$) from 1 up to $\approx N^{1/3}$. Since $N \le 10^{18}$, $d$ goes up to $10^6$, which is well within time limits.
3.  **Quadratic Solution**: For each valid $d$ (where $N \% d == 0$), it sets $k = N/d$ and solves the quadratic equation $3y^2 + 3dy + (d^2 - k) = 0$ for $y$.
4.  **Validation**: Checks if the discriminant is a perfect square and if the resulting $y$ is a positive integer. Finally, verifies the solution with integer arithmetic before printing.
5.  **Edge Cases**: Handles $N=1$ correctly (outputs -1) and large inputs efficiently.

## worker: finalize
The solution implements an $O(N^{1/3})$ algorithm.
1.  **Mathematical Derivation**: We set $d = x - y$. The equation $x^3 - y^3 = N$ transforms into $d(3y^2 + 3dy + d^2) = N$.
2.  **Bounds**: Since $y \ge 1$, the term $(3y^2 + 3dy + d^2) > d^2$, implying $N > d^3$. Thus, $d < N^{1/3}$. For $N=10^{18}$, $d$ is at most $10^6$, making iteration feasible.
3.  **Quadratic Solution**: For a fixed $d$, if $N$ is divisible by $d$, we let $k = N/d$ and solve $3y^2 + 3dy + (d^2 - k) = 0$. The discriminant is $\Delta = 12k - 3d^2$. We check if $\Delta$ is a perfect square and if the resulting $y = \frac{-3d + \sqrt{\Delta}}{6}$ is a positive integer.
4.  **Verification**: Before printing, we verify $x^3 - y^3 = N$ using integer arithmetic to avoid any potential precision issues, though the logic is sound.
