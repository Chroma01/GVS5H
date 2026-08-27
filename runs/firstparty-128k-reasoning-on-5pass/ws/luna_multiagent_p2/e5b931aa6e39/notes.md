- **Parameterization:** Let \(d=x-y>0\), so \(x=y+d\). Then
  \(N=d(3y^2+3dy+d^2)\).
- **Bound:** Since \(N=d(3y^2+3dy+d^2)>d^3\) for positive \(y\), it is sufficient to iterate \(1\le d\le\lfloor\sqrt[3]{N}\rfloor\).
- **Divisibility:** For a valid solution, \(d\) divides \(N\). Set \(q=N/d\), yielding the quadratic equation \(3y^2+3dy+d^2=q\).
- **Discriminant:** Its discriminant is \(D=12q-3d^2\), and
  \(y=(-3d+\sqrt D)/6\). An exact integer square-root check and divisibility by 6 ensure \(y\) is integral.
- **Correctness:** Every candidate is verified directly using \(x^3-y^3=N\), avoiding any floating-point errors.
- **Complexity:** The loop performs \(O(\sqrt[3]{N})\) iterations, at most about \(10^6\), with constant-time big-integer operations for the given constraints.
