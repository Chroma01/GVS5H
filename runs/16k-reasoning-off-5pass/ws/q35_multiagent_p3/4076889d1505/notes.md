
## ideation
The core difficulty is finding a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$, while respecting the constraint $M \le 10^{18}$.

1.  **Small $N$**: For $N \le 60$, we can simply choose $A=2$ and $M=2^N-1$. Since $2^{60} > 10^{18}$, this fits within the limit. The order of 2 modulo $2^N-1$ is exactly $N$ because $2^N \equiv 1 \pmod M$ and for any $k < N$, $0 < 2^k - 1 < 2^N - 1 = M$, so $2^k \not\equiv 1 \pmod M$.

2.  **Large $N$**: For $N > 60$, $2^N - 1$ is too large. We need a smaller modulus $M$.
    *   We look for a prime $p$ such that the multiplicative order of $2$ modulo $p$ is $N$.
    *   If such a prime exists, we can set $A=2$ and $M=p$.
    *   The order of $2$ modulo $p$ is $N$ if and only if:
        1.  $2^N \equiv 1 \pmod p$
        2.  For every prime factor $q$ of $N$, $2^{N/q} \not\equiv 1 \pmod p$.
    *   From condition 1, $p$ must divide $2^N - 1$.
    *   A known property is that if the order of $2$ modulo $p$ is $N$, then $N$ divides $p-1$ (by Fermat's Little Theorem, order divides $\phi(p)=p-1$). Thus, $p \equiv 1 \pmod N$.
    *   So, we can search for primes of the form $p = k \cdot N + 1$.
    *   We iterate $k = 1, 2, \dots$ until we find a prime $p \le 10^{18}$ that satisfies the order conditions.
    *   Given the distribution of primes and primitive prime divisors, we expect to find such a prime with a relatively small $k$.

3.  **Edge Case**: For $N=1$, the order is 1. We can output any $A$ and $M=1$ (since $A^1 - 1$ is always divisible by 1, and 1 is the smallest positive integer). Sample output suggests `20250126 1`, but `2 1` is also valid.

4.  **Algorithm Steps**:
    *   Read $T$.
    *   For each test case $N$:
        *   If $N=1$, print `2 1`.
        *   If $N \le 60$, print `2` and $2^N - 1$.
        *   If $N > 60$:
            *   Factorize $N$ to get its distinct prime factors.
            *   Iterate $k$ starting from 1.
            *   Calculate $p = k \cdot N + 1$.
            *   If $p > 10^{18}$, stop (should not happen for valid inputs within reasonable $k$).
            *   Check if $p$ is prime using Miller-Rabin.
            *   If prime, check if order of 2 mod $p$ is $N:
                *   Compute $r = 2^N \pmod p$. If $r \neq 1$, continue.
                *   For each prime factor $q$ of $N$, compute $r_q = 2^{N/q} \pmod p$. If $r_q == 1$, then the order is a proper divisor of $N$, so continue.
                *   If all checks pass, print `2` and $p$.

## worker: (none)
The problem requires finding a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.
1.  **Case $N=1$**: The order is 1. Any $A$ and $M=1$ works because $A^1 - 1$ is divisible by 1, and 1 is the smallest positive integer. Output `2 1`.
2.  **Case $N \le 60$**: We can set $A=2$ and $M=2^N-1$. Since $2^{60} > 10^{18}$, $M$ fits in the limit. The order of 2 modulo $2^N-1$ is exactly $N$ because $2^N \equiv 1 \pmod M$ and for any $k < N$, $0 < 2^k - 1 < M$, so $2^k \not\equiv 1 \pmod M$.
3.  **Case $N > 60$**: $2^N-1$ is too large. We look for a prime $p$ such that the order of 2 modulo $p$ is $N$.
    *   If the order is $N$, then $N$ divides $p-1$ (by Fermat's Little Theorem, order divides $\phi(p)=p-1$). So $p = kN + 1$ for some integer $k \ge 1$.
    *   We iterate $k=1, 2, \dots$ to find a prime $p = kN + 1$.
    *   For a prime $p$, the order of 2 is $N$ if and only if $2^N \equiv 1 \pmod p$ and for every prime factor $q$ of $N$, $2^{N/q} \not\equiv 1 \pmod p$.
    *   We use Miller-Rabin for primality testing and modular exponentiation for the order checks.
    *   This approach is efficient because we expect to find a suitable prime with a small $k$. Factoring $N$ (up to $10^9$) is fast.
