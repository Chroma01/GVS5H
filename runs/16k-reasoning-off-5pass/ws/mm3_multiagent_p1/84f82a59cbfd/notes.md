
## ideation
The set of 400 numbers is exactly {M^2 : M has exactly 2 distinct prime factors}. For a given A, we need the largest M^2 ≤ A, which is equivalent to the largest M ≤ √A with exactly 2 distinct prime factors, then output M^2. Since A ≤ 1e12, √A ≤ 1e6. Precomputing all numbers ≤ 1e6 with exactly two distinct prime factors via a modified sieve and storing them sorted allows O(log N) per query.

## worker: Implement a sieve up to 1,000,000 to compute the n
- I implemented a sieve that counts the number of distinct prime factors (ω(n)) for all n up to 1,000,000.
- The sieve works by iterating over each integer i; if ω(i) == 0 then i is prime, and for every multiple of i we increment ω, ensuring each distinct prime factor is counted exactly once.
- All numbers n with exactly 2 distinct prime factors are collected in a sorted list `good`.
- For each query A, I compute floor(sqrt(A)) (with correction to avoid floating point issues) and binary search in `good` for the largest element ≤ that value.
- The answer is the square of that found number.
- This runs in O(N log log N + Q log N) time and O(N) memory, which is well within limits for N=1e6 and Q=2e5.

## worker: Test the solution with the provided sample input t
The solution correctly identifies 400 numbers as squares of numbers with exactly two distinct prime factors. The sieve counts distinct prime factors (ω) for all n ≤ 1e6, collects those with ω=2, and binary searches for each query. The sqrt correction uses while loops to adjust for floating-point inaccuracies, which is safe for A up to 1e12 since s is at most 1e6 and the adjustment is bounded by 1-2 steps.

## worker: finalize
- A 400 number is exactly a perfect square of an integer with exactly two distinct prime factors: $N = p^{2a} q^{2b} = (p^a q^b)^2$.
- For each query, we need the largest $M$ with exactly 2 distinct prime factors such that $M^2 \le A$, i.e., $M \le \lfloor\sqrt{A}\rfloor$.
- The maximum $\sqrt{A}$ is $10^6$ (when $A = 10^{12}$), so we precompute all numbers up to $10^6$ with exactly 2 distinct prime factors using a sieve that counts distinct prime factors (ω).
- For each query, we compute $\lfloor\sqrt{A}\rfloor$ (with corrections for floating-point inaccuracies) and binary search the sorted list `good` for the largest value $\le$ that square root. The answer is that value squared.
- Complexity: sieve $O(N \log \log N)$, queries $O(Q \log N)$ with $N = 10^6$, $Q \le 2 \times 10^5$. Memory $O(N)$.
