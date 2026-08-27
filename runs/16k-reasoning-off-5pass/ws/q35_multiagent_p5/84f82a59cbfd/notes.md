
## ideation
The core difficulty lies in efficiently generating all "400 numbers" up to $10^{12}$ and answering queries.
1.  **Characterization**: A 400 number is of the form $p^{2a} q^{2b}$ with distinct primes $p, q$ and $a,b \ge 1$. This is equivalent to $(p^a q^b)^2$. Let $k = p^a q^b$. Then the 400 number is $k^2$.
2.  **Constraint on k**: Since the 400 number $\le 10^{12}$, we have $k^2 \le 10^{12} \implies k \le 10^6$.
3.  **Condition on k**: $k$ must have exactly 2 distinct prime factors. The exponents of these primes in the factorization of $k$ can be any integer $\ge 1$.
4.  **Algorithm**:
    *   Precompute primes up to $10^6$ using a sieve.
    *   For each prime $p$, iterate through powers $p^a$ such that $p^a \le 10^6$.
    *   For each such $p^a$, iterate through other primes $q > p$ and powers $q^b$ such that $p^a q^b \le 10^6$.
    *   Collect all such products $k = p^a q^b$.
    *   Square each $k$ to get the 400 number.
    *   Sort the list of 400 numbers.
    *   For each query $A$, use binary search (`bisect_right`) to find the largest 400 number $\le A$.

Pitfalls:
-   Double counting: Ensure we generate each pair $(p, q)$ with $p < q$ exactly once.
-   Performance: The number of such $k$ values is manageable. The number of primes up to $10^6$ is 78,498. The inner loop runs for each prime power. The total number of valid $k$ values is roughly proportional to the number of integers $\le 10^6$ with exactly 2 distinct prime factors, which is not too large (approx $10^6 \times \frac{\ln \ln 10^6}{\ln 10^6}$? No, it's smaller. Actually, we can just generate them).
-   Memory: Storing all 400 numbers. The count is not huge. Let's estimate: The number of integers $\le X$ with exactly 2 distinct prime factors is roughly $X \frac{\ln \ln X}{\ln X}$. For $X=10^6$, this is about $10^6 \times \frac{2}{14} \approx 140,000$. Squaring them gives numbers up to $10^{12}$. Sorting 140,000 integers is fast.

## worker: (None)
1.  **Characterization**: A 400 number is defined as $N = p^{2a} q^{2b}$ for distinct primes $p, q$ and $a, b \ge 1$. This can be rewritten as $N = (p^a q^b)^2$. Let $k = p^a q^b$. Then $N = k^2$.
2.  **Constraints**: Since $N \le 10^{12}$, we have $k^2 \le 10^{12} \implies k \le 10^6$.
3.  **Generation**: We need to find all integers $k \le 10^6$ that have exactly 2 distinct prime factors. The exponents of these prime factors in $k$ can be any integer $\ge 1$.
4.  **Algorithm**:
    *   Use a sieve to generate all primes up to $10^6$.
    *   Iterate through each prime $p$ and its powers $p^a \le 10^6$.
    *   For each $p^a$, iterate through primes $q > p$ and their powers $q^b$ such that $p^a q^b \le 10^6$.
    *   Store each valid product $k = p^a q^b$ in a set to avoid duplicates (though the nested loop structure with $p < q$ naturally avoids duplicates).
    *   Square each $k$ to get the corresponding 400 number.
    *   Sort the list of 400 numbers.
    *   For each query $A$, use `bisect_right` to find the largest 400 number $\le A$.
5.  **Complexity**:
    *   Sieve: $O(MAX\_K \log \log MAX\_K)$.
    *   Generating $k$: The number of such $k$ is roughly proportional to the count of integers $\le 10^6$ with exactly 2 distinct prime factors. This is manageable (around 100k-200k). The nested loops run efficiently because the inner loop breaks early when the product exceeds $MAX\_K$.
    *   Sorting: $O(M \log M)$ where $M$ is the number of valid $k$'s.
    *   Queries: $O(Q \log M)$.
    *   Overall complexity is well within limits for $Q=2 \times 10^5$ and $MAX\_K=10^6$.
