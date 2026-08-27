
## ideation
**Core Difficulty**:
The problem requires finding the largest integer $N \le A$ such that $N = p^{2k} q^{2m}$ for distinct primes $p, q$. This implies $N$ must be a perfect square, say $X^2$, where $X = p^k q^m$. Thus, $X$ must have exactly two distinct prime factors. The constraints are $A \le 10^{12}$, so $X \le 10^6$. With $Q = 2 \times 10^5$ queries, we need an efficient way to check the property of $X$ and search downwards from $\lfloor\sqrt{A}\rfloor$.

**Candidate Approaches**:
1.  **Precomputation + Linear Search**:
    -   Sieve up to $10^6$ to compute the number of distinct prime factors for each integer.
    -   For each query, calculate $L = \lfloor\sqrt{A}\rfloor$.
    -   Iterate $X$ from $L$ down to the smallest possible value (e.g., $2 \times 3 = 6$). The first $X$ with exactly 2 distinct prime factors is the answer ($X^2$).
    -   *Optimization*: Precompute a boolean array or list of "valid" $X$ values. If the density is high, linear search is fast. If not, we might need to jump or use a precomputed array of the largest valid number $\le i$.
    -   Given the density of numbers with exactly 2 prime factors (roughly proportional to $\frac{\ln \ln n}{\ln n}$? No, actually the count of numbers with exactly $k$ prime factors is related to the Dickman function or similar, but for $k=2$ it's quite dense. The count of semiprimes and their multiples up to $10^6$ is significant).
    -   Actually, the condition is $X = p^a q^b$. These are numbers with exactly 2 distinct prime factors. The count of such numbers up to $10^6$ is substantial. A linear scan downwards should hit a valid number very quickly on average.

2.  **Precomputed Array of Answers**:
    -   Create an array `ans[i]` which stores the largest valid $X \le i$.
    -   Fill this array in $O(MAX\_X)$ time.
    -   Each query becomes $O(1)$: compute $L = \lfloor\sqrt{A}\rfloor$, return `ans[L]^2`.
    -   This is robust against worst-case scenarios where a valid number is far below $L$.

## worker: Implement the Sieve of Eratosthenes up to $10^6$ t
1.  **Problem Analysis**: The problem asks for the largest integer $N \le A$ with exactly two distinct prime factors $p, q$ such that the exponent of each in the prime factorization is even. This implies $N = p^{2k} q^{2m} = (p^k q^m)^2$. Thus, $N$ must be a perfect square, say $X^2$, where $X = p^k q^m$. The condition simplifies to finding the largest $X \le \sqrt{A}$ such that $X$ has exactly two distinct prime factors.
2.  **Constraints**: $A \le 10^{12}$, so $X \le 10^6$. $Q \le 2 \times 10^5$.
3.  **Algorithm**:
    -   **Precomputation**: Use a Sieve of Eratosthenes up to $10^6$ to count the number of distinct prime factors for every integer. This takes $O(N \log \log N)$ where $N=10^6$.
    -   **Filtering**: Mark numbers with exactly 2 distinct prime factors.
    -   **Prefix Max Array**: Construct an array `max_valid` where `max_valid[i]` stores the largest valid number $\le i$. This allows $O(1)$ lookup per query.
    -   **Query Processing**: For each query $A$, compute $L = \lfloor\sqrt{A}\rfloor$. The answer is `max_valid[L]^2`.
4.  **Complexity**:
    -   Sieve: $O(MAX\_X \log \log MAX\_X) \approx 10^6$ operations.
    -   Prefix Max: $O(MAX\_X)$.
    -   Queries: $O(Q)$.
    -   Total Time: Well within limits for 2 seconds.
    -   Space: $O(MAX\_X)$ for arrays, approx 4-8 MB, well within limits.

## worker: Run the code against the provided sample inputs to
The code implements the logic derived in the thought process:
1.  **Mathematical Insight**: A "400 number" $N$ must be of the form $p^{2k}q^{2m}$, which implies $N = (p^k q^m)^2$. Thus, $N$ is a perfect square of a number $X$ that has exactly two distinct prime factors.
2.  **Constraints**: Since $A \le 10^{12}$, $X \le 10^6$. We can precompute properties for all $X$ up to $10^6$.
3.  **Precomputation**:
    -   Use a sieve to count distinct prime factors for every number up to $10^6$.
    -   Mark numbers with exactly 2 distinct prime factors as valid.
    -   Build a prefix maximum array `max_valid` where `max_valid[i]` stores the largest valid number $\le i$. This allows $O(1)$ retrieval per query.
4.  **Query Processing**: For each query $A$, calculate $L = \lfloor\sqrt{A}\rfloor$. The answer is `max_valid[L]^2`.
5.  **Complexity**: Sieve takes $O(N \log \log N)$, prefix array takes $O(N)$, and queries take $O(Q)$. With $N=10^6$ and $Q=2 \times 10^5$, this fits well within time limits.

## worker: Run the provided sample input to verify the output
The solution correctly implements the logic derived:
1.  **Mathematical Reduction**: A "400 number" $N$ must be a perfect square $X^2$ where $X$ has exactly two distinct prime factors.
2.  **Precomputation**:
    -   Sieve up to $10^6$ to count distinct prime factors for every number.
    -   Identify numbers with exactly 2 distinct prime factors.
    -   Build a `max_valid` array where `max_valid[i]` is the largest valid number $\le i$. This allows $O(1)$ query response.
3.  **Query Handling**: For each $A$, compute $L = \lfloor\sqrt{A}\rfloor$, look up `max_valid[L]`, and square it.
4.  **Verification**:
    -   Input: `404` -> $\sqrt{404} \approx 20.09 \to L=20$. Valid numbers $\le 20$: $6, 10, 12, 15, 18, 20$. Max is $20$. $20^2 = 400$. Correct.
    -   Input: `36` -> $\sqrt{36} = 6 \to L=6$. Valid $\le 6$: $6$. $6^2 = 36$. Correct.
    -   Input: `60` -> $\sqrt{60} \approx 7.7 \to L=7$. Valid $\le 7$: $6$. $6^2 = 36$. Correct.
    -   Input: `10^12` -> $L=10^6$. $10^6 = 2^6 \cdot 5^6$ (2 distinct factors). Valid. $10^{12}$. Correct.
    -   Input: `123456789` -> $\sqrt{123456789} \approx 11111.11 \to L=11111$. The code finds the largest valid $X \le 11111$. The sample output is $123454321 = 11111^2$. Since $11111 = 41 \times 271$ (2 distinct primes), $11111$ is valid. So the answer is $11111^2$. Correct.

The logic holds and matches sample outputs.
