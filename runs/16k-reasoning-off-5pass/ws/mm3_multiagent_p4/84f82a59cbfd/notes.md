
## ideation
**Core difficulty:**  
A "400 number" N must be a perfect square with exactly two distinct prime factors, each appearing with exponent at least 1 in the square root. That is, N = (p^a * q^b)^2 where p ≠ q are primes and a, b ≥ 1.

Equivalently, if we let B = p^a * q^b (square‑free w.r.t. exponent parity, but a,b ≥ 1), then N = B^2. So we need all B ≤ 10^6 such that B has exactly two distinct prime factors (any exponents allowed, but at least 1 for each) — then B^2 is a 400 number. Additionally, we can multiply B by a square factor t^2 (t ≥ 1) so long as (B·t)^2 ≤ 10^12, giving numbers like (p^a·q^b·t^2)^2 = p^(2a+2c)·q^(2b+2d)·(other primes)², which still have exactly two distinct odd‑exponent primes, so they remain 400 numbers.

**Candidate approaches:**

1. **Enumerate base B and multiply by squares**  
   - Precompute primes up to 10^6 (≈78k primes).  
   - For each pair of distinct primes (p, q) with p < q ≤ 10^6, compute B = p·q (simplest case).  
   - For each square factor s = t^2 ≤ 10^12 / B^2, compute N = (B·s)^2.  
   - Also include higher powers: for each prime p, generate p^2, p^4, … ≤ 10^6. Combine p^(2a)·q^(2b).  
   - Collect all N ≤ 10^12 into a sorted array, deduplicate.  
   - Answer queries by binary search (bisect_right).

2. **Simpler: iterate B = 1..10^6**  
   - For each B, factorize quickly (sieve smallest prime factor).  
   - If B has exactly two distinct prime factors, then for each square s ≤ 10^12 / B^2, add (B·s)^2.  
   - This handles all cases (since any 400 number N = B^2 with B square‑free w.r.t. parity, but B must have exactly 2 distinct prime factors with any positive integer exponents, so B is a number with exactly 2 distinct prime factors).  
   - Time: 10^6 × number of square factors. Number of squares s ≤ 10^12/B^2 is at most 10^6 (when B=1, but B=1 has 0 prime factors, skip). For small B, many squares; but small B with exactly 2 distinct primes start from 6 (2·3). For B=6, s up to 10^12/36 ≈ 2.7e10, so ~1.6e5 squares. That could be ~10^11 operations — too slow.

3. **Refined enumeration by prime powers**  
   - Precompute all values of form p^(2a) ≤ 10^6 (a ≥ 1). Call these P. Similarly for q.  
   - Enumerate pairs (x, y) from P (distinct underlying primes) with x·y ≤ 10^6.  
   - For each such B = x·y, enumerate square factors s = t^2 ≤ 10^12 / B^2.  
   - This reduces work because each B now already has the minimum even exponents; multiplying by t^2 adds even exponents, keeping the 400‑number property.  
   - But still many s per B. Better: just enumerate all N = (product of prime powers)² directly, i.e., iterate over B with exactly 2 distinct primes, and for each square factor t^2 ≤ 10^12/B^2, compute (B·t)^2. This is essentially the same as approach 1.

4. **Alternative: generate all 400 numbers by iterating over pairs of primes and square factors**  
   - For primes p < q, for exponents a,b ≥ 1, let B = p^a·q^b ≤ 10^6.  
   - For each square s = t^2 with t ≥ 1 and B·s ≤ 10^6, add (B·s)^2.  
   - The number of (p,q) pairs with p·q ≤ 10^6 is manageable. Adding higher powers p^(2a) multiplies the count but still small.  
   - t^2 ≤ 10^12 / B^2, so t ≤ 10^6 / B. For B=6, t up to 1.6e5. For B=30, t up to 3.3e4. Total work is sum over B of (10^6/B), which for B with two distinct primes is roughly O(10^6 · log) — maybe a few million operations, feasible.

