
## ideation
The problem asks for a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.
Constraints: $N \le 10^9$, $A, M \le 10^{18}$.

**Core Difficulty**:
1.  **Size of $M$**: We cannot simply set $M = 2^N - 1$ because for large $N$ (e.g., $N=100$), $2^N$ exceeds $10^{18}$.
2.  **Existence**:

## worker: Implement a Miller-Rabin primality test to check i
1.  **Problem Analysis**: The problem requires finding $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$. The constraints are $N \le 10^9$ and $A, M \le 10^{18}$.
2.  **Strategy**:
    *   If $N=1$, the answer is trivially $A=2, M=1$ (since $2^1-1=1$ is divisible by 1, and no smaller positive integer exists).
    *   If $N > 1$, we construct $M$ as a prime $p$ such that $p \equiv 1 \pmod N$. This ensures that the multiplicative group $\mathbb{Z}_p^*$ has order $p-1$, which is a multiple of $N$.
    *   We iterate $k = 1, 2, \dots$ and set $p = k \cdot N + 1$. We check if $p$ is prime using the Miller-Rabin test.
    *   Once a suitable prime $p$ is found, we need to find an element $A$ of order $N$ in $\mathbb{Z}_p^*$. We know that $x^N \equiv 1 \pmod p$ has exactly $N$ solutions. We can generate a candidate $A$ by picking a random generator $g$ and setting $A = g^{(p-1)/N} \pmod p$.
    *   To verify that the order of $A$ is exactly $N$, we check that $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$. If this holds for all $q$, the order is $N$.
    *   Since the density of primes is high, we will find a valid $p$ quickly. The probability of finding an $A$ with order $N$ is $\phi(N)/N$, which is also reasonably high.
3.  **Implementation Details**:
    *   **Miller-Rabin**: Implemented with deterministic bases for $n < 2^{64}$ to ensure correctness for inputs up to $10^{18}$.
    *   **Prime Factorization**: A simple trial division is sufficient since $N \le 10^9$.
    *   **Modular Exponentiation**: Standard binary exponentiation ($O(\log \text{exponent})$).
    *   **Randomness**: Used to pick the base $g$ for generating $A$.

## worker: Test the solution against the provided sample inpu
The solution implements the strategy of finding a prime $p = k \cdot N + 1$ such that the multiplicative order of some $A$ modulo $p$ is exactly $N$.
1.  **Case $N=1$**: Handled directly with output `2 1`.
2.  **Case $N > 1$**:
    *   We iterate $k$ starting from 1 to find a prime $p = k \cdot N + 1$.
    *   Since $N \le 10^9$, $p$ can reach $10^{18}$, so we use the deterministic Miller-Rabin primality test with bases up to 37, which is proven correct for $n < 2^{64}$.
    *   Once a prime $p$ is found, the group $\mathbb{Z}_p^*$ has order $p-1 = k \cdot N$. We need an element of order $N$.
    *   We pick a random generator $g$ and compute $A = g^{(p-1)/N} \pmod p$. This ensures $A^N \equiv 1 \pmod p$.
    *   To verify the order is exactly $N$, we check that $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$.
    *   If the check passes, we output $(A, p)$.
    *   The density of primes is high enough that we will find a suitable $p$ very quickly (usually $k=1$ or small). The probability of finding a valid $A$ given $p$ is $\phi(N)/N$, which is also high.
3.  **Complexity**:
    *   Primality test: $O(\log^3 p)$ or $O(\log^4 p)$ depending on multiplication cost. With $p \approx 10^{18}$, this is fast.
    *   Factorization of $N$: $O(\sqrt{N})$. Since $N \le 10^9$, $\sqrt{N} \le 31622$, which is very fast.
    *   Total time per test case is dominated by finding the first prime $kN+1$, which is expected to be very small $k$.

