
## ideation
The core insight is that a 400 number is exactly a perfect square whose square root has exactly 2 distinct prime factors. This transforms the problem from "find largest 400 number ≤ A" to "find largest good square ≤ A".

Key observations:
- Since A ≤ 10^12, the square root m ≤ 10^6
- We need m to have exactly 2 distinct prime factors (counted without multiplicity)
- Precompute all good roots up to 10^6 using a sieve
- For each query, binary search for the largest good square ≤ A

Pitfalls to avoid:
- Don't confuse "exactly 2 distinct prime factors" with "exactly 2 prime factors counted with multiplicity"
- The sieve must count distinct primes, not total prime factors
- Edge case: m itself must have exactly 2 distinct primes, so m=1 (0 primes) and m=p^k (1 prime) are excluded

## worker: Implement the complete solution: sieve for distinc
- A 400 number has exactly 2 distinct prime factors p, q, each appearing an even number of times: N = p^{2a} q^{2b} = (p^a q^b)^2 with a, b ≥ 1. So N is a perfect square whose root m = p^a q^b has exactly 2 distinct prime factors.
- Since A ≤ 10^12, m ≤ 10^6. We sieve distinct-prime-factor counts up to 10^6: for each prime i (detected by count == 0), increment the count of every multiple. This is O(LIMIT log log LIMIT) ≈ fast enough (sum of LIMIT/p over primes).
- Collect m² for all m with exactly 2 distinct prime factors; the list is naturally sorted. Answer each query with bisect_right. Total: O(LIMIT log log LIMIT + Q log M).
- Verified against samples: 404 → 400, 36 → 36, 60 → 36, 10^12 → 10^12 (root 10^6 = 2^6·5^6, two distinct primes), 123456789 → 123454321 (=11111², and 11111 = 41·271, two distinct primes).
