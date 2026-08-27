
## ideation
Core difficulty: answering 2e5 range queries, each asking for the maximum number of disjoint "2*top <= bottom" pairs — a per-query O(m) greedy is too slow, so we need an O(log N) (or better) per-query characterization.

Key structural facts:
- Array is sorted ascending. For a fixed range [L,R] of length m, the optimal strategy uses the K smallest elements as tops and the K largest as bottoms, paired in sorted order. K is feasible iff for all t in [0,K): 2*A[L+t] <= A[R-K+1+t]. Feasibility is monotone in K → binary search over K in [0, floor(m/2)].
- Naive sufficient check max(2*A[tops]) <= min(A[bottoms]) is WRONG (counterexample: A=[1,50,51,101], K=2 is feasible elementwise but 100 > 51). Must be elementwise.
- Trick to make the elementwise check O(1): precompute g(i) = smallest index with A[g(i)] >= 2*A[i] (via binary search or two pointers; g(i)=N+1 if none). Since A is sorted, A[j] >= 2*A[i] ⟺ j >= g(i). The condition "for all t: R-K+1+t >= g(L+t)" rearranges to:
  max over i in [L, L+K-1] of w[i] <= R - K + 1 - L, where w[i] = g(i) - i.
  The RHS is constant for the query, so this is a plain range-max query on precomputable array w → sparse table (O(1)) or segment tree (O(log N)).
- Verified on the counterexample: w=[1,2,...], max w[1..2]=2 <= 4-2+1-1=2 → feasible. Correct.
- Also sanity-checked against all Sample 1 answers mentally (e.g., [1,1] gives 0; full range gives 5).

Pitfalls:
- 1-indexing consistency (use 1-indexed arrays to match L,R directly).
- g(i) must be computed on the full array (absolute indices); bottoms j = R-K+1+t automatically lie inside [L,R] and are disjoint from tops since K <= m/2 and g(i) > i.
- If 2*A[i] > A[N], set g(i) = N+1 so w[i] is huge and any K needing that top fails.
- Binary search bounds: lo=0, hi=m//2; standard "largest feasible" pattern.
- Sparse table needs O(N log N) memory (~2e5*18 ints, fine); alternatively a segment tree is simpler to get right.

## worker: Implement the full Python solution: fast input par
- Feasibility of K pairs in range [L,R]: pair the K smallest (tops) with the K largest (bottoms) in sorted order; feasible iff for all t in [0,K): 2*A[L+t] <= A[R-K+1+t]. This is monotone in K, so binary search over K in [0, floor(m/2)].
- Elementwise check made O(1): since A is sorted, A[j] >= 2*A[i] iff j >= g(i), where g(i) = first index with A[g(i)] >= 2*A[i] (bisect on the full array; N+1 if none). The condition R-K+1+t >= g(L+t) for all t rearranges to max_{i in [L, L+K-1]} w[i] <= R-K+1-L with w[i] = g(i) - i — a plain range-max query answered by a sparse table.
- Verified the tricky case A=[1,50,51,101], K=2: w[1]=1, w[2]=2, max=2 <= 4-2+1-1=2 → feasible (a naive max-vs-min check would wrongly reject).
- Tops and bottoms are disjoint: g(i) > i always (since 2*A[i] > A[i]), and K <= m/2 keeps the two index windows disjoint.
- Complexity: O(N log N) preprocessing (bisect + sparse table), O(log N) per query. N, Q <= 2e5 → fine.
- 1-indexed arrays throughout to match input L, R directly; sparse table rows stored 0-indexed with careful offset conversion.

## worker: Verify the solution's correctness: re-derive the f
## Verification of the feasibility condition

**Claim:** For range [L,R] with length m, K pairs are achievable iff for all t ∈ [0,K): 2·A[L+t] ≤ A[R−K+1+t].

- *(Achievability ⇒ condition)* Any valid K-pairing uses K tops and K bottoms. The K bottoms must all be ≥ the K-th smallest... more precisely, by a standard exchange argument: sort the chosen tops ascending t₁≤…≤t_K and bottoms ascending b₁≤…≤b_K; a valid pairing exists iff 2·tᵢ ≤ bᵢ for all i (greedy smallest-top-with-smallest-valid-bottom is optimal). The best chance for K pairs uses the K smallest elements of the range as tops and the K largest as bottoms (any other choice can be swapped to these without hurting feasibility). So feasibility ⟺ 2·A[L+t] ≤ A[R−K+1+t] ∀t.
- *(Monotonicity)* If K is feasible, any K' < K is feasible (drop pairs; formally the condition for K' involves a subset of constraints with tops no larger and bottoms no smaller). So binary search is valid.

**O(1) check derivation:** Since A is sorted, A[j] ≥ 2·A[i] ⟺ j ≥ g(i), where g(i) = min{ j : A[j] ≥ 2A[i] } (or N+1). Constraint t: R−K+1+t ≥ g(L+t) ⟺ g(L+t) − (L+t) ≤ R−K+1−L. The RHS is independent of t, so defining w[i] = g(i) − i:

> K feasible ⟺ max{ w[i] : i ∈ [L, L+K−1] } ≤ R − K + 1 − L.

Also note g(i) > i always (2A[i] > A[i] since A[i] ≥ 1), so w[i] ≥ 1, and the top window [L, L+K−1] and bottom window [R−K+1, R] are disjoint because K ≤ m/2. Bottoms stay within [L,R] automatically since R−K+1+t ≤ R.

