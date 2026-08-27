
## ideation
**Core Difficulty**: The problem requires finding $x, y$ such that $x^3 - y^3 = N$ with $N$ up to $10^{18}$. A brute-force search over $x$ or $y$ is impossible because $y$ can be as large as $\approx 10^9$ (when $x-y=1$), leading to $O(N^{1/2})$ complexity which is too slow.

**Candidate Approaches**:
1.  **Iterate on the difference $k = x - y$**:
    *   Since $x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$, let $k = x-y$. Then $k$ must be a divisor of $N$.
    *   However, we don't need to find divisors. We can simply iterate $k$ starting from 1.
    *   Substitute $x = y + k$ into the equation: $N = (y+k)^3 - y^3 = 3y^2k + 3yk^2 + k^3$.
    *   This forms a quadratic equation in $y$: $3k y^2 + 3k^2 y + (k^3 - N) = 0$.
    *   We can solve for $y$ using the quadratic formula: $y = \frac{-3k^2 + \sqrt{9k^4 - 12k(k^3 - N)}}{6k}$.
    *   Simplify the discriminant: $\Delta = 9k^4 - 12k^4 + 12kN = 12kN - 3k^4 = 3k(4N - k^3)$.
    *   For a valid integer solution $y$ to exist, $\Delta$ must be a perfect square, and the resulting $y$ must be a positive integer.
    *   **Range of $k$**: Since $y \ge 1$, we have $3y^2k < N \implies k < N/3$. More tightly, since $k^3 < N$ (as $y \ge 1 \implies (y+k)^3 > k^3$), $k$ is bounded by $N^{1/3}$. For $N=10^{18}$, $k \le 10^6$. This loop is perfectly feasible ($10^6$ iterations).

2.  **Iterate on $y$ directly**:
    *   As noted, $y$ can be up to $10^9$, making this approach $O(N^{1/2})$ which is TLE.

3.  **Iterate on $x$**:
    *   $x \approx N^{1/3}$. If we iterate $x$ downwards from $(N+1)^{1/3}$, we need to check if $x^3 - N$ is a perfect cube.
    *   The gap between consecutive cubes $x^3 - (x-1)^3 \approx 3x^2$. For $N=10^{18}$, $x \approx 10^6$, gap $\approx 3 \times 10^{12}$. The difference $N$ is much smaller than the gap for large $x$ unless $y$ is close to $x$.
    *   Actually, if $x$ is large, $y$ must be close to $x$ for the difference to be $N$. Specifically $3x^2(x-y) \approx N \implies x-y \approx N/(3x^2)$.
    *   If $x \approx 10^6$, $x-y \approx 10^{18}/(3 \cdot 10^{12}) \approx 3 \cdot 10^5$. So $y$ is not necessarily close to $x$.
    *   Wait, if $x \approx 10^6$, then $x^3 \approx 10^{18}$. If $y$ is small, $x^3 - y^3 \approx x^3 = N$. So $x \approx N^{1/3}$.
    *   If $y$ is large, $x$ is also large.
    *   The maximum possible value for $x$ occurs when $y=1$, so $x = \sqrt[3]{N+1}$.
    *   The minimum possible value for $x$ occurs when $y$ is large. Since $x > y$, $x \ge y+1$. $N = x^3 - y^3 \ge (y+1)^3 - y^3 = 3y^2 + 3y + 1$. So $3y^2 < N \implies y < \sqrt{N/3}$. Thus $x \approx \sqrt{N/3}$.
    *   So $x$ ranges from $\approx 10^6$ to $\approx 6 \cdot 10^8$. Iterating $x$ is also too slow ($10^8$ is risky for 1s).
    *   Iterating $k$ (difference) is definitely the best approach because $k \le 10^6$.

## worker: Write the Python code implementing the iteration o
The solution iterates over the difference $k = x - y$. Since $x^3 - y^3 = N$ and $y \ge 1$, we derived that $k^3 < N$, implying $k < N^{1/3}$. For $N \le 10^{18}$, $k$ goes up to $10^6$, which is computationally feasible. For each $k$, we solve the resulting quadratic equation for $y$ using the discriminant. We check if the discriminant is a perfect square and if the resulting $y$ is a positive integer. The first valid pair $(x, y)$ is printed. If no pair is found after checking all possible $k$, we print -1. The use of `math.isqrt` ensures efficient and accurate integer square root calculation.

## worker: Run the code against the provided sample inputs to
The code implements the algorithm derived in the thought process:
1.  **Mathematical Derivation**: It uses the substitution $x = y + k$ to transform the cubic equation $x^3 - y^3 = N$ into a quadratic equation in terms of $y$ for a fixed difference $k$.
2.  **Discriminant Analysis**: The discriminant of the quadratic is derived as $D = 3k(4N - k^3)$. For $y$ to be an integer, $D$ must be a perfect square, and the resulting root must be a positive integer.
3.  **Complexity**: The loop runs for $k$ from $1$ up to approximately $N^{1/3}$. Given $N \le 10^{18}$, the maximum iterations are $10^6$, which fits well within the time limit (typically 1-2 seconds for Python).
4.  **Verification**: The code includes a final check `x**3 - y**3 == n` to ensure correctness, guarding against any potential floating-point inaccuracies (though `math.isqrt` is exact for integers).
5.  **Edge Cases**: Handles $N=1$ correctly (outputs -1) and large inputs efficiently.

## worker: Run the provided sample inputs (397, 1, 3997727385
The code implements the mathematical derivation discussed in the thought process. It iterates through possible values of $k = x - y$. Since $x^3 - y^3 = N$ and $y \ge 1$, we established that $k < N^{1/3}$. For $N \le 10^{18}$, $k$ goes up to $10^6$, making the loop efficient. For each $k$, it solves the quadratic equation for $y$ using the discriminant $D = 3k(4N - k^3)$. It checks if $D$ is a perfect square and if the resulting $y$ is a positive integer. Finally, it verifies the solution.

## worker: finalize
The solution iterates over the difference $k = x - y$. Since $x^3 - y^3 = N$ and $y \ge 1$, we derived that $k < N^{1/3}$. For $N \le 10^{18}$, $k$ goes up to $10^6$, making the loop efficient. For each $k$, it solves the quadratic equation for $y$ using the discriminant $D = 3k(4N - k^3)$. It checks if $D$ is a perfect square and if the resulting $y$ is a positive integer. Finally, it verifies the solution. The use of `math.isqrt` ensures efficient and accurate integer square root calculation.
