
## ideation
**Core Difficulty:**
The problem asks for the largest integer $\le A$ satisfying two conditions:
1. Exactly 2 distinct prime factors.
2. Each prime factor has an even exponent.

Mathematically, if $N = p_1^{e_1} p_2^{e_2} \dots$, then $e_1, e_2$ are even and there are exactly 2 such primes.
This implies $N = (p_1^{e_1/2} p_2^{e_2/2})^2$. Let $x = p_1^{e_1/2} p_2^{e_2/2}$. Then $N = x^2$.
The condition "exactly 2 distinct prime factors" for $N$ translates to "$x$ has exactly 2 distinct prime factors".
The constraint $A \le 10^{12}$ means $N \le 10^{12}$, so $x \le 10^6$.
The constraints require $Q \le 2 \times 10^5$ queries, so an $O(1)$ or $O(\log (\text{precomputed size}))$ per query solution is needed. Precomputing all valid $x$ up to $10^6$ and storing their squares is the optimal approach.

**Candidate Approaches:**
1.  **Sieve-based Generation:**
    -   Iterate through all numbers $x$ from $2$ to $10^6$.
    -   For each $x$, count its distinct prime factors.
    -   If count == 2, include $x^2$ in a list.
    -   To efficiently count distinct prime factors for all numbers up to $10^6$, use a linear sieve (Euler sieve) or a modified Sieve of Eratosthenes that stores the smallest prime factor (SPF) or directly counts distinct factors.
    -   Sort the resulting list of squares.
    -   For each query, use `bisect_right` to find the insertion point and return the element before it.

2.  **Iterative Construction (Less Efficient):**
    -   Iterate pairs of primes $(p, q)$ with $p < q$.
    -   Iterate exponents $a, b$ (even) such that $p^a q^b \le 10^{12}$.
    -   Store $p^a q^b$.
    -   This involves nested loops and might be slightly slower to implement correctly without bounds checking, though the number of valid numbers is small enough. The sieve approach is more systematic for checking "exactly 2 factors" for every number.

**Pitfalls:**
-   **Data Types:** $A$ can be up to $10^{12}$, so standard 32-bit integers are insufficient. Python handles large integers automatically, but logic must ensure no overflow in other languages (not an issue here).
-   **Edge Cases:** The smallest 400 number is $2^2 \cdot 3^2 = 36$. The constraints say $A \ge 36$, so a solution always exists.
-   **Efficiency:** Generating the list must be fast ($< 0.1s$). A simple sieve up to $10^6$ is very fast.
-   **Binary Search:** Must use the correct variant (`bisect_right` in Python) to find the largest element $\le A$. If `bisect_right` returns index `i`, the answer is at `i-1`.

**Plan:**
1.  Implement a sieve up to $10^6$ to compute `omega[x]` (number of distinct prime factors) for each $x$.
2.  Collect $x^2$ where `omega[x] == 2` into a list `valid_numbers`.
3.  Sort `valid_numbers`.
4.  Read $Q$ and process queries using binary search.

## worker: Write the Python code implementing the sieve logic
1.  **Algorithm Selection**: The problem requires finding the largest integer $\le A$ with exactly two distinct prime factors, each with an even exponent. This structure implies the number is a perfect square of a composite number with exactly two distinct prime factors ($N = (p^k q^m)^2$).
2.  **Precomputation**: Since $A \le 10^{12}$, the base number $x = \sqrt{N}$ is at most $10^6$. We precompute the number of distinct prime factors for all integers up to $10^6$ using a sieve-like method.
    -   Initialize an array `omega` of size $10^6 + 1$.
    -   Iterate $i$ from 2 to $10^6$. If `omega[i]` is 0, $i$ is prime.
    -   For each prime $i$, increment `omega[j]` for all multiples $j$ of $i$.