5. **Even simpler insight:**  
   - N is a 400 number iff N is a perfect square and the square root of N has exactly two distinct prime factors.  
   - So enumerate all square roots R ≤ 10^6 with exactly two distinct prime factors.  
   - For each such R, compute N = R^2.  
   - Additionally, for each square factor s = t^2 ≤ 10^12 / R^2, compute (R·t)^2.  
   - Actually (R·t) is a new square root with the same distinct prime factors (plus possibly new ones from t, but then it would have more than 2 distinct primes, breaking the condition). Wait!  
   - **Important correction:** If t introduces a new prime factor, then (R·t) would have ≥ 3 distinct primes, and N = (R·t)^2 would NOT be a 400 number. So we must require that t is composed only of primes p and q (the same two primes). In other words, t must be of the form p^c · q^d (with c,d ≥ 0, not both zero). But since t^2 is a perfect square, t must already be a perfect square: t = u^2 where u = p^e · q^f. Then R·t = p^(a+2e) · q^(b+2f), still exactly two distinct primes.  
   - So the enumeration is: pick distinct primes p, q; pick non‑negative integers a,b ≥ 1 (exponents in the base R), and non‑negative integers e,f (from the square factor t^2 = (p^e q^f)^2). Then R_total = p^(a+2e) · q^(b+2f) ≤ 10^6, and N = R_total^2 ≤ 10^12.  
   - This is equivalent to: R_total runs over all numbers ≤ 10^6 with exactly two distinct prime factors. So we just need to enumerate all R ≤ 10^6 with exactly two distinct prime factors, and output R^2. Done! No need to iterate over t separately.  
   - Wait, is that correct? Let R be any number ≤ 10^6 with exactly two distinct prime factors p, q. Write R = p^A · q^B with A,B ≥ 1. Then N = R^2 = p^(2A) · q^(2B). Since 2A and 2B are even, N is a 400 number. So **every** such N is a 400 number, and every 400 number arises this way.  
   - Therefore the set of 400 numbers ≤ 10^12 is exactly { R^2 : R ≤ 10^6, R has exactly two distinct prime factors }.  
   - This is much cleaner! No need to iterate over square factors t.

6. **Count check:**  
   - Number of integers ≤ 10^6 with exactly 2 distinct prime factors.  
   - For a prime pair (p,q) with p<q and p·q ≤ 10^6, and any exponents A,B ≥ 1 with p^A·q^B ≤ 10^6.  
   - Estimate: The number of such R is on the order of a few hundred thousand. For each R we compute R^2.  
   - For example, p=2, q=3: R = 2^A·3^B ≤ 10^6. A can be 1..19 (2^19=524288, 2^20=1048576), B can be 1..12 (3^12=531441). So ~19*12 = 228 pairs for (2,3) alone, but many exceed 10^6. Actually for each A, max B such that 3^B ≤ 10^6/2^A. This gives maybe ~100 pairs per prime pair, and there are ~30k prime pairs with p·q ≤ 10^6. Total maybe a few million? That might be large but still feasible if we iterate carefully.  
   - Alternatively, iterate R = 1..10^6, use SPF to count distinct prime factors, and if exactly 2, add R^2. That's 10^6 operations, trivial!  
   - Then sort the resulting list (~O(N log N) where N is a few hundred thousand) and binary search for each query.  
   - This is the simplest and most efficient approach.

**Pitfalls:**

- Must ensure 400 numbers exist for all A in [36, 10^12]. 36 = 6^2, 6 has prime factors 2 and 3 — yes. So lower bound is fine.  
- The list must be deduplicated and sorted.  
- R=1 (no prime factors) is not included.  
- R must have exactly 2 distinct prime factors, each with exponent ≥ 1. Using SPF array and counting distinct primes.  
- For R up to 10^6, R^2 fits in 64‑bit (≤ 10^12). Use Python int (unbounded).  
- Q up to 2×10^5, binary search with bisect in Python is O(log N) per query, fine.  
- Build the list once, then answer all queries.

**Algorithm:**

1. Precompute smallest prime factor (SPF) for all integers up to 10^6 using sieve.  
2. For each R from 2 to 10^6:  
   - Count distinct prime factors using SPF (divide out).  
   - If exactly 2 distinct primes, add R^2 to list.  
3. Sort and deduplicate the list.  
4. For each query A, binary search the largest value ≤ A (use bisect_right).  
5. Output the result.

**Complexity:**  
- Sieve: O(10^6 log log 10^6).  
- Enumeration: O(10^6) amortized.  
- Number of 400 numbers: roughly sum_{p<q, p·q≤10^6} (log_{p}(10^6/q)+1)*(log_{q}(10^6/p)+1) — estimated < 5×10^5.  
- Sorting: O(N log N).  
- Queries: O(Q log N).  
- Total well within limits.

## worker: Implement the sieve for smallest prime factor up t
- A "400 number" N ≤ 10^12 is exactly a perfect square whose square root R has exactly two distinct prime factors (each with exponent ≥ 1 in R). Since N ≤ 10^12, R ≤ 10^6.
- Sieve smallest prime factor (SPF) up to 10^6 in O(MAX_R log log MAX_R).
- Enumerate every R from 2 to 10^6, count distinct prime factors using SPF. If count == 2, append R^2 to the list.
- Sort the resulting list (a few hundred thousand elements) and answer each query with `bisect_right` to find the largest value ≤ A. Complexity is O(10^6 + N log N + Q log N), easily fast for Q ≤ 2×10^5.