## worker: Run the code against the provided sample inputs to
The code implements the strategy derived in the thought process:
1.  **Case N=1**: Outputs `2 1`.
2.  **Case N>1**: Iterates $k=1, 2, \dots$ to find a prime $p = k \cdot N + 1$.
    *   Uses a deterministic Miller-Rabin test for $n < 2^{64}$ to check primality of $p$.
    *   Once a prime $p$ is found, it computes $A = g^{(p-1)/N} \pmod p$ for a random $g$.
    *   It verifies that the order of $A$ is exactly $N$ by checking $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$.
    *   This ensures $A^N \equiv 1 \pmod p$ and no smaller power works.
3.  **Constraints**: $N \le 10^9$ implies $p$ can be up to $\approx 10^{18}$ (if $k \approx 10^9$), fitting within 64-bit integers. The time complexity per test case is dominated by the primality test and factorization, which are efficient enough for $T=10^4$.

## worker: Run the provided sample input to verify the output
The provided solution implements the strategy of finding a prime $p = k \cdot N + 1$ such that the multiplicative order of some $A$ modulo $p$ is exactly $N$.
1.  **Case $N=1$**: Handled directly with output `2 1`.
2.  **Case $N > 1$**:
    *   We iterate $k$ starting from 1 to find a prime $p = k \cdot N + 1$.
    *   We use a deterministic Miller-Rabin primality test with bases up to 37, which is proven correct for $n < 2^{64}$ (covering the $10^{18}$ limit).
    *   Once a prime $p$ is found, the group $\mathbb{Z}_p^*$ has order $p-1 = k \cdot N$. We need an element of order $N$.
    *   We pick a random generator $g$ and compute $A = g^{(p-1)/N} \pmod p$. This ensures $A^N \equiv 1 \pmod p$.
    *   To verify the order is exactly $N$, we check that $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$.
    *   If the check passes, we output $(A, p)$.
    *   The density of primes is high enough that we will find a suitable $p$ very quickly (usually $k=1$ or small). The probability of finding a valid $A$ given $p$ is $\phi(N)/N$, which is also high.
3.  **Complexity**:
    *   Primality test: $O(\log^3 p)$ or $O(\log^4 p)$ depending on multiplication cost. With $p \approx 10^{18}$, this is fast.
    *   Factorization of $N$: $O(\sqrt{N})$. Since $N \le 10^9$, $\sqrt{N} \le 31622$, which is very fast.
    *   Total time per test case is dominated by finding the first prime $kN+1$, which is expected to be very small $k$.

## worker: finalize
The solution implements a constructive approach to find a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$.

1.  **Case $N=1$**: The problem requires $A^1 - 1$ to be a multiple of $M$ with no smaller $n$. If we choose $M=1$, $A^1 - 1$ is always divisible by 1. Since $n$ must be positive, the smallest $n$ is 1. Thus, $(2, 1)$ is a valid solution.
2.  **Case $N > 1$**:
    *   We need $M$ such that the multiplicative order of $A$ modulo $M$ is $N$.
    *   A reliable construction is to choose $M$ as a prime $p$ such that $p \equiv 1 \pmod N$. This ensures that the order of the multiplicative group $\mathbb{Z}_p^*$ is $p-1$, which is a multiple of $N$.
    *   We iterate $k = 1, 2, \dots$ and check if $p = k \cdot N + 1$ is prime using the deterministic Miller-Rabin primality test (valid for $n < 2^{64}$).
    *   Once a suitable prime $p$ is found, the group $\mathbb{Z}_p^*$ has order $p-1 = k \cdot N$. We need an element $A$ of order exactly $N$.
    *   We pick a random generator $g$ and compute $A = g^{(p-1)/N} \pmod p$. This guarantees $A^N \equiv 1 \pmod p$.
    *   To ensure the order is exactly $N$ (and not a proper divisor), we verify that $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$.
    *   The probability of finding a valid $A$ is $\phi(N)/N$, which is reasonably high. We retry with different random $g$ if necessary.
    *   Given the density of primes, we will find a suitable $p$ very quickly (usually $k$ is small). The constraints $N \le 10^9$ and $M \le 10^{18}$ are respected.
