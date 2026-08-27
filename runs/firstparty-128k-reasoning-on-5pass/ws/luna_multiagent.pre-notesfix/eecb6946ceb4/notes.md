
## ideation
The core difficulty is avoiding enumeration of all endpoint pairs, which is quadratic in \(N\). A fine triplet is determined by its middle value \(B\), and its endpoints satisfy \(A+C=2B\). If \(f[x]\) is the indicator of membership in \(S\), then the coefficient of \(x^{2B}\) in \(f(x)^2\) counts ordered pairs \((A,C)\) whose sum is \(2B\). For a present \(B\), this coefficient consists of one diagonal pair \((B,B)\) plus two ordered versions of every valid pair \(A<C\). Thus the contribution of \(B\) is \((\operatorname{conv}[2B]-1)/2\).

The answer is at most about \(M^2/4\), where \(M\le 10^6\), so a signed 64-bit integer is sufficient.

## worker: Derive a practical exact convolution implementatio
The indicator polynomial is \(F(x)=\sum_{s\in S}x^s\). The coefficient of \(x^{2B}\) in \(F(x)^2\) counts ordered pairs \((A,C)\) with \(A+C=2B\). For a present \(B\), it includes \((B,B)\) once and every valid \(A<C\) pair twice, so the contribution is \((\text{coefficient}-1)/2\).

A single NTT modulus, \(998244353\), is sufficient because every convolution coefficient is at most \(N\le 10^6\), far below the modulus. The transform size is the smallest power of two greater than \(2\max(S)\), at most \(2^{21}\). The algorithm performs one forward NTT, pointwise squaring, and one inverse NTT, with \(O(M\log M)\) time and \(O(M)\) memory, where \(M=\max(S)\).
