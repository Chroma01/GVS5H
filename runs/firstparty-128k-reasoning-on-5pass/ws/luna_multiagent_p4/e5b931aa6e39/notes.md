- **Enumeration variable:** Let \(d=x-y>0\). Then \(x=y+d\), and
  \(N=d(3y^2+3dy+d^2)\).
- **Search bound:** Since \(3y^2+3dy+d^2\ge d^2\), we have \(N\ge d^3\). Therefore it is sufficient to enumerate \(1\le d\le\lfloor\sqrt[3]{N}\rfloor\), at most \(10^6\) values.
- **Divisibility:** For a candidate \(d\), it must divide \(N\). Set \(M=N/d\), yielding
  \(3y^2+3dy+d^2=M\).
- **Discriminant:** The quadratic in \(y\) has discriminant
  \(D=12M-3d^2\). A valid integer \(y\) requires \(D\) to be a nonnegative perfect square.
- **Recovering \(y\):** If \(r=\sqrt D\), then
  \(y=(r-3d)/6\). The numerator must be positive and divisible by \(6\).
- **Exact arithmetic:** `math.isqrt` checks perfect squares without floating-point errors. The cube-root limit is corrected after an initial floating-point estimate.
- **Verification:** Every candidate is finally checked directly with \(x^3-y^3=N\), ensuring correctness.
- **Complexity:** \(O(\sqrt[3]{N})\) iterations and \(O(1)\) extra space.
