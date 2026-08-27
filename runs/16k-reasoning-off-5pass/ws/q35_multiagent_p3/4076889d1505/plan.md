The problem asks for a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$. A simple construction is to set $M = A^N - 1$. In this case, $A^N \equiv 1 \pmod M$ by definition. We need to ensure that no smaller positive integer $k < N$ satisfies $A^k \equiv 1 \pmod M$. Since $M = A^N - 1$, we have $A^k - 1 < A^N - 1 = M$ for all $k < N$ (assuming $A \ge 2$). Therefore, $A^k - 1$ cannot be a multiple of $M$ for any $k < N$ because it is strictly less than $M$ and positive. Thus, the smallest such $n$ is indeed $N$. We can choose $A=2$ and $M=2^N - 1$. However, $M$ can be up to $2^{10^9}-1$, which is far too large ($10^{18}$ limit). We need a smaller $M$.

Alternative construction: Let $M$ be a prime such that $N$ divides $M-1$. Then there exists an element of order $N$ in the multiplicative group modulo $M$. Specifically, if we pick a prime $M$ such that $M \equiv 1 \pmod N$, we can find a generator $g$ and set $A = g^{(M-1)/N}$. Then the order of $A$ is $N$. However, finding such a prime and generator for large $N$ is complex.

Simpler construction: Let $A = 2$. We need $M$ such that the order of $2$ modulo $M$ is $N$. This requires $M | 2^N - 1$ and $M \nmid 2^k - 1$ for $k < N$. We can simply choose $M = 2^N - 1$ if it fits in $10^{18}$. But $N$ can be $10^9$, so $2^N$ is huge.

Let's reconsider the constraints. $M \le 10^{18}$.
If we set $A = N+1$ and $M = N$, then $A \equiv 1 \pmod M$. The order of $1$ is $1$, not $N$ (unless $N=1$).
If we set $A = 2$ and $M = 2^N - 1$, $M$ is too big.

Let's use the property: If we choose $M$ to be a divisor of $A^N - 1$ but not of $A^k - 1$ for any $k < N$, the order is $N$.
Consider $A=2$. We need $M | 2^N - 1$.
If $N$ is small, $2^N - 1$ fits in $10^{18}$. $2^{60} > 10^{18}$, so for $N \le 60$, we can just output $2, 2^N - 1$.
For large $N$, we need a different approach.

Note that if we pick $A = 10^9 + 7$ (a prime) and $M = A^N - 1$? No, $M$ is too big.

Let's look at the sample cases.
N=3: A=2, M=7. $2^3-1=7$. Order is 3.
N=16: A=11, M=68. $11^{16} \equiv 1 \pmod{68}$?
$11^2 = 121 = 2 \times 68 + 1 \equiv 1 \pmod{68}$. Order is 2, not 16. Wait.
Let's check sample output 2: 11 68.
$11^1 - 1 = 10$, not div by 68.
$11^2 - 1 = 120$, not div by 68 ($120 = 68 + 52$).
$11^4 = (11^2)^2 = 121^2 \equiv 1^2 = 1 \pmod{68}$?
$121 = 68 + 53 \equiv 53 \equiv -15 \pmod{68}$.
$11^2 \equiv 53 \pmod{68}$.
$11^4 \equiv 53^2 = 2809$. $2809 / 68 = 41.3$. $41 \times 68 = 2788$. $2809 - 2788 = 21$. Not 1.
This sample solution is complex.

Let's go back to the simple construction: $A=2, M=2^N-1$.
This works for $N \le 60$.
For $N > 60$, we can't use $2^N-1$.

However, we can construct $M$ using prime factors.
We know that the order of $A$ modulo $M$ is $N$ if $M$ divides $A^N-1$ and for every prime factor $p$ of $M$, the order of $A$ modulo $p^k$ is $N$ (or divides $N$ but the LCM is $N$).

Actually, there is a very simple solution:
Let $A = 2$.
Let $M = 2^N - 1$. This is valid only if $M \le 10^{18}$.
If $N$ is large, we can't use this.

