
## ideation
The core difficulty is that N can be up to 2×10^5 and values up to 2^60, so we cannot enumerate all subsets. However, the guarantee C(N,K) ≤ 10^6 means the number of K-subsets is small enough to enumerate directly (10^6 combinations, each XOR computed in O(1) incrementally or O(K) — O(K) per combination could be up to 10^6 × K which might be too slow if K is large; but note if K is large, then C(N,K) ≤ 10^6 forces N-K small, so we should enumerate the complement side).

Key insight: XOR of K chosen elements = (XOR of all N elements) ⊕ (XOR of the N-K unchosen elements). So if K > N/2, enumerate subsets of size N-K (the complement), compute their XOR, and combine with total XOR. C(N,K) = C(N,N-K), so enumerating min(K, N-K) sized subsets keeps the count ≤ 10^6.

Efficiency concerns:
- Using itertools.combinations in Python over 10^6 subsets with O(1) work each is feasible (~1-2 seconds). Computing XOR incrementally: we can compute XOR of each combination by XOR-ing its elements — that's O(K) per combination in the worst case. But when we enumerate the smaller side, min(K, N-K) could still be large only when C(N, K) is small. Actually if min(K, N-K) = m, then C(N, m) ≤ 10^6 and the total work is C(N,m) × m. For m ≤ 3 this is fine. For larger m, C(N,m) ≤ 10^6 with N ≤ 2×10^5 forces m ≤ ~4-5 (since C(2×10^5, 4) ≈ 6.7×10^19... wait, C(N,4) for N=2×10^5 is about 6.6×10^19, way over 10^6). Let me reconsider: C(N, m) ≤ 10^6 with N large means m is tiny: m=1 → N ≤ 10^6 (always true); m=2 → N(N-1)/2 ≤ 10^6 → N ≤ ~1414; m=3 → N ≤ ~181; m=4 → N ≤ ~55. So when m is small, N is also bounded, and total work C(N,m)×m is at most ~10^6 × small m. Worst case m=2, N=1414: 10^6 combos × 2 ops = 2×10^6 ops. Fine.
- Edge cases: K=0 not possible (K≥1). K=N: answer is XOR of all. m=0 case: answer is total XOR if K=N... wait if K=N, complement size 0, XOR of empty set = 0, answer = total XOR. Handle m=0.

Alternative smarter approaches (not needed but worth noting): Gaussian elimination / linear basis over GF(2) for maximizing XOR works for the "any subset" case, but the fixed-cardinality constraint makes it harder (would need basis with cardinality tracking, or meet-in-the-middle). Given C(N,K) ≤ 10^6, brute force is simplest and safe.

Pitfalls:
- Recursion depth if implementing combinations manually — use itertools.combinations.
- Time limit: pure Python loop over 10^6 combinations with inner XOR loop should be OK, but we can micro-optimize: for m=1, just take max; for m=2, double loop with local variable references. Actually itertools.combinations with a sum-xor via functools.reduce or a manual loop is fine.
- Reading input fast: sys.stdin.buffer.read().
- A_i < 2^60 fits in Python int natively.

Let me double check worst-case timing: m=2, N≈1414, C≈10^6. Loop: for combo in combinations(range(N), 2): x = A[c0]^A[c1]. That's 10^6 iterations — fine in Python (~0.5s).

m=3, N≈181: C(181,3)≈ 9.7×10^5, each with 3 XORs → ~3×10^6 ops. Fine.

So plan: read input, compute total XOR, m = min(K, N-K), enumerate combinations of indices of size m, compute XOR of chosen elements (if m==K, candidate = xor of combo; else candidate = total ^ xor of combo), track max. Print max.

## worker: Implement and output the complete Python solution:
- Key identity: XOR of a chosen K-subset = (XOR of all N elements) ⊕ (XOR of the complementary (N−K)-subset). So we enumerate whichever side is smaller: m = min(K, N−K). Since C(N,K) = C(N,N−K) ≤ 10^6, the enumeration count is bounded by 10^6.
- Work per combination is O(m). The constraint C(N,m) ≤ 10^6 with N ≤ 2×10^5 forces m to be tiny whenever N is large (m=2 ⇒ N ≲ 1414, m=3 ⇒ N ≲ 182, etc.), so total operations stay within a few ×10^6 — fast enough in pure Python.
- Edge cases handled: K = N (m = 0, answer = total XOR), K = 1 (answer = max element), K = N−1 (enumerate single complements).
- Micro-optimizations: special-cased m = 0 and m = 1 to avoid combination overhead; used local accumulation loops instead of functools.reduce.
