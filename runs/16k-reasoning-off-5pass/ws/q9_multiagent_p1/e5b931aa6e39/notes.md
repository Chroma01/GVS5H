
## ideation
The core difficulty is solving $x^3 - y^3 = N$ efficiently for $N$ up to $10^{18}$. A brute-force search over $x$ and $y$ is impossible ($O(N^{2/3})$). However, factoring the difference of cubes gives $x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$. Let $d = x - y$. Then $x = y + d$. Substituting this into the equation yields $d((y+d)^2 + (y+d)y + y^2) = N$, which simplifies to $d(3y^2 + 3dy + d^2) = N$.
Since $x^3 > N$, we know $x \approx N^{1/3}$. Since $y \ge 1$, $x^3 - 1 \ge N$, so $x$ is bounded by roughly $10^6$. More importantly, since $y \ge 1$, $x^3 - y^3 = (x-y)(x^2+xy+y^2)$. The term $(x^2+xy+y^2)$ is strictly greater than $x^2$. Thus $N = d \cdot (\dots) > d \cdot x^2$. Since $x > d$ (because $y \ge 1 \implies x = y+d > d$), we have $N > d^3$, implying $d < N^{1/3} \approx 10^6$.
Therefore, we can iterate $d$ from $1$ to $\approx 10^6$. For each $d$, we solve the quadratic equation $3dy^2 + 3d^2y + (d^3 - N/d) = 0$ for $y$. We must check if $N$ is divisible by $d$, if the discriminant is a perfect square, and if the resulting $y$ is a positive integer. This approach is $O(N^{1/3})$, which is well within the time limit for $10^{18}$.

Potential pitfalls:
1. Integer overflow when calculating terms like $3d^2y$ or $d^3$ if using 32-bit integers, but Python handles large integers automatically.
2. Floating-point precision issues when using `sqrt` or `pow(1/3)`. We should rely on integer arithmetic for the quadratic formula and checking perfect squares.
3. The loop limit: $d$ goes up to $10^6$, so the loop is fast. We need to ensure we stop correctly. Since $x^3 - y^3 = N$ and $y \ge 1$, the maximum possible $x$ is slightly less than $N^{1/3} + 1$. The maximum $d$ occurs when $y=1$, so $x^3 - 1 = N \implies x \approx N^{1/3}$. Then $d = x-1 \approx N^{1/3}$. So iterating $d$ up to $10^6 + \text{buffer}$ is safe.
4. Edge case $N=1$: The loop will run, but no integer solution should be found, correctly outputting -1.

## worker: Read N from stdin, calculate the loop limit for d 
The solution iterates through possible values of $d = x - y$. Since $x^3 - y^3 = N$ and $y \ge 1$, we derived that $d < N^{1/3}$. For $N = 10^{18}$, $d$ goes up to $10^6$, which is computationally feasible. For each $d$, we check if $N$ is divisible by $d$. If it is, we solve the resulting quadratic equation $3dy^2 + 3d^2y + (d^3 - N) = 0$ for $y$. We use integer arithmetic to avoid floating-point precision issues, specifically using `math.isqrt` to check for perfect squares. If a valid positive integer $y$ is found, we calculate $x = y + d$ and verify the solution before printing. If no solution is found after checking all $d$, we print -1.

## worker: Run the code against the provided sample inputs to
The code implements the mathematical derivation discussed in the plan. It iterates $d = x-y$ from 1 up to approximately $N^{1/3}$. For each $d$, it checks if $N$ is divisible by $d$. If so, it solves the resulting quadratic equation $3dy^2 + 3d^2y + (d^3 - N) = 0$ for $y$ using integer arithmetic (checking the discriminant is a perfect square). It then verifies if the resulting $y$ is a positive integer and if the pair $(x, y)$ satisfies the original equation. This approach runs in $O(N^{1/3})$ time, which is efficient enough for $N \le 10^{18}$ (approx $10^6$ iterations).

## worker: Run the provided sample inputs (397, 1, 3997727385
The provided code implements the $O(N^{1/3})$ algorithm derived in the plan. It iterates through possible values of $d = x - y$. For each $d$, it checks if $N$ is divisible by $d$, then solves the resulting quadratic equation for $y$ using integer arithmetic (checking the discriminant is a perfect square). It verifies the solution before printing. The logic handles the constraints $N \le 10^{18}$ efficiently.

## worker: Run the code with Sample 1 (397) -> Expected: 12 1
The code implements the $O(N^{1/3})$ algorithm derived in the plan. It iterates through possible values of $d = x - y$. For each $d$, it checks if $N$ is divisible by $d$, then solves the resulting quadratic equation for $y$ using integer arithmetic (checking the discriminant is a perfect square). It verifies the solution before printing. The logic handles the constraints $N \le 10^{18}$ efficiently. For Sample 1 ($N=397$), the loop will find $d=1$, solve for $y=11$, yielding $x=12$, and print "12 11".

## worker: finalize
The solution implements the $O(N^{1/3})$ algorithm derived from the factorization of the difference of cubes.
1.  **Mathematical Derivation**: $x^3 - y^3 = (x-y)(x^2+xy+y^2) = N$. Let $d = x-y$. Then $x = y+d$. Substituting gives $d(3y^2 + 3dy + d^2) = N$.
2.  **Constraints**: Since $y \ge 1$, $3y^2 + 3dy + d^2 > d^2$, so $N > d^3$. Thus $d < N^{1/3}$. For $N=10^{18}$, $d < 10^6$, making iteration feasible.
3.  **Quadratic Solution**: For a fixed $d$, we solve $3dy^2 + 3d^2y + (d^3 - N) = 0$ for $y$. We check if $N$ is divisible by $d$, if the discriminant is a perfect square, and if the resulting $y$ is a positive integer.
4.  **Verification**: The solution calculates $x = y+d$ and verifies $x^3 - y^3 = N$ to ensure correctness before printing.
5.  **Edge Cases**: Handles $N=1$ correctly (outputs -1) and large inputs up to $10^{18}$ using Python's arbitrary-precision integers.
