
## ideation
The problem asks for the largest integer $N \le A$ such that $N$ has exactly 2 distinct prime factors, and each prime factor divides $N$ an even number of times.

Let the prime factorization of $N$ be $p_1^{e_1} p_2^{e_2} \dots p_m^{e_m}$.
The conditions are:
1. $m = 2$. Let the primes be $p$ and $q$.
2. $e_1$ is even and $e_2$ is even. Let $e_1 = 2a$ and $e_2 = 2b$ with $a, b \ge 1$.

Thus, $N = p^{2a} q^{2b} = (p^a q^b)^2$.
Let $k = p^a q^b$. Then $N = k^2$.
The number $k$ has prime factorization $p^a q^b$. Since $p \neq q$, $k$ has exactly 2 distinct prime factors.
Conversely, if $k$ has exactly 2 distinct prime factors, say $p$ and $q$, then $k = p^a q^b$ with $a,b \ge 1$. Then $N=k^2 = p^{2a} q^{2b}$ satisfies the conditions.

So the problem reduces to:
Find the largest perfect square $k^2 \le A$ such that $k$ has exactly two distinct prime factors.
Let $S = \lfloor \sqrt{A} \rfloor$. We need the largest $k \le S$ such that $k$ has exactly two distinct prime factors. The answer is $k^2$.

Constraints: $A \le 10^{12}$, so $S \le 10^6$.
$Q \le 2 \times 10^5$.

Algorithm:
1. Precompute for all integers $k$ from 1 to $10^6$ the number of distinct prime factors.
   - We can use a sieve-like method. Initialize an array `num_distinct_primes` of size $10^6+1$ with zeros.
   - Iterate $i$ from 2 to $10^6$. If `num_distinct_primes[i]` is 0, then $i$ is prime. For all multiples $j$ of $i$, increment `num_distinct_primes[j]`.
2. Collect all $k \in [1, 10^6]$ such that `num_distinct_primes[k] == 2` into a sorted list `valid_ks`.
3. For each query $A$:
   - Compute $S = \lfloor \sqrt{A} \rfloor$. Be careful with floating point precision. Use integer square root or check neighbors.
   - Find the largest element in `valid_ks` that is $\le S$. This can be done with `bisect_right` in Python.
   - The answer is the square of that element.

Pitfalls:
- Floating point precision for $\sqrt{10^{12}}$. $10^6$ is exact, but for $A$ close to $10^{12}$, `math.sqrt` might have issues? Actually `math.isqrt` is available in Python 3.8+ and is safe.
- The smallest 400 number is $2^2 \cdot 3^2 = 36$. The problem states $A \ge 36$, so a solution always exists.
- The list `valid_ks` will be sorted naturally if we iterate $k$ from 1 upwards.

Complexity:
- Sieve: $O(M \log \log M)$ or $O(M \log M)$ where $M=10^6$. This is very fast.
- Query: $O(\log M)$ per query using binary search. Total $O(Q \log M)$.
- Space: $O(M)$ for the array and list.

This approach is efficient enough.

## worker: Implement the sieve to count distinct prime factor
The key insight is that a "400 number" $N$ must be of the form $p^{2a} q^{2b}$ for distinct primes $p, q$ and positive integers $a, b$. This can be rewritten as $N = (p^a q^b)^2 = k^2$, where $k = p^a q^b$ has exactly two distinct prime factors.

Thus, the problem reduces to finding the largest perfect square $k^2 \le A$ such that $k$ has exactly two distinct prime factors.

Algorithm:
1. Since $A \le 10^{12}$, we have $k \le 10^6$. We precompute the number of distinct prime factors for all integers up to $10^6$ using a sieve.
2. We collect all $k \in [1, 10^6]$ with exactly 2 distinct prime factors into a sorted list `valid_ks`.
3. For each query $A$, we compute $S = \lfloor \sqrt{A} \rfloor$ using `math.isqrt` for precision.
4. We use binary search (`bisect_right`) to find the largest $k \in \text{valid\_ks}$ such that $k \le S$.
5. The answer is $k^2$.

Complexity:
- Sieve: $O(M \log \log M)$ where $M = 10^6$, which is very fast.
- Query: $O(\log M)$ per query using binary search.
- Total: $O(M \log \log M + Q \log M)$, well within limits for $Q = 2 \times 10^5$.
