
## ideation
**Core difficulty:** For each index `i`, we must find the maximum GCD achievable when we pick `K` elements that must include `A_i`.  
The GCD of a set containing `A_i` must be a divisor `d` of `A_i`. To have GCD = `d`, we need at least `K-1` *other* elements divisible by `d`, i.e., the total count of numbers in the whole array divisible by `d` must be at least `K`.  
Thus the answer for `i` is simply: `max{ d | d divides A_i and cnt[d] >= K }`.

**Candidate approaches:**
1. **Brute force per i** – try all subsets of size K-1 among numbers divisible by a candidate divisor. Too slow.
2. **Pre‑compute divisor counts** – Count, for every `v` (1…maxA), how many array elements are multiples of `v`. This can be done in `O(maxA log maxA)` using a frequency array + multiple‑sum pass (sieve‑like).  
3. **Per‑i enumeration of divisors** – Factor `A_i` (or enumerate divisors by trial division up to sqrt(A_i) or by prime factors) to get all its divisors, then pick the largest one whose count is ≥ K.  
4. **Use smallest prime factor (SPF) sieve** to quickly factor each `A_i` and generate its divisors efficiently.

**Pitfalls:**
- N can be up to 1.2e6 → output must be generated quickly (use `sys.stdout.write` or join into list).
- maxA = 1e6 → arrays of size 1e6+5 are fine.
- Need to handle K = N correctly (then count[d] must be exactly N if d divides all chosen numbers, but we only need ≥ N).
- When K = 1 (allowed because “at most N”), the answer is just `A_i` itself, because we pick the K elements = just `A_i`. The divisor‑count method still works: the largest divisor of `A_i` is `A_i` itself, and `cnt[A_i] ≥ 1` is always true. Good.
- The input numbers can be up to 1e6, so a simple frequency array works.
- Counting multiples: standard trick:
  ```python
  cnt = [0] * (maxA+1)
  for x in A: cnt[x] += 1
  for v in range(1, maxA+1):
      for m in range(v, maxA+1, v):
          cnt_divisible[v] += cnt[m]   # but we can store directly in cnt
  ```
  A common optimization is to reuse the freq array as the “divisible count” array, overwriting it. But we need the original frequencies for the inner loop? We can store them in a separate `freq` array or do the pass in place if we are careful (first copy freq into a separate `mult` array, or simply compute directly using an auxiliary array).  
  Given memory 1e6 * 2 ~ 8 MB (if using int), it’s fine.

- Complexity of divisor enumeration for each A_i: number of divisors of numbers up to 1e6 is at most ~240 (for 720720). With N=1.2e6, worst-case operations ~ 1.2e6 * 240 ≈ 2.88e8, which might be borderline in Python. We need an efficient way.

