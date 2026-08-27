
## ideation
The core insight: for index i, the answer is the largest d dividing A_i such that at least K elements of A are divisible by d (pick A_i plus any K-1 other multiples of d). So the problem reduces to:
1. Compute cnt[d] = number of elements divisible by d, for all d up to M = max(A) ≤ 1e6. Do this with a frequency array freq[x], then for each d from 1..M, sum freq over multiples of d — O(M log M) ≈ 14M operations, fine.
2. Precompute best[x] = max divisor d of x with cnt[d] ≥ K. Fill by iterating d ascending over all "valid" d (cnt[d] ≥ K) and writing best[m] = d for every multiple m of d; since d increases, the last write is the largest valid divisor. Also O(M log M).
3. Answer for each i is best[A_i].

Pitfalls:
- N up to 1.2e6 — need fast I/O (sys.stdin.buffer.read) and avoid per-element Python overhead where possible; the sieve loops in pure Python (~2 × 14M iterations) should be OK but tight-ish; can restrict the d-loop to values where freq or multiples matter. Actually the harmonic sum M/d over d=1..M ≈ M ln M ≈ 14M for M=1e6, each inner step a simple array add/assign — acceptable in CPython if written tightly (local variable binding, range loops). Roughly 2-4 seconds; may need minor optimization (e.g., skip d with no multiples? can't know cheaply — but we can skip d where cnt[d] < K in the second pass, which helps when few valid d; worst case K=1 all valid).
- K=1 edge: answer is A_i itself; the sieve handles it since A_i divides itself and cnt[A_i] ≥ 1.
- Memory: arrays of size M+1 ints; use array('i') or list of ints — list of 1e6+1 ints is ~28MB each in CPython for arbitrary ints but small ints cached... values up to 1.2e6 not cached; better use array('i') or just lists (two lists ~ 70MB might be risky). Use array('i') or numpy if allowed; safest pure-Python: list is fine typically (AtCoder-style limits ~256MB; two lists of 1e6 ints ≈ 2 × 36MB = 72MB, plus freq — three arrays ~108MB, borderline). Can drop freq after computing cnt (reuse), and best can reuse... Actually need freq to build cnt; then freq can be freed. cnt and best needed. Consider array('i') to be safe (4MB each).
- Output N lines — build with '\n'.join on list of strings.

## worker: Write the complete Python solution: fast input par
- Reduction: for index i, answer = max d | A_i with cnt[d] ≥ K, since we can pick A_i plus any K−1 other multiples of d. Correctness: any chosen set of size K containing A_i has gcd g dividing A_i, and all K elements are divisible by g, so cnt[g] ≥ K; conversely any valid d yields a feasible set with gcd ≥ d (gcd of chosen multiples of d is a multiple of d... actually gcd could be a multiple of d, which is even better — so max valid d is achievable as gcd exactly? If gcd of the chosen set is d' > d, then d' also divides A_i and cnt[d'] ≥ K, so the optimum is itself a valid d. Hence answer = max valid divisor.)
- Sieve passes are O(M log M) ≈ 14M inner steps each for M = 1e6; two passes with tight local bindings. Used `array('i')` to keep memory ~4MB per array instead of ~36MB per list.
- K=1 works naturally: A_i divides itself and cnt[A_i] ≥ 1, so best[A_i] = A_i.
