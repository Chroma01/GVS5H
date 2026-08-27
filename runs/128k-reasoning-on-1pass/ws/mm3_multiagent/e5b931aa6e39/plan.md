We use the factorization  
\[
x^3 - y^3 = (x-y)(x^2+xy+y^2)=N .
\]  
Let \(d=x-y\;(>0)\). Then  
\[
N = d\bigl(3y^2+3yd+d^2\bigr) .
\]  
Since \(y\ge1\), the second factor is larger than \(d^2\), hence \(d^3<N\) and we only need to try
\(d\le \sqrt[3]{N}\;( \le10^6\) for the given limits).  
For each divisor \(d\) of \(N\) we set \(M=N/d\) and solve the quadratic
\(3y^2+3d\,y+d^2 = M\). Its discriminant is  
\[
\Delta = 12M-3d^2 .
\]  
If \(\Delta\) is a non‑negative perfect square, let \(s=\sqrt{\Delta}\).  
Then  
\[
y = \frac{s-3d}{6}
\]  
must be a positive integer; the corresponding \(x=y+d\) gives a solution.
We check the condition \(x^3-y^3=N\) before printing.
If no suitable \(d\) is found, output \(-1\).