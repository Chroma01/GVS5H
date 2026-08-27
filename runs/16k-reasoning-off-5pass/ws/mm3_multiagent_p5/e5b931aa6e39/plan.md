The equation \(x^3 - y^3 = N\) can be rewritten as \((x - y)(x^2 + xy + y^2) = N\). For large \(N\) (up to \(10^{18}\)), we can iterate over possible values of \(d = x - y\) (a positive divisor of \(N\)). For each divisor \(d\), we need to solve the system:
- \(x = y + d\)
- \(d \cdot (x^2 + xy + y^2) = N\)

Substituting \(x = y + d\) gives a quadratic equation in \(y\):
\[
d \cdot (3y^2 + 3dy + d^2) = N \implies 3dy^2 + 3d^2 y + d^3 - N = 0
\]
This quadratic in \(y\) can be solved using the discriminant. We need the discriminant to be a non-negative perfect square, and the resulting \(y\) to be a positive integer. Since \(N \le 10^{18}\), the number of divisors is small (at most around \(10^5\) in worst case), but iterating over all divisors up to \(\sqrt{N}\) is feasible within time limits (around \(10^9\) operations, which is borderline). We can optimize by noting that \(x\) and \(y\) are positive, so \(x > y \ge 1\), meaning \(x^3 - y^3 \ge 7\) (since \(2^3 - 1^3 = 7\)). Also, for small \(N\) we can handle directly.

A more efficient approach: For each \(x\) from 1 to \(\sqrt[3]{N}+1\), compute \(y = \sqrt[3]{x^3 - N}\). This is O(\(N^{1/3}\)) which is at most \(10^6\) for \(N=10^{18}\), very fast. We compute \(x^3\) (careful with overflow in Python, but Python handles big integers). Then check if \(x^3 - N\) is a perfect cube of a positive integer less than \(x\).