3.  **Generation**: Iterate $x$ from 2 to $10^6$. If `omega[x] == 2`, add $x^2$ to a list `valid_numbers`. Since we iterate $x$ in increasing order, the list is automatically sorted.
4.  **Query Processing**: For each query $A$, use binary search (`bisect_right`) on `valid_numbers` to find the largest element $\le A$. The time complexity per query is $O(\log(\text{count}))$, which is very efficient given $Q \le 2 \times 10^5$.
5.  **Complexity**:
    -   Sieve: $O(N \log \log N)$ where $N=10^6$. Very fast.
    -   Query: $O(Q \log N)$.
    -   Total time is well within limits (typically < 1 second for Python).

## worker: Run the code against the provided sample inputs to
The code implements the logic derived in the planning phase:
1.  **Precomputation**: It uses a sieve-like approach up to $10^6$ to count the number of distinct prime factors (`omega`) for every integer.
2.  **Generation**: It iterates through numbers $x$ up to $10^6$. If `omega[x] == 2`, it calculates $x^2$ and adds it to `valid_numbers`. Since $x$ is iterated in increasing order, `valid_numbers` is automatically sorted.
3.  **Query Processing**: For each query $A$, it uses `bisect_right` to find the largest precomputed 400 number less than or equal to $A$.
4.  **Efficiency**: The sieve runs in $O(N \log \log N)$ where $N=10^6$, and each query takes $O(\log (\text{count}))$. This fits well within the time limits for $Q=2 \times 10^5$.
5.  **Verification**: The logic correctly handles the sample inputs. For example, for $A=404$, it finds 400 ($20^2$, where $20=2^2 \cdot 5$ has 2 distinct prime factors). For $A=36$, it finds 36 ($6^2$, where $6=2 \cdot 3$ has 2 distinct prime factors).

## worker: Run the provided sample input to verify the output
The code implements the logic derived in the planning phase:
1.  **Precomputation**: It uses a sieve-like approach up to $10^6$ to count the number of distinct prime factors (`omega`) for every integer.
2.  **Generation**: It iterates through numbers $x$ up to $10^6$. If `omega[x] == 2`, it calculates $x^2$ and adds it to `valid_numbers`. Since $x$ is iterated in increasing order, `valid_numbers` is automatically sorted.
3.  **Query Processing**: For each query $A$, it uses `bisect_right` to find the largest precomputed 400 number less than or equal to $A$.
4.  **Efficiency**: The sieve runs in $O(N \log \log N)$ where $N=10^6$, and each query takes $O(\log (\text{count}))$. This fits well within the time limits for $Q=2 \times 10^5$.
5.  **Verification**: The logic correctly handles the sample inputs. For example, for $A=404$, it finds 400 ($20^2$, where $20=2^2 \cdot 5$ has 2 distinct prime factors). For $A=36$, it finds 36 ($6^2$, where $6=2 \cdot 3$ has 2 distinct prime factors).

## worker: finalize
The solution implements a precomputation strategy based on the mathematical properties of "400 numbers".
1.  **Mathematical Insight**: A number $N$ is a 400 number if it has exactly two distinct prime factors, say $p$ and $q$, and each appears with an even exponent. This means $N = p^{2k} \cdot q^{2m} = (p^k \cdot q^m)^2$. Thus, $N$ must be a perfect square of some integer $x = p^k \cdot q^m$, where $x$ has exactly two distinct prime factors.
2.  **Constraints Analysis**: Since $A \le 10^{12}$, the base number $x = \sqrt{N}$ is at most $10^6$.
3.  **Algorithm**:
    -   Use a sieve-like method to compute the number of distinct prime factors (`omega`) for every integer up to $10^6$.
    -   Iterate through $x$ from 2 to $10^6$. If `omega[x] == 2`, then $x^2$ is a valid 400 number.
    -   Store these valid numbers in a sorted list.
    -   For each query $A$, use binary search (`bisect_right`) to find the largest precomputed number $\le A$.
4.  **Complexity**:
    -   Sieve: $O(N \log \log N)$ where $N=10^6$.
    -   Query Processing: $O(Q \log (\text{count of valid numbers}))$.
    -   This approach is highly efficient and fits well within the time limits for $Q=2 \times 10^5$.
