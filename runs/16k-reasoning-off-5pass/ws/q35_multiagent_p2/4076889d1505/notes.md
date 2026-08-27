
## ideation
The problem asks for a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$. This means $A^N \equiv 1 \pmod M$ and for all $1 \le k < N$, $A^k \not\equiv 1 \pmod M$.

A standard construction is to set $M = A^N - 1$. Then $A^N - 1$ is divisible by $M$ (quotient 1). For any $k < N$, $0 < A^k - 1 < A^N - 1 = M$ (assuming $A \ge 2$), so $A^k - 1$ cannot be a multiple of $M$. Thus, the smallest such $n$ is $N$.
The constraints are $A, M \le 10^{18}$.
If we choose $A=2$, then $M = 2^N - 1$. This is valid as long as $2^N - 1 \le 10^{18}$. Since $2^{60} > 10^{18}$, this construction works for $N \le 59$ (actually $2^{59} \approx 5.76 \times 10^{17} < 10^{18}$, $2^{60} \approx 1.15 \times 10^{18} > 10^{18}$). So for $N \le 59$, we can output `2` and `2^N - 1`.

For $N > 59$, we need a different construction.
Consider $A = N+1$ and $M = N$.
Then $A^1 - 1 = N$, which is divisible by $M=N$.
For $k=1$, it is divisible. Is it the smallest? Yes, if $N > 1$. But we need order $N$, not 1. So this doesn't work.

Consider $A = 2$ and $M$ being a prime factor of $2^N - 1$ with order $N$. By Zsigmondy's theorem, such a prime exists for $N > 1$ (except $N=6$). However, finding this prime factor for large $N$ is computationally expensive and the prime itself might be larger than $10^{18}$.

Alternative construction:
Let $A = 2$ and $M = 2^N - 1$ for small $N$.
For large $N$, we can use the fact that if we set $A = N+1$ and $M = N$, the order is 1.
What if we set $A = 2$ and $M = 2^N - 1$ is too big.

Let's try $A = N+1$ and $M = N^2 + N + 1$? No.

Let's look at the sample cases.
$N=3 \rightarrow 2, 7$. $2^3-1=7$.
$N=16 \rightarrow 11, 68$. $11^{16} \equiv 1 \pmod{68}$.
$N=1 \rightarrow 20250126, 1$. $2^1-1=1$ is divisible by 1. Order is 1.
$N=55 \rightarrow 33, 662$.

For $N=1$, any $A$ works with $M=1$. Output `2 1`.

For $N > 1$, if we can find an $A$ such that $A^N - 1 \le 10^{18}$, we can set $M = A^N - 1$.
We need $A^N \le 10^{18} + 1$.
If $N$ is large, $A$ must be small.
If $N > 60$, $A$ must be 1? No, $A \ge 2$. $2^{60} > 10^{18}$. So for $N \ge 60$, we cannot use $A=2$ with $M=2^N-1$.

We need a construction where $M$ is small but the order is large.
This requires $M$ to have a large multiplicative order. The maximum order modulo $M$ is $\phi(M)$. We need $\phi(M) \ge N$.
Also we need an element $A$ of order exactly $N$. This requires $N | \phi(M)$ and specific conditions on the prime factors of $M$.

A simple construction for large $N$:
Let $M$ be a prime $p$ such that $N | p-1$. Then there exists an element of order $N$ modulo $p$.
We need $p \le 10^{18}$ and $p \equiv 1 \pmod N$.
The smallest prime $p \equiv 1 \pmod N$ is roughly $N$. For $N=10^9$, $p \approx 10^9$, which is well within $10^{18}$.
So for any $N$, we can find a prime $p = kN + 1$ for some small $k$.
Then we need to find a primitive $N$-th root of unity modulo $p$.
Let $g$ be a primitive root modulo $p$. Then $A = g^{(p-1)/N} \pmod p$ has order $N$.
We can set $M = p$.
Then $A^N \equiv 1 \pmod p$. And for $k < N$, $A^k \not\equiv 1 \pmod p$ because the order is exactly $N$.
So the pair $(A, M) = (g^{(p-1)/N} \pmod p, p)$ works.