## Indexing check of the sparse table

- `st[0] = w[1..N]` (length N), so `st[0][i]` corresponds to w[i+1] (0-indexed storage of 1-indexed data).
- `st[k][i]` = max of w over the 2^k elements starting at 1-indexed position i+1, i.e., w[i+1 … i+2^k]. Build: `cur[i] = max(prev[i], prev[i+half])` — correct standard construction; `len(cur) = N − 2^k + 1` ✓.
- `range_max(l, r)`: length = r−l+1, kk = ⌊log2(length)⌋. First block starts at 1-indexed l → storage index l−1 → `row[l-1]` ✓. Second block ends at 1-indexed r → starts at r−2^kk+1 → storage index r−2^kk → `row[r - (1<<kk)]` ✓. Blocks overlap-cover [l, r] since 2·2^kk ≥ length ✓. Bounds: r−2^kk ≤ N−2^kk = len(row)−1 ✓.
- `log2` table: log2[1]=0, log2[i] = log2[i>>1]+1 gives ⌊log2 i⌋ ✓.

## Mental testing

**Sample 1:** A = [1,1,2,3,4,4,7,10,11,12,20] (indices 1..11).
g/w: i=1: 2A=2 → j=3, w=2. i=2: → j=3, w=1. i=3: 2A=4 → j=5, w=2. i=4: 6 → j=7, w=3. i=5: 8 → j=8, w=3. i=6: 8 → j=8, w=2. i=7: 14 → j=11, w=4. i=8: 20 → j=11, w=3. i=9: 22 → none, w=12. i=10: w=12. i=11: w=12.

- Query (2,5): m=4, hi=2. K=2: max w[2..3]=max(1,2)=2 ≤ 5−2+1−2=2 ✓ → answer 2 ✓.
- Query (3,8): m=6, hi=3. K=2: max w[3..4]=3 ≤ 8−2+1−3=4 ✓. K=3: max w[3..5]=3 ≤ 8−3+1−3=3 ✓ → answer 3 ✓.
- Query (7,11): m=5, hi=2. K=2: max w[7..8]=4 ≤ 11−2+1−7=3? No. K=1: w[7]=4 ≤ 11−1+1−7=4 ✓ → answer 1 ✓.
- Query (1,2): m=2, hi=1. K=1: w[1]=2 ≤ 2−1+1−1=1? No → answer 0 ✓.
- Query (1,11): m=11, hi=5. K=5: max w[1..5]=3 ≤ 11−5+1−1=6 ✓ → answer 5 ✓.

All match.

**Sample 2 spot checks:** A = [127,148,170,174,258,311,331,414,416,436,517,523,532,587,591,638,660,748,760,776,837,857,972,984].
- Query (1,5): m=5, hi=2. Values 127,148,170,174,258. K=1: w[1]: 2·127=254 → first ≥254 is index 5 (258), w=4 ≤ 5−1+1−1=4 ✓. K=2: max w[1..2]; w[2]: 296 → index 6 (311), w=4; max=4 ≤ 5−2+1−1=3? No → answer 1 ✓ (expected 1).
- Query (1,17): m=17, hi=8, expected 6. K=6: need max w[1..6] ≤ 17−6+1−1=11. w[1]=4 (idx5), w[2]: 296→idx6, w=4; w[3]: 340→idx7 (414? 2·170=340, first ≥340 is idx7=414? idx6=311<340, yes idx7), w=4; w[4]: 348→idx7, w=3; w[5]: 516→idx11 (517), w=6; w[6]: 622→idx14? 2·311=622, idx13=532,idx14=587? 587<622, idx15=591<622, idx16=638 ≥622 → w=10. max=10 ≤ 11 ✓. K=7: max w[1..7]; w[7]: 662 → idx17? 2·331=662, idx17=660<662, idx18=748 → w=11; max=11 ≤ 17−7+1−1=10? No → answer 6 ✓.
- Query (9,23): expected 2. m=15, hi=7. K=2: max w[9..10] ≤ 23−2+1−9=13. w[9]: 2·416=832 → idx21 (837), w=12; w[10]: 872 → idx23 (972), w=13; max=13 ≤ 13 ✓. K=3: max w[9..11]; w[11]: 2·517=1034 → none, w=25 → fails. Answer 2 ✓.

**Edge cases:**
- *Duplicates* (1,1): g(1) = index of first ≥2; if none, w=N+1, K=1 fails since RHS = R−L ≤ N−1 < N+1 ✓.
- *g(i)=N+1*: w[i]=N+1; any K including top i requires N+1 ≤ R−K+1−L ≤ N−1 (since R≤N, K≥1, L≥1) → infeasible ✓.
- *K=0*: binary search starts lo=0 and never calls range_max with empty range (mid ≥ 1 always when lo<hi) ✓. Also `range_max` is only called with l ≤ r since mid ≥ 1 ✓.
- *m//2 cap*: K ≤ m/2 ensures windows disjoint and bottoms within range ✓.
- *bisect bounds*: `bisect_left(A, 2*A[i], i+1, N+1)` searches A[i+1..N]; correct since g(i) > i. A has sentinel A[N+1]=0 but hi=N+1 excludes it ✓.

**Complexity:** O(N log N) preprocessing, O(log N) per query — well within limits for N, Q ≤ 2·10⁵.

The solution is correct as written; no changes made.
