
## ideation


## worker: (none)
The problem asks for the sum of scores of all good sequences $S$.
The score is $\prod S_i$.
We can compute the contribution of each prime $p$ separately.
For a fixed prime $p$, let $a_i = v_p(A_i)$.
The condition $f(S_i/S_{i+1}) = A_i$ implies $v_p(S_{i+1}) - v_p(S_i) = \pm a_i$.
Let $P_i = v_p(S_i)$. Then $P_{i+1} - P_i = \delta_i \in \{a_i, -a_i\}$.
Also $P_i \ge 0$.
The condition $\gcd(S_1, \dots, S_N) = 1$ implies $\min_i P_i = 0$.
The score contribution for prime $p$ is $p^{\sum P_i}$.
We need to sum $p^{\sum P_i}$ over all valid paths $P$.
We use DP with state $(h, m)$ where $h = P_k - m_k \ge 0$ and $m = m_k = \min_{j \le k} P_j \le 0$.
The transition considers both choices for $\delta_i$.
We ensure $P_{k+1} \ge 0$.
After $N-1$ steps, we sum over all states $(h, m)$ the value $val \times p^{-N m}$.
This accounts for the term $-N \min P$ in the exponent.
The number of states is manageable because $h$ and $m$ are bounded by the sum of $a_i$.
For $N=1000$ and $A_i \le 1000$, the sum of $a_i$ can be up to $10^6$, but the number of reachable states is likely much smaller.
We use a dictionary to store only reachable states.
We handle $a_i = 0$ separately to avoid unnecessary computations.
The final answer is the product of contributions from all primes modulo 998244353.
