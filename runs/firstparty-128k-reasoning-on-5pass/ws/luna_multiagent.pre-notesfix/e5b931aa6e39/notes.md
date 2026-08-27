
## ideation
The proposed plan has a serious complexity issue: \(y\) is not bounded by approximately \(\sqrt[3]{N}\). When \(x-y=1\), valid candidates can have \(y\) on the order of \(\sqrt{N}\), which is far too large to enumerate for \(N\le 10^{18}\). A better parameter is the difference \(d=x-y\). Since
\(N=d(3y^2+3dy+d^2)\), we have \(d^3\le N\), so \(d\) is at most about \(10^6\).

## worker: Implement the divisor-difference algorithm: enumer
Using \(d=x-y\), we have
\[
N=d(3y^2+3dy+d^2).
\]
Since the second factor is at least \(d^2\), \(d^3\le N\), so only \(d\le\lfloor\sqrt[3]{N}\rfloor\) need to be checked.

For each divisor \(d\) of \(N\), solving the quadratic in \(y\) gives discriminant
\[
D=12(N/d)-3d^2,
\]
and
\[
y=\frac{\sqrt D-3d}{6}.
\]
The implementation checks that \(D\) is an exact square, the division is integral, and \(y>0\), then verifies the original equation. The complexity is \(O(\sqrt[3]{N})\) time and \(O(1)\) memory.
