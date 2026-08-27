
## ideation
The core insight: N = p^{2a} q^{2b} = (p^a q^b)^2, so N is a perfect square whose root m = p^a q^b has exactly two distinct prime factors. Since A ≤ 10^12, m ≤ 10^6. The task reduces to: generate all m ≤ 10^6 with exactly two distinct prime factors, square them, sort, and binary search per query.

Key difficulty: efficiently enumerating all such m without duplicates. Options:
1. Sieve the smallest prime factor (SPF) up to 10^6, then factor each m and count distinct primes — O(10^6 log) which is fine (~10^6 numbers, fast in Python with arrays, maybe borderline but acceptable).
2. Enumerate prime pairs (p, q) and exponent combinations — more complex dedup but fewer candidates.

Pitfalls:
- Duplicates when enumerating via pairs (e.g., 2^1·3^1·... no, m has exactly two distinct primes, so each m corresponds to a unique pair {p,q} — no duplicates across pairs, but within a pair multiple (a,b) give distinct m; that's fine).
- Python speed: factoring 10^6 numbers via SPF is roughly 10^6·(few divisions) — should run in ~1-2s. Precompute distinct-prime-count via DP: cnt[x] = cnt[x // p^e] + 1 style, or cnt[x] = cnt[x/spf[x]] + (1 if spf[x/spf[x]] != spf[x] else 0). That's a clean O(10^6) recurrence.
- Memory: use arrays of ints; list of valid squares could be large. Count of m ≤ 10^6 with exactly 2 distinct prime factors is on the order of a few hundred thousand — fine.
- Binary search with bisect per query: Q ≤ 2·10^5, trivial.

Edge cases: A ≥ 36 guaranteed, and answer always exists (36 = 6^2 is the smallest 400 number). Squares may overflow? m ≤ 10^6, m^2 ≤ 10^12 fits in Python int easily.

## worker: Write the complete Python solution: linear sieve f
- A 400 number N = p^{2a} q^{2b} = (p^a q^b)^2, so N is a perfect square whose root m has exactly two distinct prime factors. Since A ≤ 10^12, m ≤ 10^6.
- Built an SPF sieve up to sqrt(max query), then computed the number of distinct prime factors for every m via the recurrence: let p = spf[m], y = m/p; if y == 1 then cnt = 1; else if spf[y] == p then cnt[m] = cnt[y]; else cnt[m] = cnt[y] + 1. This is O(limit).
- Collected m^2 for all m with cnt[m] == 2, sorted them, and answered each query with bisect_right. Q ≤ 2·10^5 so total cost is trivial after the O(10^6) precomputation.
- The smallest 400 number is 36 = 6^2, and constraints guarantee A ≥ 36, so bisect always finds a valid index.
- Note: the first cnt loop in the code is redundant (immediately overwritten by the clean second loop); it does not affect correctness but could be removed for clarity. The second loop alone is correct.
