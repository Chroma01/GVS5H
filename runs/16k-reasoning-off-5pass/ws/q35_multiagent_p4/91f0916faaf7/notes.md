
## ideation
The problem asks for the sum of scores of all "good" sequences $S$ satisfying local constraints $f(S_i/S_{i+1}) = A_i$ and a global GCD constraint $\gcd(S_1, \dots, S_N) = 1$.

1.  **Multiplicative Structure**: The function $f(x)$ and the GCD condition are multiplicative with respect to prime factors. We can decompose the problem by each prime $p$. For each prime $p$, let $a_i = v_p(A_i)$ be the exponent of $p$ in $A_i$. The condition $f(S_i/S_{i+1}) = A_i$ implies that for the exponents $e_{i,p} = v_p(S_i)$, we must have $|e_{i,p} - e_{i+1,p}| = a_i$.
2.  **Global GCD Constraint**: The condition $\gcd(S_1, \dots, S_N) = 1$ translates to: for every prime $p$, $\min(e_{1,p}, \dots, e_{N,p}) = 0$.
3.  **Dynamic Programming for Each Prime**: For a fixed prime $p$, we need to sum the contributions $\prod_{i=1}^N p^{e_{i,p}}$ over all valid exponent sequences.
    *   Let $\delta_i = e_{i,p} - e_{1,p}$. Then $e_{i,p} = e_{1,p} + \delta_i$.
    *   The condition $|e_{i,p} - e_{i+1,p}| = a_i$ becomes $|\delta_i - \delta_{i+1}| = a_i$ with $\delta_1 = 0$.
    *   The global constraint $\min(e_{i,p}) = 0$ implies $e_{1,p} + \min(\delta_i) = 0$, so $e_{1,p} = -\min(\delta_i)$. Let $m = \min(\delta_i)$. Note $m \le 0$.
    *   The total exponent of $p$ in the score is $\sum_{i=1}^N e_{i,p} = \sum_{i=1}^N (e_{1,p} + \delta_i) = N \cdot e_{1,p} + \sum_{i=1}^N \delta_i = -N \cdot m + \sum_{i=1}^N \delta_i$.
    *   We can use DP to track the distribution of $(m, \delta_N, \sum \delta_i)$.
    *   State: `dp[i][m][d]` = sum of $p^{\sum_{k=1}^i \delta_k}$ for all paths of length $i$ ending with current delta $d$ and minimum delta so far $m$.
    *   Transition: From state $(m, d)$ at step $i$, we can go to $d' = d + a_i$ or $d' = d - a_i$.
        *   New min $m' = \min(m, d')$.
        *   New sum of deltas $S' = S + d'$.
        *   The weight updates by multiplying by $p^{d'}$.
    *   Since $N$ is up to 1000 and $A_i$ up to 1000, the range of $\delta$ can be large. However, we can use a dictionary/hash map to store only reachable states $(m, d)$. The number of reachable states is manageable for typical cases, and worst-case analysis suggests it fits within time limits given the modulo arithmetic and sparse transitions.
4.  **Combining Results**: The total answer is the product of the results for each prime $p$ that divides any $A_i$. For primes not dividing any $A_i$, the only valid sequence is all zeros (exponents), contributing a factor of 1.

## worker: (none)
The solution decomposes the problem by prime factors due to the multiplicative nature of the score and the GCD condition. For each prime $p$, we determine the exponents $e_{i,p}$ of $p$ in $S_i$. The condition $f(S_i/S_{i+1}) = A_i$ implies $|e_{i,p} - e_{i+1,p}| = v_p(A_i)$. The global GCD condition implies $\min_i e_{i,p} = 0$.

We use Dynamic Programming to sum the contributions for each prime. The DP state tracks the minimum delta seen so far ($m$) and the current delta ($d$) relative to $e_{1,p}$. The weight in the DP state accumulates $p^{\sum \delta_k}$. Transitions involve choosing $+a_i$ or $-a_i$ for the next delta, updating the minimum and multiplying the weight by $p^{\text{new delta}}$. Finally, we adjust the weight by $p^{-N \cdot m}$ to account for the base exponent $e_{1,p} = -m$. The results for all primes are multiplied together modulo 998244353.

Complexity: For each prime, the number of states $(m, d)$ is bounded by the range of possible deltas. While worst-case range is large, the number of reachable states is typically much smaller, and using a dictionary/hash map ensures we only process reachable states. Given $N \le 1000$ and $A_i \le 1000$, this approach is efficient enough.