Wait, look at $N=1$. Output 20250126 1. $M=1$. Any $A$ works since $A^n - 1$ is always multiple of 1. Smallest $n$?
Condition: smallest $n$ such that $M | A^n - 1$.
If $M=1$, $1 | A^n - 1$ is always true. Smallest positive integer $n$ is 1.
So for $N=1$, any $A, M=1$ works.

For $N > 1$, we need $M > 1$.

Let's try $A = N+1, M = N$?
$(N+1)^n \equiv 1 \pmod N \iff 1^n \equiv 1 \pmod N$. Always true for $n \ge 1$. Smallest $n=1$. Not $N$.

Let's try $A = 2, M = 2^N - 1$ for small $N$.
For large $N$, we can use the fact that if we pick a prime $p$ such that $p | 2^N - 1$ and $p \nmid 2^k - 1$ for $k < N$, then the order of $2$ modulo $p$ is $N$.
Such a prime $p$ is called a primitive prime divisor of $2^N - 1$. By Zsigmondy's theorem, such a prime exists for all $N > 1$ except $N=6$.
For $N=6$, $2^6 - 1 = 63 = 3^2 \cdot 7$.
Order of 2 mod 3 is 2.
Order of 2 mod 7 is 3.
LCM(2,3) = 6.
So if we set $M = 63$, the order of 2 mod 63 is LCM(order mod 9, order mod 7).
$2^1=2, 2^2=4, 2^3=8\equiv -1, 2^6 \equiv 1 \pmod 7$. Order 3.
$2^1=2, 2^2=4, 2^3=8\equiv -1, 2^6 \equiv 1 \pmod 9$. Order 6.
LCM(6,3) = 6.
So $M=63$ works for $N=6$.

So the strategy is:
1. If $N=1$, output `2 1`.
2. If $N \le 60$, output `2` and `2^N - 1`.
3. If $N > 60$, find a prime $p$ such that the order of $2$ modulo $p$ is $N$. Then output `2` and `p`.
   How to find such a prime?
   We know $p | 2^N - 1$.
   Also, the order of $2$ mod $p$ is $N$ implies $N | p-1$, so $p = kN + 1$.
   We can iterate $k=1, 2, \dots$ and check if $p = kN + 1$ is prime and if the order of $2$ mod $p$ is $N$.
   Checking if order is $N$:
   - Check $2^N \equiv 1 \pmod p$.
   - Check $2^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$.
   
   Since $N \le 10^9$, factoring $N$ is fast.
   We need to find a prime $p = kN + 1$.
   By Dirichlet's theorem, there are infinitely many such primes.
   We just need to find one that is $\le 10^{18}$.
   Since $p \approx kN$, and we need $p \le 10^{18}$, we can have $k$ up to $10^9$.
   We can iterate $k$ starting from 1.
   For each $k$, let $p = kN + 1$.
   Check if $p$ is prime (Miller-Rabin).
   If prime, check if order of 2 mod $p$ is $N$.
   This requires factoring $N$.
   
   Is it guaranteed that a small $k$ works?
   Usually, yes. The smallest primitive prime divisor is often small relative to $N$? Not necessarily.
   However, we only need *one* such prime.
   
   Let's refine the plan:
   1. Handle $N=1$: `2 1`.
   2. Handle $N \le 60$: `2` `2^N - 1`.
   3. For $N > 60$:
      a. Factorize $N$ to get its prime factors.
      b. Iterate $k = 1, 2, \dots$
      c. Let $p = k \cdot N + 1$.
      d. If $p > 10^{18}$, break (shouldn't happen for small $k$).
      e. If $p$ is prime:
         i. Check if $2^N \equiv 1 \pmod p$. (This is true if $p | 2^N - 1$. We can compute this via modular exponentiation).
         ii. Check if for every prime factor $q$ of $N$, $2^{N/q} \not\equiv 1 \pmod p$.
         iii. If both conditions hold, the order is exactly $N$. Output `2` and `p`.

   This approach is efficient because:
   - Factoring $N$ ($10^9$) is fast.
   - Miller-Rabin is fast.
   - We expect to find a suitable prime $p$ with small $k$.