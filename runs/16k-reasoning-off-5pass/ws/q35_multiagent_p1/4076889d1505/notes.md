
## ideation
The core difficulty is constructing a pair $(A, M)$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$, while respecting the constraint $M \le 10^{18}$.
1.  **Naive Construction Failure**: Setting $M = 2^N - 1$ works perfectly for the order condition but fails for large $N$ ($N > 60$) because $M$ exceeds $10^{18}$.
2.  **Prime Modulus Strategy**: We can look for a prime modulus $M = p$ such that $N$ divides $p-1$. If such a prime exists, the multiplicative group $\mathbb{Z}_p^*$ is cyclic of order $p-1$. Since $N | (p-1)$, there exists an element of order $N$.
3.  **Existence**: By Dirichlet's theorem and prime number theorem heuristics, there is likely a prime of the form $k \cdot N + 1$ for a small integer $k$. For $N \le 10^9$, $p \approx N$ is well within $10^{18}$. We can iterate $k=1, 2, \dots$ to find the smallest prime $p = kN + 1$.
4.  **Finding A**: Once a prime $p$ is found, we need an element $A$ of order $N$ modulo $p$.
    -   The group order is $p-1 = kN$.
    -   Pick a random generator $g$ of $\mathbb{Z}_p^*$ (or just a random element and check).
    -   Set $A = g^{(p-1)/N} \pmod p = g^k \pmod p$.
    -   The order of $A$ will be $N / \gcd(\text{order}(g), N)$. If $g$ is a primitive root (order $p-1$), then $\gcd(p-1, N) = N$ (since $N|p-1$), so the order is $N$.
    -   To ensure $A$ has order exactly $N$, we can verify that $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$. Alternatively, simply picking a random $g$ and computing $A = g^k \pmod p$ usually yields an element of order $N$ with high probability, or we can check the condition. A robust way is to pick a random $g$, compute $A = g^k \pmod p$, and check if $A^N \equiv 1$ and for all prime factors $q$ of $N$, $A^{N/q} \not\equiv 1$.
5.  **Complexity**:
    -   Finding $p$: Primality testing (Miller-Rabin) is fast. The number of trials for $k$ is small on average.
    -   Finding $A$: Modular exponentiation is fast ($O(\log p)$).
    -   Factoring $N$: Needed to check prime factors of $N$ for verification. Since $N \le 10^9$, trial division up to $\sqrt{N} \approx 31622$ is very fast.
6.  **Edge Cases**: $N=1$. Order 1 means $A^1 \equiv 1 \pmod M$. $A=2, M=1$ works (sample output). Or $A=2, M=3$ ($2^1=2 \not\equiv 1$). Wait, sample says $N=1 \rightarrow 20250126, 1$. $M=1$ is allowed. $A^1 - 1$ is multiple of 1. Smallest $n$? $A^1-1$ is div by 1. So $n=1$. Correct.
    -   For $N=1$, we can just output `2 1`.

## worker: (none)
1.  **Problem Analysis**: The problem requires finding $A, M$ such that the multiplicative order of $A$ modulo $M$ is exactly $N$. The constraints are $A, M \le 10^{18}$ and $N \le 10^9$.
2.  **Strategy**:
    *   Set $M = p$ to be a prime number.
    *   Choose $p$ such that $N$ divides $p-1$. This ensures that the multiplicative group $\mathbb{Z}_p^*$, which has order $p-1$, contains an element of order $N$ (since the group is cyclic).
    *   Specifically, let $p = k \cdot N + 1$. We iterate $k=1, 2, \dots$ to find the smallest prime $p$. For $N \le 10^9$, such a prime is expected to be found very quickly (small $k$), keeping $p \ll 10^{18}$.
    *   Once $p$ is found, we need to construct $A$. Let $g$ be a random element in $\mathbb{Z}_p^*$. Then $A = g^{(p-1)/N} \pmod p$ satisfies $A^N \equiv 1 \pmod p$.
    *   The order of $A$ is $N / \gcd(\text{order}(g), N)$. To guarantee the order is exactly $N$, we verify that $A^{N/q} \not\equiv 1 \pmod p$ for all prime factors $q$ of $N$. If this holds, the order is $N$.
    *   We repeat the random selection of $g$ until such an $A$ is found. The probability of failure is low, so this loop terminates quickly.
3.  **Complexity**:
    *   **Prime Search**: Miller-Rabin is $O(k \log^3 p)$. The number of $k$ values tried is small on average.
    *   **Factorization of N**: Trial division up to $\sqrt{N} \approx 31622$ is very fast for $N \le 10^9$.
    *   **Finding A**: Modular exponentiation is $O(\log p)$. The verification involves checking each prime factor of $N$.
    *   Overall complexity per test case is well within limits for $T=10^4$.
4.  **Edge Cases**:
    *   $N=1$: Handled separately as `2 1` (since $M=1$ is allowed and $A^1-1$ is divisible by 1).
    *   Large $N$: The construction ensures $M \le 10^{18}$ because we find a prime $p \approx N$ or slightly larger.
