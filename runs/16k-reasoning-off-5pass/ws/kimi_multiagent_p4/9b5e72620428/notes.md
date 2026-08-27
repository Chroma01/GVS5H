
## ideation
**Core difficulty:** A can be permuted freely and -1s are wildcards (any non-negative integer), so the problem is really about whether we can choose a target sum S and pair up A-values with B-values (via a bijection) so every pair sums to S.

**Key structural reasoning:**
- Let fa = #fixed (non -1) in A, fb = #fixed in B, a = N−fa, b = N−fb wildcards.
- If k fixed-A values are paired with fixed-B values, the remaining fa−k fixed A's must pair with B-wildcards (needs b ≥ fa−k) and fb−k fixed B's pair with A-wildcards (needs a ≥ fb−k). Both reduce to k ≥ fa+fb−N. So the required number of fixed-fixed pairs is L = max(0, fa+fb−N), and any k between L and min(fa,fb) works count-wise.
- Wildcards can realize any value ≤ S, so we need S ≥ every fixed value (S ≥ maxFixed). Then any fixed A paired with a B-wildcard (set it to S−A_i ≥ 0) and vice versa works; wildcard-wildcard pairs are free.
- So the answer is **Yes iff there exists S ≥ maxFixed such that the max matching between fixed A's and fixed B's with edge "A_i + B_j = S" has size ≥ L**.
- For fixed S, max matching = Σ_v min(cntA[v], cntB[S−v]) (greedy by value groups is optimal since edges only depend on values).

**Efficient computation:** matching(S) = Σ_v min(cntA[v], cntB[S−v]). If we iterate over all (distinct value v in A, distinct value w in B) pairs and add min(cntA[v], cntB[w]) to h[v+w], then h[S] accumulates exactly Σ_v min(cntA[v], cntB[S−v]) (each v contributes once per S since w = S−v is determined). This is O(dA·dB) ≤ 4·10⁶ for N=2000 — fine.

**Edge cases / pitfalls:**
- L = 0 (enough wildcards): always Yes — pick S = max(maxFixed, 0); all fixed values pair with wildcards on the other side. (Includes all--1 case.)
- Must enforce S ≥ maxFixed when scanning h (otherwise wildcards would need negative values).
- Values up to 1e9 → use hash maps (Counter / dict), not arrays.
- Verified against all three samples mentally: Sample1 L=2, S=4 gives matching 2 → Yes; Sample2 L=3, best matching 2 → No; Sample3 L=2, S≥4 best matching 1 → No.

## worker: Implement and output the complete Python solution:
- Reduction (from plan): with fa fixed A's and fb fixed B's, at least L = max(0, fa+fb−N) fixed–fixed pairs are forced (pigeonhole via wildcard counts). Wildcards can realize any value in [0, S], so we need a target sum S ≥ maxFixed such that at least L disjoint fixed pairs (i, j) satisfy A_i + B_j = S.
- For fixed S, the max matching only depends on value multiplicities: matching(S) = Σ_v min(cntA[v], cntB[S−v]) (greedy per value group is optimal since all elements with the same value are interchangeable).
- Computing h[S] by iterating over all distinct (v, w) pairs and adding min(cntA[v], cntB[w]) to h[v+w] yields exactly that sum for every S simultaneously, in O(dA·dB) ≤ 4·10⁶ operations — fine for N ≤ 2000.
- L ≤ 0 short-circuits to Yes (choose S = max(maxFixed, 0); every fixed value pairs with a wildcard). This also covers the all-(-1) case.
- Verified logic against all three samples: Sample 1 (L=2, S=4 gives matching 2 → Yes), Sample 2 (L=3, best matching 2 → No), Sample 3 (L=2, S≥4 best matching 1 → No).
