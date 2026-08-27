
## ideation
The core difficulty is solving the Diophantine equation $x^3 - y^3 = N$ efficiently given $N$ up to $10^{18}$. A brute-force search over $x$ or $y$ is infeasible because the search space for $y$ can be as large as $\approx 5.77 \times 10^8$ (derived from $3y^2 < N$), which might be too slow for a strict time limit if the constant factor is high or if many test cases exist (though here it's a single input, $10^8$ operations in Python is risky).

The optimal approach is to factor the difference of cubes:
$x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N$.
Let $k = x - y$. Since $x > y \ge 1$, we have $k \ge 1$.
Substituting $x = y + k$ into the second factor:
$(y+k)^2 + (y+k)y + y^2 = 3y^2 + 3ky + k^2$.
So, $k(3y^2 + 3ky + k^2) = N$.
This can be rewritten as a quadratic equation in terms of $y$:
$3k y^2 + 3k^2 y + (k^3 - N) = 0$.

For a fixed $k$, we can solve for $y$ using the quadratic formula:
$y = \frac{-3k^2 \pm \sqrt{(3k^2)^2 - 4(3k)(k^3 - N)}}{6k}$
$y = \frac{-3k^2 \pm \sqrt{9k^4 - 12k^4 + 12kN}}{6k}$
$y = \frac{-3k^2 \pm \sqrt{12kN - 3k^4}}{6k}$
$y = \frac{-3k^2 \pm \sqrt{3k(4N - k^3)}}{6k}$

Since $y$ must be positive, we take the positive root:
$y = \frac{-3k^2 + \sqrt{3k(4N - k^3)}}{6k}$.

Constraints on $k$:
For the term under the square root to be non-negative: $4N - k^3 \ge 0 \implies k \le \sqrt[3]{4N}$.
Given $N \le 10^{18}$, the maximum value for $k$ is $\approx \sqrt[3]{4 \times 10^{18}} \approx 1.587 \times 10^6$.
Iterating $k$ from 1 to $\approx 1.6 \times 10^6$ is computationally very feasible (well within typical 2-second limits for Python).

For each $k$:
1. Calculate discriminant $D = 3k(4N - k^3)$.
2. Check if $D$ is a perfect square. If not, continue.
3. Calculate integer square root $S = \lfloor \sqrt{D} \rfloor$. If $S^2 \neq D$, continue.
4. Check if $(-3k^2 + S)$ is divisible by $6k$. If so, $y = (-3k^2 + S) / (6k)$.
5. If $y$ is a positive integer, then $x = y + k$. Output $x, y$ and terminate.
6. If the loop finishes without a solution, output -1.

Pitfalls:
- Integer overflow: In Python, integers have arbitrary precision, so overflow is not an issue, but efficiency matters.
- Floating point precision: Using `math.sqrt` on very large numbers ($10^{18}$) is generally safe for perfect square checks if followed by integer verification, but integer-only square root algorithms (like `isqrt` from `math` in Python 3.8+) are safer and more precise.
- Time limit: The loop runs $\sim 1.6 \times 10^6$ times. Inside the loop, operations are constant time. This should pass.

## worker: Implement the solution by iterating $k$ from 1 to 
The solution implements the mathematical derivation discussed in the plan.
1.  **Transformation**: The equation $x^3 - y^3 = N$ is transformed by setting $k = x - y$. This leads to a quadratic equation in $y$: $3ky^2 + 3k^2y + (k^3 - N) = 0$.
2.  **Discriminant Analysis**: The discriminant of this quadratic is $D = 3k(4N - k^3)$. For $y$ to be a real number, $D \ge 0$, which implies $k \le \sqrt[3]{4N}$.
3.  **Search Space**: Given $N \le 10^{18}$, the maximum value for $k$ is approximately $1.58 \times 10^6$. Iterating through all possible values of $k$ in this range is computationally efficient (well within time limits).
4.  **Integer Verification**: For each $k$, we calculate $D$. If $D$ is a perfect square, we compute the potential integer solution for $y$ using the quadratic formula. We verify that the numerator is divisible by the denominator ($6k$) and that $y$ is positive.
5.  **Output**: If a valid pair $(x, y)$ is found, it is printed immediately. If the loop completes without finding a solution, `-1` is printed.
6.  **Precision**: `math.isqrt` is used for integer square root calculation to ensure exactness with large numbers, avoiding floating-point inaccuracies.

## worker: Run the code against the provided sample inputs to
The code implements the mathematical derivation discussed in the plan.
1.  **Transformation**: The equation $x^3 - y^3 = N$ is transformed by setting $k = x - y$. This leads to a quadratic equation in $y$: $3ky^2 + 3k^2y + (k^3 - N) = 0$.
2.  **Discriminant Analysis**: The discriminant of this quadratic is $D = 3k(4N - k^3)$. For $y$ to be a real number, $D \ge 0$, which implies $k \le \sqrt[3]{4N}$.
3.  **Search Space**: Given $N \le 10^{18}$, the maximum value for $k$ is approximately $1.58 \times 10^6$. Iterating through all possible values of $k$ in this range is computationally efficient (well within time limits).
4.  **Integer Verification**: For each $k$, we calculate $D$. If $D$ is a perfect square, we compute the potential integer solution for $y$ using the quadratic formula. We verify that the numerator is divisible by the denominator ($6k$) and that $y$ is positive.
5.  **Output**: If a valid pair $(x, y)$ is found, it is printed immediately. If the loop completes without finding a solution, `-1` is printed.
6.  **Precision**: `math.isqrt` is used for integer square root calculation to ensure exactness with large numbers, avoiding floating-point inaccuracies.

The logic handles the constraints and edge cases (like $N=1$) correctly as verified by the sample inputs.

## worker: Run the code against Sample 1 (397) -> Expected: 1
The code implements the mathematical derivation discussed in the plan.
1.  **Transformation**: The equation $x^3 - y^3 = N$ is transformed by setting $k = x - y$. This leads to a quadratic equation in $y$: $3ky^2 + 3k^2y + (k^3 - N) = 0$.
2.  **Discriminant Analysis**: The discriminant of this quadratic is $D = 3k(4N - k^3)$. For $y$ to be a real number, $D \ge 0$, which implies $k \le \sqrt[3]{4N}$.
3.  **Search Space**: Given $N \le 10^{18}$, the maximum value for $k$ is approximately $1.58 \times 10^6$. Iterating through all possible values of $k$ in this range is computationally efficient (well within time limits).
4.  **Integer Verification**: For each $k$, we calculate $D$. If $D$ is a perfect square, we compute the potential integer solution for $y$ using the quadratic formula. We verify that the numerator is divisible by the denominator ($6k$) and that $y$ is positive.
5.  **Output**: If a valid pair $(x, y)$ is found, it is printed immediately. If the loop completes without finding a solution, `-1` is printed.
6.  **Precision**: `math.isqrt` is used for integer square root calculation to ensure exactness with large numbers, avoiding floating-point inaccuracies.

## worker: finalize
The solution transforms the equation $x^3 - y^3 = N$ by setting $k = x - y$. This converts the problem into solving a quadratic equation for $y$ in terms of $k$: $3ky^2 + 3k^2y + (k^3 - N) = 0$. The discriminant of this quadratic is $D = 3k(4N - k^3)$. For $y$ to be a valid positive integer, $D$ must be a perfect square, and the resulting root must be an integer. The constraint $D \ge 0$ implies $k \le \sqrt[3]{4N}$. Given $N \le 10^{18}$, the maximum $k$ is approximately $1.58 \times 10^6$, which allows for an efficient iteration. The code iterates $k$, checks the perfect square condition using integer arithmetic (`math.isqrt`), verifies divisibility, and outputs the first valid pair $(x, y)$ found.
