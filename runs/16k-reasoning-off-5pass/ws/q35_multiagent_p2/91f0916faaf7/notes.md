
## ideation
The problem asks for the sum of scores of all "good" sequences $S$ of length $N$, where the score is $\prod S_i$, subject to local constraints $f(S_i/S_{i+1}) = A_i$ and a global constraint $\gcd(S_1, \dots, S_N) = 1$.

1.  **Multiplicative Decomposition**: The condition $f(P/Q) = P \cdot Q = A$ implies that for any prime $p$, the exponents of $p$ in the numerator and denominator of the reduced fraction $S_i/S_{i+1}$ must sum to $v_p(A_i)$. Since the fraction is reduced, one of the exponents is 0. This leads to the condition $|v_p(S_i) - v_p(S_{i+1})| = v_p(A_i)$. Let $e_i = v_p(S_i)$ and $a_i = v_p(A_i)$. The condition is $|e_i - e_{i+1}| = a_i$.
    The global condition $\gcd(S_1, \dots, S_N) = 1$ translates to: for every prime $p$, $\min(e_1, \dots, e_N) = 0$.
    The score factorizes into $\prod_p p^{\sum e_i}$. Thus, the total sum is the product over all primes $p$ of the sum of $p^{\sum e_i}$ for valid exponent sequences for that prime.

2.  **Solving for a Single Prime**:
    For a fixed prime $p$, we need to compute:
    $$ \text{Ans}_p = \sum_{\substack{e_1, \dots, e_N \ge 0 \\ |e_i - e_{i+1}| = a_i \\ \min(e_i) = 0}} p^{\sum e_i} $$
    Let $S_{\ge 0}$ be the sum over all sequences with $e_i \ge 0$ satisfying the difference constraints.
    Let $S_{\ge 1}$ be the sum over all sequences with $e_i \ge 1$ satisfying the difference constraints.
    Then $\text{Ans}_p = S_{\ge 0} - S_{\ge 1}$.
    
    Note that if $e_i \ge 1$, we can write $e_i = 1 + e'_i$ with $e'_i \ge 0$. The difference constraints $|e_i - e_{i+1}| = a_i$ become $|e'_i - e'_{i+1}| = a_i$. The score term becomes $p^{\sum (1+e'_i)} = p^N p^{\sum e'_i}$.
    Therefore, $S_{\ge 1} = p^N \cdot S_{\ge 0}^{(shifted)}$, where $S_{\ge 0}^{(shifted)}$ is the sum for sequences $e'_i \ge 0$.
    However, the set of valid sequences for $e'_i \ge 0$ is not necessarily the same as for $e_i \ge 0$ if there are boundary effects, but structurally the transitions are identical. The only difference is the range of valid values.
    
    Actually, it is simpler to bound the values. If $\min(e_i) = 0$, then all $e_i$ are bounded by $M = \sum_{i=1}^{N-1} a_i$. Any sequence with $\min(e_i)=0$ must satisfy $0 \le e_i \le M$.
    We can compute the sum of scores for all sequences satisfying $|e_i - e_{i+1}| = a_i$ and $0 \le e_i \le M$. Let this sum be $Total(M)$.
    This sum $Total(M)$ includes sequences where $\min(e_i) > 0$.
    The sequences with $\min(e_i) \ge 1$ are exactly those with $1 \le e_i \le M$.
    Let $e_i = 1 + e'_i$. Then $0 \le e'_i \le M-1$.
    The sum for these is $p^N \cdot Total(M-1)$.
    So, $\text{Ans}_p = Total(M) - p^N \cdot Total(M-1)$.

3.  **DP Implementation**:
    $Total(K)$ can be computed using DP.
    $DP[i][v]$ = sum of $p^{\sum_{j=1}^i e_j}$ for valid prefixes $e_1, \dots, e_i$ such that $e_i = v$ and $0 \le e_j \le K$ for all $j \le i$.
    Transition: $DP[i][v] = p^v \cdot (DP[i-1][v-a_i] \text{ if } v \ge a_i \text{ else } 0 + DP[i-1][v+a_i] \text{ if } v+a_i \le K \text{ else } 0)$.
    Base case: $DP[1][v] = p^v$ for $0 \le v \le K$.
    The answer for the prime is $\sum_v DP[N][v]$.

4.  **Complexity**:
    $N \le 1000$, $A_i \le 1000$. Max $a_i \le 10$. Max $M \le 10000$.
    For each prime, DP is $O(N \cdot M)$. In worst case $10^7$ ops.
    Number of primes up to 1000 is 168. But we only process primes that divide at least one $A_i$.
    This is efficient enough.

## worker: Implement a function to get prime factorization of
1.  **Prime Factorization**: The problem is multiplicative. We decompose the problem into independent subproblems for each prime factor $p$ present in the input array $A$.
2.  **Local Condition**: For a prime $p$, let $a_i = v_p(A_i)$. The condition $f(S_i/S_{i+1}) = A_i$ implies $|v_p(S_i) - v_p(S_{i+1})| = a_i$. Let $e_i = v_p(S_i)$.
3.  **Global Condition**: $\gcd(S_1, \dots, S_N) = 1$ implies $\min(e_1, \dots, e_N) = 0$ for every prime $p$.
4.  **DP Formulation**: We need to sum $p^{\sum e_i}$ over all sequences $e_i \ge 0$ satisfying the difference constraints and $\min(e_i) = 0$.
    -   Let $Total(K)$ be the sum of scores for sequences with $0 \le e_i \le K$.
    -   The sequences with $\min(e_i) = 0$ are those in $[0, M]$ minus those in $[1, M]$.
    -   Sequences in $[1, M]$ correspond to sequences $e'_i = e_i - 1$ in $[0, M-1]$.
    -   The score scales by $p^N$. So, $Ans_p = Total(M) - p^N \cdot Total(M-1)$.
5.  **Complexity**: $N \le 1000$, max exponent sum $M \le 10000$. The DP for each prime is $O(N \cdot M)$. Since we only process primes dividing some $A_i$, and there are few such primes, this is efficient.
6.  **Edge Cases**: If $M=0$ (all $a_i=0$), $Total(0)=1, Total(-1)=0$, result $1 - p^N \cdot 0 = 1$. Correct.