Algorithm:
1. If $N=1$, output `2 1`.
2. If $N \le 59$, output `2` and `2^N - 1`.
3. If $N > 59$:
   a. Find the smallest prime $p$ such that $p \equiv 1 \pmod N$.
      Since $p \ge N+1$, and we need $p \le 10^{18}$, this is always possible for $N \le 10^9$ because there is always a prime in $[N+1, 2N]$ (Bertrand's postulate doesn't guarantee $1 \pmod N$, but Dirichlet's theorem says there are infinitely many. The smallest prime $p \equiv 1 \pmod N$ is known to be $O(N^2)$ or better, definitely $< 10^{18}$ for $N \le 10^9$).
      Actually, we can just iterate $k=1, 2, \dots$ and check if $kN+1$ is prime.
   b. Find a primitive root $g$ modulo $p$.
   c. Compute $A = g^{(p-1)/N} \pmod p$.
   d. Output $A$ and $p$.

Complexity:
Finding the smallest prime $p \equiv 1 \pmod N$:
For $N=10^9$, we check $k=1, 2, \dots$. The gap between primes is small. We expect to find a prime quickly.
Checking primality of numbers up to $10^{18}$ can be done with Miller-Rabin.
Finding a primitive root: Iterate $g=2, 3, \dots$ and check if $g$ is a primitive root.
Checking if $g$ is a primitive root modulo $p$:
Factorize $p-1 = N \cdot k$.
For each prime factor $q$ of $p-1$, check if $g^{(p-1)/q} \not\equiv 1 \pmod p$.
Since $p-1 = N \cdot k$, and $N$ can be large, factoring $p-1$ might be hard if $k$ is large.
However, $p \approx N$. So $p-1 \approx N$. Factoring $N$ is feasible for $N \le 10^9$ (trial division up to $\sqrt{N} \approx 31622$).

So the plan is:
1. Handle $N=1$ and small $N$ separately.
2. For large $N$:
   - Find smallest prime $p = kN + 1$.
   - Factorize $p-1$. Since $p-1 = kN$, and we know $N$, we can factor $N$ and then factor $k$.
   - Find primitive root $g$.
   - Compute $A = g^{(p-1)/N} \pmod p$.
   - Output $A, p$.

Pitfalls:
- $N=1$: Handled.
- $N=2$: $2^2-1=3$. $A=2, M=3$. Order of 2 mod 3 is 2. Correct.
- $N=6$: $2^6-1=63$. $A=2, M=63$. Order of 2 mod 63? $2^6=64 \equiv 1$. $2^3=8 \not\equiv 1$. $2^2=4 \not\equiv 1$. $2^1=2 \not\equiv 1$. So order is 6. Correct.
- Large $N$: Ensure $p \le 10^{18}$. Since $N \le 10^9$, $p \approx 10^9$ is fine.

Implementation details:
- Miller-Rabin primality test for numbers up to $10^{18}$.
- Trial division for factoring $N$ (up to $10^9$).
- Finding primitive root: iterate $g$ from 2. Check if $g$ is primitive root.
- Modular exponentiation.

Let's refine the "find smallest prime $p \equiv 1 \pmod N$" part.
We check $k=1, 2, \dots$.
$p = kN + 1$.
Check if $p$ is prime.
Since $N \le 10^9$, $p$ can be up to $\approx 10^9 \times \text{small constant}$.
The density of primes is $1/\ln p$. So we expect to find a prime within a few thousand iterations.
This is very fast.

Factoring $p-1 = kN$.
We already have $N$. We need to factor $k$ as well?
No, we need the prime factors of $p-1$.
$p-1 = k \cdot N$.
We can factor $N$ (since $N \le 10^9$).
We can factor $k$ (since $k$ is small, typically $< 1000$).
So we can get all prime factors of $p-1$.

Then find primitive root $g$.
For each candidate $g$, check if $g^{(p-1)/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $p-1$.
This is efficient.

Then $A = g^{(p-1)/N} \pmod p$.
Note that $(p-1)/N = k$.
So $A = g^k \pmod p$.

This construction ensures order of $A$ is $N$.
$A^N = g^{kN} = g^{p-1} \equiv 1 \pmod p$.
If $A^d \equiv 1 \pmod p$ for $d < N$, then $g^{kd} \equiv 1 \pmod p$.
This implies $p-1 | kd$.
$p-1 = kN$. So $kN | kd \implies N | d$.
Since $d < N$, this is impossible. So order is exactly $N$.

One edge case: $N=1$.
$A=2, M=1$.
$2^1 - 1 = 1$, divisible by 1.
Smallest $n$ is 1. Correct.

Another edge case: $N=2$.
$2^2-1=3$. $A=2, M=3$.
$2^1-1=1$, not div by 3.
$2^2-1=3$, div by 3.
Order 2. Correct.

So the code will:
1. Read T.
2. For each test case N:
   - If $N=1$, print "2 1".
   - If $N \le 59$, print "2 " + str($2^N - 1$).
   - Else:
     - Find smallest $k \ge 1$ such that $p = kN + 1$ is prime.
     - Factor $p-1$. Since $p-1 = kN$, factor $N$ and $k$.
     - Find primitive root $g$ mod $p$.
     - Compute $A = pow(g, k, p)$.
     - Print $A, p$.

Let's double check $N=60$.
$2^{60}-1 > 10^{18}$. So we use the prime method.
$p = k \cdot 60 + 1$.
$k=1 \implies 61$ (prime).
$p=61$.
$p-1 = 60$.
Factor 60: $2, 3, 5$.
Find primitive root mod 61.
Try $g=2$.
$2^{60/2} = 2^{30} \pmod{61}$.
$2^{30} = (2^5)^6 = 32^6$.
$32^2 = 1024 = 16 \times 61 + 48 \equiv 48 \equiv -13$.
$32^4 \equiv 169 \equiv 47 \equiv -14$.
$32^6 \equiv (-13)(-14) = 182 = 3 \times 61 - 1 \equiv -1 \not\equiv 1$.
$2^{60/3} = 2^{20}$.
$2^{10} = 1024 \equiv 48 \equiv -13$.
$2^{20} \equiv 169 \equiv 47 \equiv -14 \not\equiv 1$.
$2^{60/5} = 2^{12}$.
$2^{12} = 4096$.
$4096 / 61 = 67.14$. $61 \times 67 = 4087$.
$4096 - 4087 = 9 \not\equiv 1$.
So 2 is a primitive root mod 61.
$A = 2^{60/60} = 2^1 = 2$.
Output `2 61`.
Check: Order of 2 mod 61 is 60?
$2^{60} \equiv 1$.
Divisors of 60: 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30.
We checked 30, 20, 12.
$2^{30} \equiv -1$.
$2^{20} \equiv -14$.
$2^{12} \equiv 9$.
$2^{15} = 2^{12} \cdot 2^3 = 9 \cdot 8 = 72 \equiv 11 \not\equiv 1$.
$2^{10} = -13 \not\equiv 1$.
$2^6 = 64 \equiv 3 \not\equiv 1$.
$2^5 = 32 \not\equiv 1$.
$2^4 = 16 \not\equiv 1$.
$2^3 = 8 \not\equiv 1$.
$2^2 = 4 \not\equiv 1$.
$2^1 = 2 \not\equiv 1$.
So order is 60. Correct.

The solution seems solid.

## worker: Implement the solution in Python, including Miller
1. **Problem Analysis**: The problem requires finding $A, M$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$. This means $A^N \equiv 1 \pmod M$ and for all $1 \le k < N$, $A^k \not\equiv 1 \pmod M$.
2. **Small N Construction**: For $N \le 59$, we can simply set $A=2$ and $M=2^N-1$. Since $2^{60} > 10^{18}$, this fits within the constraints. The order of 2 modulo $2^N-1$ is exactly $N$ because $2^N \equiv 1 \pmod{2^N-1}$ and for $k<N$, $0 < 2^k-1 < 2^N-1$, so $2^k \not\equiv 1 \pmod{2^N-1}$.
3. **Large N Construction**: For $N > 59$, $2^N-1$ exceeds $10^{18}$. We use a prime modulus $p$ such that $N | p-1$. By Dirichlet's theorem, such primes exist. We find the smallest prime $p = kN+1$.
4. **Primitive Root**: Since $p$ is prime, there exists a primitive root $g$ modulo $p$. The element $A = g^{(p-1)/N} \pmod p$ has order exactly $N$ modulo $p$.
   - $A^N = g^{p-1} \equiv 1 \pmod p$.
   - If $A^d \equiv 1 \pmod p$ for $d < N$, then $g^{d(p-1)/N} \equiv 1 \pmod p$, implying $p-1 | d(p-1)/N$, so $N | d$. Since $d < N$, this is a contradiction. Thus, the order is exactly $N$.
5. **Complexity**:
   - Finding $p$: We check $k=1, 2, \dots$. The gap between primes is small, so this is fast. Primality test is Miller-Rabin, $O(k \log^3 p)$.
   - Factoring $p-1$: $p-1 = kN$. We factor $N$ (up to $10^9$) and $k$ (small). Trial division up to $\sqrt{N}$ is fast.
   - Finding primitive root: Iterate $g$ and check conditions. This is fast.
   - Overall complexity per test case is very low, well within limits for $T=10^4$.
