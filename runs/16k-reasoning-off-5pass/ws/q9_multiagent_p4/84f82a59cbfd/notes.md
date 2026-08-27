
## ideation
**Core Difficulty:**
The problem asks for the largest integer $\le A$ with exactly two distinct prime factors, each appearing with an even exponent.
1.  **Mathematical Transformation**: If $N = p_1^{e_1} p_2^{e_2} \dots$, the condition "exactly 2 distinct prime factors" and "each exponent is even" implies $N = p_1^{2k} p_2^{2m} = (p_1^k p_2^m)^2$.
2.  **Simplification**: Let $X = p_1^k p_2^m$. Then $N = X^2$. The condition on $N$ translates directly to: $X$ must have exactly two distinct prime factors. The exponents of these primes in $X$ ($k$ and $m$) can be any positive integer (since $2k, 2m$ are even).
3.  **Constraints**: $A \le 10^{12}$. Thus $X \le \sqrt{10^{12}} = 10^6$.
4.  **Query Nature**: $Q \le 2 \times 10^5$. We need an efficient way to answer queries. Since the maximum $X$ is small ($10^6$), we can precompute all valid $X$ values up to $10^6$.
5.  **Algorithm**:
    *   Precompute a boolean array or list of numbers up to $10^6$ that have exactly 2 distinct prime factors.
    *   For each query $A$, compute $S = \lfloor\sqrt{A}\rfloor$.
    *   Find the largest precomputed valid number $\le S$.
    *   Output the square of that number.

**Candidate Approaches:**
1.  **Sieve-like Precomputation**:
    *   Iterate from 2 to $10^6$.
    *   For each number, count distinct prime factors.
    *   Store numbers with count == 2 in a sorted list.
    *   Use binary search (`bisect_right`) on this list for each query.
    *   Complexity: Precomputation $O(M \log \log M)$ or $O(M)$ where $M=10^6$. Query $O(\log (\text{count}))$. Total time well within limits.

2.  **Direct Factorization per Query**:
    *   For each query, iterate downwards from $\lfloor\sqrt{A}\rfloor$. Check if the number has exactly 2 distinct prime factors.
    *   Worst case: $A \approx 10^{12}$, $\sqrt{A} = 10^6$. If the gap between valid numbers is large, this could be slow. Given constraints and density of such numbers, it might pass, but precomputation is safer and cleaner.

**Pitfalls:**
*   **Definition of "Distinct Prime Factors"**: Ensure we count distinct primes, not total exponents. E.g., $12 = 2^2 \cdot 3^1$ has 2 distinct primes. $36 = 2^2 \cdot 3^2$ has 2 distinct primes. $6 = 2 \cdot 3$ has 2 distinct primes.
*   **Edge Cases**: $A$ is small (min 36). The smallest valid number is $2^1 \cdot 3^1 = 6$ (since $6^2=36$). The problem guarantees a solution exists.
*   **Integer Overflow**: Python handles large integers automatically, but logic must ensure we don't square a number $> 10^6$ if not needed.
*   **Efficiency**: Doing trial division for every number up to $10^6$ inside the precomputation loop might be slightly slow if not optimized (e.g., using a sieve to store smallest prime factor or just counting during a sieve). A simple sieve counting distinct primes is very fast.

**Plan Details**:
1.  Create an array `distinct_primes` of size $10^6 + 1$, initialized to 0.
2.  Iterate $i$ from 2 to $10^6$.
3.  If `distinct_primes[i] == 0` (it's prime), iterate through its multiples $j = i, 2i, \dots$ and increment `distinct_primes[j]`.
    *   *Correction*: Standard sieve increments for every multiple. This correctly counts distinct prime factors because each prime $p$ is added to the count of all its multiples exactly once.
4.  Collect all $x$ where `distinct_primes[x] == 2` into a list `valid_roots`.
5.  For each query $A$:
    *   $limit = \text{isqrt}(A)$.
    *   Find index in `valid_roots` using binary search such that `valid_roots[idx] <= limit`.
    *   Result is `valid_roots[idx] ** 2`.

## worker: Implement the sieve to count distinct prime factor
1.  **Mathematical Insight**: A number $N$ is a "400 number" if it has exactly two distinct prime factors $p, q$ and their exponents in the prime factorization are even. This means $N = p^{2k} q^{2m} = (p^k q^m)^2$. Let $X = p^k q^m$. Then $N = X^2$. The condition simplifies to finding the largest perfect square $X^2 \le A$ such that $X$ has exactly two distinct prime factors.
2.  **Precomputation**: Since $A \le 10^{12}$, $X \le 10^6$. We can precompute the number of distinct prime factors for every integer up to $10^6$ using a sieve-like method.
    *   Initialize an array `counts` of size $10^6+1$ to 0.
    *   Iterate $i$ from 2 to $10^6$. If `counts[i]` is 0, $i$ is prime. Iterate through all multiples of $i$ and increment their count.
    *   Collect all $x$ where `counts[x] == 2` into a sorted list `valid_roots`.
3.  **Query Processing**: For each query $A$, calculate $S = \lfloor\sqrt{A}\rfloor$. Use binary search (`bisect_right`) on `valid_roots` to find the largest element $\le S$. The answer is the square of that element.
4.  **Complexity**:
    *   Precomputation: $O(M \log \log M)$ where $M=10^6$, which is very fast.
    *   Query: $O(\log (\text{number of valid roots}))$. With $Q=2 \cdot 10^5$, total time is well within limits.

## worker: Run the code against the provided sample inputs to
The code implements the logic derived in the thought process:
1.  **Precomputation**: It uses a sieve-like approach to count distinct prime factors for all numbers up to $10^6$. This is efficient ($O(N \log \log N)$).
2.  **Filtering**: It collects numbers with exactly 2 distinct prime factors into a sorted list `valid_roots`.
3.  **Query Handling**: For each query $A$, it calculates $\lfloor\sqrt{A}\rfloor$ and uses binary search (`bisect_right`) to find the largest precomputed valid root less than or equal to this limit. The answer is the square of that root.
4.  **Verification**:
    *   Query 404: $\sqrt{404} \approx 20.09$. Largest valid root $\le 20$ is 10 ($2 \times 5$). $10^2 = 100$. Wait, let's re-check the sample logic.
    *   Sample 1 says for 404, answer is 400.
    *   $400 = 20^2$. $20 = 2^2 \times 5^1$. Distinct primes are 2 and 5. Count is 2. Correct.
    *   My manual trace: $\sqrt{404} = 20$. Is 20 in `valid_roots`? Yes, distinct primes of 20 are {2, 5}, count is 2. So `bisect_right` will point after 20, index - 1 = index of 20. $20^2 = 400$. Correct.
    *   Sample 36: $\sqrt{36} = 6$. $6 = 2 \times 3$. Count 2. $6^2 = 36$. Correct.
    *   Sample 60: $\sqrt{60} \approx 7.7$. Valid roots $\le 7$: 6. $6^2 = 36$. Correct.
    *   Sample $10^{12}$: $\sqrt{10^{12}} = 10^6$. $10^6 = 2^6 \times 5^6$. Distinct primes {2, 5}. Count 2. $10^{12}$ is valid. Correct.
    *   Sample 123456789: $\sqrt{123456789} \approx 11111.11$. We need largest valid root $\le 11111$. The sample output is 123454321. $\sqrt{123454321} = 11111$. Let's check 11111. $11111 = 41 \times 271$. Both prime. Count 2. So $11111^2 = 123454321$. Correct.

The logic holds.
