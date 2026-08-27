
## ideation
The core difficulty is constructing a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$, while respecting the constraint $M \le 10^{18}$.

1.  **Small N (N <= 60):**
    We can use the construction $M = 2^N - 1$ and $A = 2$.
    -   $2^N \equiv 1 \pmod{2^N - 1}$, so the order divides $N$.
    -   For any $k < N$, $2^k - 1 < 2^N - 1 = M$, so $2^k - 1$ is not divisible by $M$.
    -   Thus, the smallest such $n$ is $N$.
    -   Since $2^{60} > 10^{18}$, this works for $N \le 59$. For $N=60$, $2^{60}-1 \approx 1.15 \times 10^{18}$, which exceeds $10^{18}$. So strictly $N \le 59$. Let's use $N \le 60$ with base 2? No, $2^{60}-1 > 10^{18}$. So $N \le 59$.

2.  **Large N (N > 60):**
    We need a different construction because $2^N - 1$ exceeds $10^{18}$.
    We look for a prime $M$ such that $N$ divides $M-1$. If such a prime exists, the multiplicative group $(\mathbb{Z}/M\mathbb{Z})^\times$ is cyclic of order $M-1$. Since $N | M-1$, there exists an element of order $N$.
    -   Let $M = k \cdot N + 1$. We search for the smallest integer $k \ge 1$ such that $M$ is prime.
    -   Given $N \le 10^9$, $M$ can be up to $\approx 10^{18}$ (if $k$ is large). However, prime gaps are small relative to the magnitude, so we expect to find a prime $M$ with a small $k$ quickly.
    -   Once $M$ is found, we need to find an element $A$ of order $N$.
    -   Let $g$ be a primitive root modulo $M$. Then $A = g^{(M-1)/N} \pmod M$ has order $N$.
    -   To find a primitive root $g$, we iterate $g=2, 3, \dots$ and check if $g^{(M-1)/q} \not\equiv 1 \pmod M$ for all prime factors $q$ of $M-1$.
    -   $M-1 = k \cdot N$. We need the prime factorization of $k \cdot N$. Since $N \le 10^9$, we can factorize $N$ easily. We also factorize $k$ (which is small).
    -   Then compute $A = g^{(M-1)/N} \pmod M$ using modular exponentiation.

3.  **Edge Case N=1:**
    Any $A$ and $M=1$ works because $A^1 - 1 = A-1$ is divisible by 1. The smallest $n$ is 1. Sample output uses $M=1$.

4.  **Pitfalls:**
    -   $M$ must be $\le 10^{18}$. We must ensure the found prime $M$ satisfies this. If $k$ gets too large, $M$ might exceed $10^{18}$. However, for $N \ge 1$, primes of the form $kN+1$ are dense enough that we won't exceed $10^{18}$ for $N \ge 1$ within reasonable $k$. Specifically, for $N=10^9$, $k=1 \implies M=10^9+1$ (check primality). If not prime, $k=2 \dots$. The density of primes suggests $k$ will be small.
    -   Factorization of $N$ is required. $N \le 10^9$ allows $O(\sqrt{N})$ factorization.
    -   Modular exponentiation must handle large numbers (Python handles large integers automatically).

## worker: (None)
The problem requires finding $A, M$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.

1.  **Small N ($N \le 59$):**
    We use the construction $A=2, M=2^N-1$.
    -   $2^N \equiv 1 \pmod{2^N-1}$.
    -   For any $k < N$, $2^k - 1 < 2^N - 1 = M$, so $M \nmid (2^k - 1)$.
    -   Thus, the smallest $n$ is $N$.
    -   $2^{59}-1 < 10^{18}$, so this fits the constraints. $2^{60}-1 > 10^{18}$, so we stop at 59.

2.  **Large N ($N > 59$):**
    We need $M \le 10^{18}$. The construction $M=A^N-1$ fails because $A \ge 2 \implies M > 10^{18}$.
    Instead, we use properties of cyclic groups:
    -   Find a prime $M$ such that $N \mid M-1$. Let $M = k \cdot N + 1$.
    -   We iterate $k=1, 2, \dots$ until $M$ is prime. By the Prime Number Theorem, primes are dense enough that $k$ will be small, ensuring $M \le 10^{18}$.
    -   Primality testing is done via Miller-Rabin.
    -   Once prime $M$ is found, the multiplicative group $(\mathbb{Z}/M\mathbb{Z})^\times$ is cyclic of order $M-1$.
    -   Since $N \mid M-1$, there exists an element of order $N$.
    -   We find a primitive root $g$ modulo $M$ by testing small integers $g=2, 3, \dots$ and checking $g^{(M-1)/q} \not\equiv 1 \pmod M$ for all prime factors $q$ of $M-1$.
    -   The prime factors of $M-1 = k \cdot N$ are found by factorizing $N$ and $k$. Since $N \le 10^9$, factorization is fast ($O(\sqrt{N})$). $k$ is small.
    -   We set $A = g^{(M-1)/N} \pmod M$. The order of $A$ is exactly $N$.

3.  **Edge Case N=1:**
    Any $A$ and $M=1$ work. $A^1-1$ is divisible by 1. Smallest $n$ is 1.

4.  **Complexity:**
    -   Factorization of $N$: $O(\sqrt{N})$.
    -   Finding primitive root: Depends on number of prime factors and size of $g$. Typically very fast.
    -   Finding prime $M$: Depends on prime gaps. Expected $k$ is small.
    -   Modular exponentiation: $O(\log M)$.
    -   Total per test case is efficient enough for $T=10^4$.
