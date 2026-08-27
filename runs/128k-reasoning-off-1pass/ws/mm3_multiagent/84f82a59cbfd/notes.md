
## ideation
Core difficulty: We need numbers N ≤ 10^12 that are products of two distinct prime squares: N = p²·q²·... wait, actually the exponent for each prime must be even and positive, so N = p^(2a) * q^(2b) with a,b ≥ 1, p≠q primes. So N = (p^a)² * (q^b)² = (p^a * q^b)². So every 400-number is a perfect square, specifically the square of a number that is the product of two distinct prime powers (each at least to the first power). Equivalently, N = m² where m has exactly two distinct prime factors, each appearing with any positive integer exponent. But simpler: N = p²·q² where p,q are distinct primes and we can also have higher even powers: p^4·q^2, p^2·q^4, etc. So we must generate all numbers of form p^(2a)·q^(2b) with a,b ≥ 1, p≠q, up to 10^12.

Approach options:
1. Generate by iterating over primes and even exponent combinations. For each pair of distinct primes (p,q) and each a,b ≥ 1 compute p^(2a)·q^(2b) ≤ 10^12. Store in sorted list, binary search per query.
2. Observe that the count of such numbers is small. Let's estimate: Primes up to 10^6 (since smallest prime square p² ≤ 10^12 means p ≤ 10^6). Number of primes up to 10^6 ≈ 78,498. For each pair of primes, we can have a=1,b=1 giving p²·q². But we can also increase exponents. However, the number of such numbers is manageable (probably under ~10^6). Generating all and binary searching is feasible.

Pitfalls:
- Must ensure we don't double count (e.g., (p=2,a=1,q=3,b=1) and (p=3,a=1,q=2,b=1) produce same number). Use p < q to avoid duplicates.
- Exponent loops must respect bounds: p^(2a) ≤ 10^12, q^(2b) ≤ 10^12, product ≤ 10^12.
- Edge case: A can be as low as 36 (which is 2²·3² = 36, the smallest 400 number).
- Input size Q up to 2·10^5, so binary search O(log size) is fine. Precomputation one-time cost.

## worker: Generate all 400-numbers up to 10^12 by iterating 
The code generates all 400-numbers up to the maximum query value by:
1. Sieving primes up to `sqrt(max_A)` (since the smallest prime factor squared must be ≤ 10^12).
2. For each prime `p`, iterating over even powers `p^(2a)` (a≥1) while `p^(2a) ≤ max_A`.
3. For each such power, iterating over larger primes `q > p`, iterating over even powers `q^(2b)` (b≥1) while the product `p^(2a)·q^(2b) ≤ max_A`.
4. Storing all distinct products in a set to avoid duplicates, then converting to a sorted list.

Each query is answered via binary search (`bisect_right`) on this sorted list. The precomputation handles at most ~10^6 numbers, well within memory and time limits. Edge cases like `A=36` are covered because 36 = 2²·3² is generated.