**Better complexity plan:**
- Use smallest prime factor (SPF) sieve up to 1e6 → O(maxA log log maxA).
- For each A_i, factor it into primes with exponents, generate all divisors via recursion or iterative product. Since maxA=1e6, the number of divisors per number is small on average (the maximum is ~240, but that happens for highly composite numbers; many numbers have few divisors). This should be fast enough in PyPy with careful loops.
- For each A_i, iterate over its divisors; we could also iterate over multiples of each divisor? No, divisor enumeration is the direct way.
- To speed up, we can iterate divisors in decreasing order until we find one with count >= K, then break. Since we need the maximum, once we find a valid divisor, no larger divisor exists (we're iterating decreasing). So we can stop early. But generating divisors in sorted order requires generating all and then taking max; generating only the largest might be complicated. Instead, we can pre‑compute for every possible divisor value `d` whether `cnt[d] >= K`. Then for each A_i, we only need to test its divisors; we can keep a running maximum. The average number of divisors is small (~100 for typical 1e6 numbers), so per element is fine.
- Even simpler: since we have `cnt` for all `v`, we can for each `A_i` just loop over all divisors (generated efficiently) and compute `max(d for d in divisors(A_i) if cnt[d] >= K)`. This is O(total divisors) ~ N * average divisors, which is okay.

**Final plan:**
1. Read N, K, array A.
2. Find maxA = max(A).
3. Build frequency array `freq` of size maxA+1: `freq[x] = number of occurrences of x`.
4. Build `cnt` (size maxA+1) initialized to 0. For each `v` in 1..maxA:
     for `m` in range(v, maxA+1, v):
         cnt[v] += freq[m]
   This is a harmonic-sum O(maxA log maxA) pass (~1e6 * (1 + 1/2 + ... ) ≈ 1e6 * log(1e6) ≈ 20e6). Acceptable.
5. For each i from 1 to N:
     Get value x = A[i].
     Find all divisors of x. Use SPF to factor x into (p, e) pairs, then generate all divisors by multiplication.
     Initialize ans = 1 (since at worst the GCD is 1, and we always have cnt[1] = N >= K, so ans exists).
     For each divisor d:
         if cnt[d] >= K and d > ans: ans = d
     Print ans.
6. Use fast output: accumulate results in a list of strings and `'\n'.join`, then `sys.stdout.write`.

**Edge cases:**
- K = 1: then we need to pick just A_i. The largest divisor of A_i with count >= 1 is A_i itself (cnt[A_i] >= 1). So ans = A_i. Our method works.
- All numbers distinct, K = N: then we need a divisor d that divides all numbers. The only such d is gcd of all numbers. The answer for each i is that gcd. Our method: the largest divisor d of A_i such that cnt[d] >= N. This will be the global gcd. Works.
- Large K but small counts: e.g., K > max cnt[v] for any v dividing A_i, then ans = 1? Wait, can we always achieve GCD=1? Yes, because we can always pick any K numbers including A_i, and GCD can be 1 if we include a number coprime to others or simply because not all share a common factor. But is it guaranteed that we can get GCD=1? Not necessarily if K=1? K=1: GCD is A_i itself, not 1. But our method: the largest divisor d of A_i with cnt[d] >= 1 is A_i (since cnt[A_i] >= 1). So ans = A_i. That's correct.
  For K>=2: we can always achieve GCD=1 by picking A_i and any other K-1 numbers (since we can always pick some numbers; the GCD of the set could be 1 if the set doesn't share a common factor >1). But wait, is it always possible to force GCD=1? The problem asks for the maximum possible GCD. It might be that all numbers are multiples of some prime p, and we need to pick K numbers. The GCD could be at least p. But if we can pick numbers that are not all multiples of p, we can get GCD 1. However, if the array consists solely of multiples of p, then any subset will have GCD at least p, and we could get exactly p by choosing numbers that have exactly p as common factor? Actually, if all numbers are multiples of p, the GCD of any subset is a multiple of p. But can we get exactly p? Not necessarily; it could be larger. But 1 is not achievable. However, our method will give the correct answer: the largest divisor d of A_i with cnt[d] >= K. Since all numbers are multiples of p, p divides A_i and cnt[p] = N >= K, so ans >= p. If p is the maximum such divisor, ans = p (or larger). So we don't need to worry about a default of 1; the method naturally finds the correct max.

**Complexities:**
- Time: O(maxA log maxA + N * τ(maxA)) where τ is divisor count. In practice, N=1.2e6, maxA=1e6, τ(maxA) ~ up to 240, but average is much lower. Should run in < 2-3 seconds in PyPy with optimizations (e.g., using local variables, not using list of lists for SPF, using array module or simple list).
- Memory: O(maxA) for freq and cnt, plus O(maxA) for SPF (can be stored as int array of size maxA+1). Total ~ 3 * 1e6 * 8 bytes = 24 MB, plus array A (1.2e6 * 28 bytes for Python ints → too big? Actually Python int is ~28 bytes, 1.2e6 * 28 = 33.6 MB, still okay but heavy). To reduce memory, we can read A and store in a list of ints (which are Python objects). That is necessary to iterate later. Or we can process the queries as we read the second line if we could, but we need maxA first to allocate arrays. So we must read all A into a list first. It's fine: 1.2e6 elements * 28 bytes ~ 34 MB, plus other arrays ~ 8 MB each, total < 60 MB, which is within typical limits (256 MB).

**Optimizations:**
- Use `array('I')` for freq/cnt? Python's array module can store integers compactly, but access is slightly slower. Might not be necessary. Using list of ints is fine.
- For divisor generation, using prime factorization via SPF is efficient. Generate divisors by recursive multiplication.

**Implementation details:**
- SPF sieve: `spf = [0] * (maxA+1)`. For i in range(2, maxA+1): if spf[i]==0: spf[i]=i; for j in range(i*i, maxA+1, i): if spf[j]==0: spf[j]=i. But `i*i` may overflow for i>sqrt(maxA). Standard approach:
  ```python
  spf = list(range(maxA+1))
  spf[0] = 0
  spf[1] = 1
  for i in range(2, int(maxA**0.5)+1):
      if spf[i] == i:  # i is prime
          for j in range(i*i, maxA+1, i):
              if spf[j] == j:
                  spf[j] = i
  ```
  This is O(maxA log log maxA).

- Factorization: given x, while x > 1: p = spf[x]; e = 0; while x % p == 0: x //= p; e += 1; store (p, e). Then generate divisors:
  ```python
  divisors = [1]
  for p, e in factors:
      cur = []
      pow_p = 1
      for _ in range(e):
          pow_p *= p
          for d in divisors:
              cur.append(d * pow_p)
      divisors.extend(cur)
  ```
  This generates all divisors unsorted. We need max divisor satisfying condition. We can just iterate over `divisors` and keep max. Since we need max, we can generate divisors in any order.

- Precompute `cnt` for all v:
  ```python
  freq = [0] * (maxA+1)
  for x in A: freq[x] += 1
  cnt = [0] * (maxA+1)
  for v in range(1, maxA+1):
      s = 0
      for m in range(v, maxA+1, v):
          s += freq[m]
      cnt[v] = s
  ```
  This is double loop. We can micro-opt: for v in range(1, maxA+1): for m in range(v, maxA+1, v): cnt[v] += freq[m]. Same.

  We can also store `cnt` in the same array as `freq` by using a separate array to accumulate. But using two arrays is clearer and faster (no need to save freq for later, we don't need it). So we can just do:
  ```python
  cnt = [0] * (maxA+1)
  for v in range(1, maxA+1):
      for m in range(v, maxA+1, v):
          cnt[v] += freq[m]
  ```
  Wait, `freq` is used inside. So we need `freq` first. That's fine.

- However, the inner loop for each v is O(maxA/v). Sum_{v=1}^{maxA} maxA/v = maxA * H_maxA ≈ maxA * (ln maxA + gamma) ≈ 1e6 * 14 ≈ 14e6. That's small. Actually wait, H_1e6 ≈ ln(1e6)+gamma ≈ 13.8. So 1e6 * 14 = 14 million iterations. That's perfectly fine in Python! Good.

- For each A_i, generate divisors. Number of divisors per number is small. We can precompute divisors for all numbers? That would be too large (sum of divisor counts for all numbers up to 1e6 is ~ N log N, but here we have up to 1.2e6 numbers, but we only need for the actual values, not all numbers. We can precompute divisor lists for each possible value? No, memory would be large: each number up to 1e6 has on average ~100 divisors, times 1e6 = 100 million integers, too much.

- So we generate divisors on the fly using SPF.

**Potential issue:** Generating divisors for each A_i using SPF and loops might still be a bit slow for N=1.2e6, but likely okay in PyPy with tight loops. Let's estimate: average number of divisors for a random number around 1e6 is maybe ~100-150? Actually, the average number of divisors for numbers up to N is about log N. For N=1e6, average ~ log(1e6) ~ 14. So per element ~14 divisor checks, plus factorization (which is O(log x) steps). So total operations ~ 1.2e6 * (log 1e6 + 14) ≈ 1.2e6 * (20) = 24e6. That's very fast.

- But we must be careful with Python overhead: function calls, etc. We'll write the divisor generation inline in the main loop to avoid function call overhead.

**Alternative approach to avoid divisor generation per element:** For each possible d, we know cnt[d]. For each A_i, we want max d | A_i with cnt[d] >= K. We could iterate over all d in decreasing order? No, that would be O(maxA) per i.

- Another approach: Since we have cnt[d], we can for each A_i factor it and check its divisors. That's the standard solution for this problem (known as "Maximum GCD of K elements including i" or similar). It's efficient.

**Edge Cases and Testing:**
- Sample 1: N=5, K=2, A=[3,4,6,7,12]. Expected outputs: 3,4,6,1,6.
- Sample 2: N=3, K=3, A=[6,10,15]. Expected: 1,1,1.
- Sample 3: N=10, K=3, A=... Expected: 59,590,590,879,879,590,20,879,590,59.

**Implementation Plan:**
1. import sys.
2. def solve():
     data = sys.stdin.buffer.read().split()
     it = iter(data)
     N = int(next(it)); K = int(next(it))
     A = [int(next(it)) for _ in range(N)]
     maxA = max(A) if A else 0

## worker: Integrate SPF-based divisor generation into the pe
The solution uses the key insight that the maximum achievable GCD for index `i` is the largest divisor `d` of `A_i` such that at least `K` elements in the whole array are divisible by `d`.  
- A frequency array `freq` is built to count occurrences of each value.  
- An array `cnt` is filled via a harmonic-sum sieve (over all `v`, sum `freq[m]` for multiples `m` of `v`). This runs in `O(maxA log maxA)` which is about 14 million operations for `maxA = 1e6`.  
- A smallest prime factor (SPF) sieve is built to factor each `A_i` quickly into prime powers.  
- For each element, we generate all its divisors from the prime factorization and pick the largest one with `cnt[d] >= K`.  
- The algorithm handles all edge cases (including `K = 1` and `K = N`) correctly. Complexity is well within limits for the given constraints.

## worker: Test the current solution with the provided sample
The solution is complete and self-contained. It implements the standard approach for this problem:
- Count frequency of each value.
- For each possible divisor `v`, count how many array elements are multiples of `v` using a harmonic-sum sieve.
- Use a smallest prime factor (SPF) sieve to quickly factor each `A_i` and generate its divisors.
- For each `A_i`, find the largest divisor `d` such that `cnt[d] >= K`; that is the answer.
- Edge cases (`K=1`, `K=N`, etc.) are handled correctly.
