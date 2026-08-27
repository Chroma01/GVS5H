
## ideation
The problem asks us to find the largest "400 number" not exceeding A.
A "400 number" $N$ is defined by:
1. $N$ has exactly 2 distinct prime factors.
2. For each prime factor $p$, the exponent of $p$ in the prime factorization of $N$ is even.

Let the prime factorization of $N$ be $N = p_1^{e_1} p_2^{e_2}$.
Condition 2 implies $e_1, e_2$ are even. Let $e_1 = 2a, e_2 = 2b$ for integers $a, b \ge 1$.
Then $N = p_1^{2a} p_2^{2b} = (p_1^a p_2^b)^2$.
Let $Y = p_1^a p_2^b$. Then $N = Y^2$.
Since $N$ has exactly 2 distinct prime factors, $Y$ must also have exactly 2 distinct prime factors.
Thus, the problem reduces to finding the largest integer $Y \le \lfloor\sqrt{A}\rfloor$ such that $Y$ has exactly 2 distinct prime factors. Then the answer is $Y^2$.

Constraints:
$Q \le 2 \times 10^5$.
$A \le 10^{12} \implies \sqrt{A} \le 10^6$.
We need to answer queries efficiently.
We can precompute the number of distinct prime factors for all integers up to $10^6$ using a sieve.
Then, we can precompute a lookup table `max_valid[k]` which stores the largest integer $\le k$ having exactly 2 distinct prime factors.
For each query, we compute $K = \lfloor\sqrt{A}\rfloor$, retrieve `max_valid[K]`, and output the square.

Complexity:
Precomputation: $O(M \log \log M)$ where $M = 10^6$.
Query: $O(1)$.
Total Time: $O(M \log \log M + Q)$.
Space: $O(M)$.
This fits well within the time and memory limits.

Pitfalls:
- Integer overflow: $Y^2$ can be up to $10^{12}$, which fits in a 64-bit integer. Python handles large integers automatically.
- Input/Output speed: With $2 \times 10^5$ queries, using `input()` and `print()` might be too slow. Use `sys.stdin.read` and `sys.stdout.write`.
- Sieve implementation: Ensure `cnt[i]` correctly counts distinct prime factors.
- `math.isqrt` availability: Use it if Python 3.8+, otherwise `int(A**0.5)`.
