
## ideation
We need to count sequences \(S=(S_1,\dots,S_N)\) of positive integers such that for each \(i\),
\[
f\!\left(\frac{S_i}{S_{i+1}}\right)=A_i,\qquad 
f\!\left(\frac{P}{Q}\right)=P\cdot Q\ (\gcd(P,Q)=1),
\]
and \(\gcd(S_1,\dots,S_N)=1\).  
For a prime \(p\), write \(v_{i,p}=v_p(S_i)\). For an edge \(i\) with exponent \(e_i=v_p(A_i)\) (0 if \(p\nmid A_i\)), the condition forces a binary choice:
- **do not select** \(p\): \(v_{i+1,p}=v_{i,p}+e_i\);
- **select** \(p\) (i.e. include the full prime power in the unitary divisor): allowed only if \(v_{i,p}\ge e_i\), then \(v_{i+1,p}=v_{i,p}-e_i\).

The choices for different primes are independent because for each edge we may pick any subset of the primes dividing \(A_i\) (unitary divisor). Thus the total sum of scores factorises over primes:
\[
\text{Answer}=\prod_{p} F_p\pmod{998244353},
\]
where \(F_p\) is the sum over all sequences of exponents \((v_{1,p},\dots,v_{N,p})\) satisfying the above dynamics, never going negative, and having \(\min_i v_{i,p}=0\) (to ensure overall gcd 1). For a fixed prime \(p\) the contribution of a sequence to the product of all \(S_i\) is \(p^{\sum_i v_{i,p}}\), so we must sum \(p^{\sum_i v_{i,p}}\) over those sequences.

The exponents are bounded: to ever reach 0 we need \(v_{1,p}\le \sum_i e_i\) (total possible subtraction). Let \(S=\sum_i e_i\). The maximal value that can appear is \(v_{1,p}+S\le 2S\). Hence a DP over positions \(i\) and current exponent \(v\) (range \(0..2S\)) with a flag “has been zero” suffices.

DP state: \(dp[v][z]\) = sum of \(p^{\sum_{j=1}^{i} v_{j,p}}\) for all ways to be at position \(i\) with current exponent \(v\) and “zero already seen” flag \(z\in\{0,1\}\).  
Initialisation (\(i=1\)):
- for \(v=0..S\): \(z=(v==0)\); \(dp[v][z]=p^{v}\).

Transition for edge \(i\) (exponent \(e_i\)):
- **add** (no selection): \(v' = v+e_i\) (if \(v'\le 2S\));
- **subtract** (selection): allowed if \(v\ge e_i\); then \(v' = v-e_i\);
- new flag \(z' = z\ \text{or}\ (v'=0)\);
- add \(dp[v][z]\cdot p^{v'}\) to \(dp'[v'][z']\).

After processing all \(N-1\) edges, \(F_p = \sum_{v} dp[v][1]\) (visited zero at least once). Primes never appearing in any \(A_i\) give \(F_p=1\) (exponent must be 0 for all positions).

Complexities: for each prime \(p\), \(S\le N\cdot\max e_i\le 1000\cdot 9=9000\); DP runs in \(O(N\cdot S)\) time and \(O(S)\) memory. Number of distinct primes is at most the primes \(\le 1000\) (≈168), but only those dividing some \(A_i\) appear; in practice ≤10. Total work easily fits.

## worker: Implement the solution: factor each A_i, group exp
We factor each \(A_i\) into prime powers. For each prime \(p\) we obtain the list of exponents \(e_i=v_p(A_i)\) for all edges. The condition on a sequence forces for each prime a walk on non‑negative integers where at step \(i\) we either add \(e_i\) (do not select \(p\)) or subtract \(e_i\) (select \(p\), allowed only if current value \(\ge e_i\)). The overall gcd condition requires the walk to visit 0 at least once. The contribution of a walk to the total product of the sequence is \(p^{\sum_i v_{i,p}}\).  
Because the walks for different primes are independent, the answer factorises:
\[
\text{Answer}=\prod_{p} \Bigl(\sum_{\text{walks touching 0}} p^{\sum_i v_{i,p}}\Bigr)\pmod{998244353}.
\]

For a fixed prime, let \(S=\sum_i e_i\). Any walk that ever reaches 0 must start with \(v_1\le S\); the maximal value during the walk is at most \(2S\). A DP over positions \(i\) and current exponent \(v\) (range \(0..2S\)) with a boolean flag “has been zero” is therefore sufficient. The transition updates the flag and multiplies by the weight of the new term \(p^{v'}\). After processing all edges we sum the states where the flag is true. The complexity is \(O(N\cdot S)\) per prime, which is at most a few million operations; the total number of distinct primes is small (≤10 for the given constraints), so the program easily runs in time.
