
## ideation
The core problem: for each query range [L,R], find the maximum matching where pairs (top, bottom) satisfy 2*top <= bottom, both in range, each mochi used at most once.

Key facts to verify:
- Array is sorted ascending, so within any range the elements are sorted.
- Classic greedy: two pointers, i at smallest unmatched, j seeking smallest element >= 2*A[i]; match and advance both. This gives maximum matching in O(m). Proof: exchange argument — matching smallest possible top with smallest feasible bottom never hurts.
- Structural property: in the greedy, tops always come from the smaller half and bottoms from the larger half. In fact there's a known result (this is AtCoder ABC/typical "kagamimochi" problem): the answer K satisfies that the K tops are the K smallest elements used and the K bottoms are the K largest... Actually the known optimal: pair the i-th smallest of the lower half candidates. Let me think: the greedy matching on sorted array — an alternative characterization: maximum K such that for all t=1..K, the t-th smallest element x_t among chosen tops satisfies 2*x_t <= the t-th smallest among chosen bottoms. A clean known fact: answer = max K such that a[L+K-1... ] hmm. There's a known simpler characterization: K is achievable iff for the K smallest elements s_1..s_K and K largest elements b_1..b_K (b_t = (m-K+t)-th smallest), 2*s_t <= b_t for all t? Not exactly — greedy doesn't necessarily use the K largest as bottoms. But a valid check: the maximum K equals the largest K such that for all t in 1..K: 2 * (t-th smallest of first m-K elements) <= (t-th smallest of last K elements)? This is getting complicated; safer to think of the standard greedy and find a fast query structure.

Candidate approaches:
1. Offline sweep with BIT/segment tree: Precompute nxt[i] = smallest index j with A[j] >= 2*A[i] (binary search, O(N log N)). Then a pair (i,j) is valid iff j >= nxt[i]. The greedy matching on [L,R]: iterate i from L, maintain pointer j; equivalently, match tops in increasing order, each top i matched to the smallest available bottom position >= max(nxt[i], previous bottom+1). This is like interval scheduling / matching in a convex bipartite graph — greedy by earliest deadlines. To answer many queries offline: sort queries by R, sweep, and we need a data structure that computes the greedy matching count restricted to [L,R]. Known technique: this is equivalent to counting via "for each position as bottom, match it with the smallest unmatched top i with nxt[i] <= position" — greedy from the bottom side: sweep j from L to R, when at j, among unmatched tops i in [L, j) with nxt[i] <= j, match the... which top? To maximize, match the largest such top? Or smallest? Matching the smallest available top keeps larger tops for later bottoms — but later bottoms are bigger, so larger tops also fit; matching smallest top is safe (exchange argument). Hmm, actually for maximizing count, any maximal matching in a convex bipartite graph is maximum? No — need care. The standard result: processing bottoms left to right, match each bottom with the smallest unmatched feasible top gives maximum matching (this is the transpose of the classic greedy). 

2. Persistent segment tree / functional approach: answer for [L,R] might be computed as f(L,R) = number of matches. There's a known solution for this exact problem (typical AtCoder: "Kagamimochi" from JAG or ABC 297? Actually it's from "HHKB2020"? No—it's typical). One known approach: the answer K for range [L,R] satisfies: K = max number such that greedy works; can be computed by noting matches pair i (in left part) with p[i] (in right part), and p is monotone. Could binary search K and check feasibility: K pairs feasible iff we can choose K tops and K bottoms. Feasibility check for given K: the optimal is to take the K smallest as tops? Not exactly, tops and bottoms must be disjoint. Known lemma: K pairs feasible iff for all t in 1..K: 2*A[L+t-1] <= A[R-K+t]. I.e., pair t-th smallest in range with t-th largest among the K largest? Let me sanity check with sample: range (1,2,3,4), m=4, K=2: check t=1: 2*1 <= A[R-1]=3 ✓; t=2: 2*2 <= A[R]=4 ✓. K=2 works. Could K=2 also need disjointness — tops are indices L..L+K-1, bottoms R-K+1..R, disjoint iff 2K <= m. Check sample 5: full array (1,1,2,3,4,4,7,10,11,12,20), m=11, K=5: tops indices 1..5: (1,1,2,3,4), bottoms indices 7..11: (7,10,11,12,20). Check: 2*1<=7, 2*1<=10, 2*2<=11, 2*3<=12, 2*4<=20 ✓. Answer 5 ✓. Check sample 2: (2,3,4,4,7,10), m=6, K=3: tops (2,3,4), bottoms (4,7,10): 2*2<=4, 2*3<=7, 2*4<=10 ✓. Answer 3 ✓. Check query (7,11): (7,10,11,12,20), m=5, K=2: tops (7,10), bottoms (12,20): 2*7=14<=12? No. K=1: tops (7), bottoms (20): 14<=20 ✓. Answer 1 ✓. 

But is the lemma "K feasible iff 2*A[L+t-1] <= A[R-K+t] for all t" actually correct in general? This is a known result for this type of problem: the optimal strategy pairs smallest tops with the K largest bottoms? Hmm, counterexample risk: suppose tops must be disjoint from bottoms; using the K smallest as tops and K largest as bottoms is the best possible configuration: if any matching with K pairs exists, sorting tops ascending s_1..s_K and bottoms ascending b_1..b_K, we need 2*s_t <= b_t for each t (a matching exists in this "nested" setting iff sorted condition holds, by Hall's theorem for threshold graphs). The K smallest possible tops are the K smallest elements of the range, and the K largest possible bottoms are the K largest; if these are disjoint (2K<=m) and satisfy the condition, done. If they overlap (2K > m), we can't take both extremes. Hmm, but when 2K > m, tops and bottoms interleave. Example: (1, 2, 100), m=3, K=1: tops A[L]=1, bottoms A[R]=100, 2<=100 ✓, answer 1 ✓. Example where overlap matters: (1, 3, 4), K=1: 2*1<=4 ✓. Fine since K=1 tops={first}, bottoms={last}, disjoint when m>=2.

Trickier: m=4, K=2 requires disjoint: tops indices L,L+1; bottoms R-1,R — disjoint. In general tops L..L+K-1 and bottoms R-K+1..R are disjoint iff L+K-1 < R-K+1 i.e. 2K <= m. If 2K > m, the extreme choice overlaps, but maybe another choice works. Example: (1, 2, 3), m=3, K=1: fine. Can 2K > m with K>=2? m=5, K=3: need 6 elements, impossible. Actually K pairs need 2K mochi, so 2K <= m always. So disjointness holds automatically. 

But is the condition necessary? If K pairs exist with tops s_t and bottoms b_t (sorted), then s_t >= A[L+t-1] (t-th smallest top is at least t-th smallest element) and b_t <= A[R-K+t] (t-th smallest bottom is at most t-th smallest among K largest). So 2*A[L+t-1] <= 2*s_t <= b_t <= A[R-K+t]. So the condition is necessary. Sufficiency: if 2*A[L+t-1] <= A[R-K+t] for all t, pairing index L+t-1 with R-K+t gives valid disjoint pairs. So the lemma is exactly: answer = max K such that for all t in 1..K, 2*A[L+t-1] <= A[R-K+t]. 

Now, the condition is monotone in K (if K works, K-1 works? Need to check: condition for K-1: 2*A[L+t-1] <= A[R-(K-1)+t] for t<=K-1. Since A[R-K+t+1] >= A[R-K+t], yes, monotone). So we can binary search K per query, but checking takes O(K) — too slow.

We need fast check: define for the query, we need max over t of something. Condition: 2*A[L+t-1] <= A[R-K+t]. Rearranged: for each t, A[R-K+t] >= 2*A[L+t-1]. Let u = L+t-1 (top index), v = R-K+t (bottom index); v - u = R-K+t - L-t+1 = (R-L+1) - K = m - K, constant! So the condition is: for all u in [L, L+K-1], A[u + (m-K)] >= 2*A[u]. Define d = m - K (the "gap" between top and bottom indices). Then K = m - d, and condition: for all u in [L, L + (m-d) - 1] = [L, R-d], 2*A[u] <= A[u+d]. So we want to minimize d (to maximize K=m-d) such that min over u in [L, R-d] of (A[u+d] - 2*A[u]) >= 0... equivalently define g(u,d) = A[u+d] >= 2*A[u]. For fixed d, the set of u where it holds. We want smallest d such that all u in [L, R-d] satisfy it. Note d >= ceil(m/2) since K <= m/2 means d = m-K >= m/2... wait K <= floor(m/2), so d >= ceil(m/2). And as d increases, condition easier (A[u+d] larger). So binary search d in [ceil(m/2), m] (d=m gives K=0, vacuously... range [L, R-m] = [L, L-1] empty, condition holds, K=0). Check condition for given d: need range query: does there exist u in [L, R-d] with A[u+d] < 2*A[u]? Define bad[u] = largest d such that A[u+d] < 2*A[u], i.e., bad threshold: let nxt2[u] = first index with A >= 2*A[u]; then u is "bad for gap d" iff u+d < nxt2[u] (and u+d <= N), i.e., d < nxt2[u]-u. So for query (L,R) and candidate d, we need: for all u in [L, R-d], nxt2[u] - u <= d, i.e., max over u in [L, R-d] of (nxt2[u] - u) <= d. Define h[u] = nxt2[u] - u (if nxt2[u] exists, else 0... if no element is >= 2*A[u], then u can never be a top; h[u] = infinity? If nxt2[u] doesn't exist, then u is bad for all feasible d, meaning condition fails unless range excludes u. h[u] = INF = N+1 say). Then condition: RMQ max of h over [L, R-d] <= d.

So per query: binary search d (or directly compute answer) with a range-max query on h. That's O(log N) RMQ per binary search step, O(log^2 N) per query — with sparse table O(1) RMQ, total O(Q log N). N,Q up to 2e5 — fine.

Even better: answer K = m - d*, where d* = smallest d in [ceil(m/2), m] with maxH(L, R-d) <= d. Note the function maxH(L, R-d) is nonincreasing in d (range shrinks), and d increases; so the predicate is monotone. Binary search works.

Edge cases: define h[u] = nxt2[u]-u where nxt2[u] = smallest index > u... wait, >= 2*A[u], could be u itself? A[u] >= 2*A[u] only if A[u]<=0; sizes >= 1, so nxt2[u] > u always. If no such index, h[u] = INF (large, e.g., N+5). Then maxH <= d fails for any d <= m <= N, so such u must be excluded from [L, R-d] — correct, since u can't be a top.

Also need d >= 1 obviously; d in [ceil(m/2), m]. Check d=m: range [L, R-m] = [L, L-1] empty → maxH = -inf <= d, predicate true. Good, binary search lo=ceil(m/2) might already be true.

Let me re-verify sample 1 query 1: range L=2,R=5, A=(1,2,3,4) (values at indices 2..5: 1,2,3,4). m=4. nxt2: for value 1 (idx2): first >=2 → idx3 (value2), h=1. value2 (idx3): first >=4 → idx5, h=2. value3 (idx4): first >=6 → idx7, h=3. value4 (idx5): first>=8 → idx8, h=3. d range [2,4]. d=2: range u in [2, 5-2=3]: max(h[2],h[3])=max(1,2)=2 <= 2 ✓. So d*=2, K=4-2=2 ✓.

Query 5: L=1,R=11, m=11, d in [6,11]. h values: idx1 (1): first>=2 → idx3, h=2. idx2 (1): h=2 (idx3). idx3 (2): first>=4 → idx5, h=2. idx4 (3): first>=6 → idx7, h=3. idx5 (4): first>=8 → idx8, h=3. idx6 (4): h=2 (idx8). idx7 (7): first>=14 → idx11, h=4. idx8 (10): none ≥20? 20>=20 yes idx11, h=3. idx9 (11): first>=22 none → INF. idx10 (12): INF. idx11: INF. d=6: u in [1, 11-6=5]: max h[1..5]=3 <=6 ✓. K=11-6=5 ✓.

Query 3: L=7,R=11, m=5, d in [3,5]. d=3: u in [7,8]: max(h[7]=4, h[8]=3)=4 >3 ✗. d=4: u in [7,7]: h[7]=4<=4 ✓. K=5-4=1 ✓.

Query 4: L=1,R=2, m=2, d in [1,2]. d=1: u in [1,1]: h[1]=2 >1 ✗. d=2: empty ✓. K=0 ✓.

Great, the approach is validated on samples.

Pitfalls:
- INF handling: h[u] = N+1 (or m can be up to N, d up to m <= N; INF must exceed any d, N+1 works but careful: if h[u]=INF and u in range, predicate false for all d <= m <= N < INF — correct).
- Sparse table for range max, O(N log N) build, O(1) query. Or segment tree O(log N) query → O(Q log^2 N) = 2e5 * ~17*17 ≈ 6e7, borderline in Python. Better: sparse table with O(1) query → O(Q log N) total ≈ 2e5*17 ≈ 3.4e6 operations, fine in Python.
- Binary search per query over d: ~17 iterations, each O(1) RMQ.
- Alternatively compute d* directly: d* = max over... hmm, d* = smallest d >= ceil(m/2) with maxH(L,R-d) <= d. Could also be computed as: consider threshold; but binary search is simple.
- Note: also need d such that K = m-d pairs; also K <= floor(m/2) ensured by d >= ceil(m/2).
- nxt2 via bisect on A: O(N log N).
- 1-indexing care.

Implementation plan:
- Read N, A (1-indexed list with dummy at 0).
- h[i] for i in 1..N: j = bisect_left(A, 2*A[i], lo=i+1) → if j <= N: h[i]=j-i else INF=N+1. (bisect on the list; use 0-indexed array carefully.)
- Build sparse table over h[1..N].
- For each query (L,R): m=R-L+1; lo= (m+1)//2, hi=m (d range); binary search smallest d with queryMax(L, R-d) <= d. Answer = m - d.
- RMQ max via sparse table: k = log2(len); max(st[k][l], st[k][r-2^k+1]).
- Empty range case: when d=m, R-d = L-1 < L → treat max as 0 (skip query). Handle: if L > R-d: predicate true.

Complexity: O((N+Q) log N). 

Let me double check the lemma once more with a potential tricky case: A = (1, 2, 2, 3), query whole, m=4. h: idx1(1): first>=2 → idx2, h=1. idx2(2): first>=4 → none (max is 3) → INF. idx3(2): INF. idx4: INF. d in [2,4]. d=2: u in [1,2]: max(h1=1, h2=INF)=INF >2 ✗. d=3: u in [1,1]: h=1<=3 ✓. K=1. Indeed: pairs possible: (1,2),(1,2),(1,3) — only 1 pair since 2*2=4>3. ✓.

Another: A=(1,1,2,2), m=4. h: idx1: first>=2 → idx3, h=2. idx2: idx3, h=1. idx3: first>=4 none INF. idx4 INF. d in [2,4]. d=2: u in [1,2]: max(2,1)=2<=2 ✓. K=2. Pairs (1,2),(1,2) ✓.

Tricky: A=(1,2,3,4,5,6,7,8), m=8. h: i1: first>=2 idx2 h1. i2: first>=4 idx4 h2. i3: first>=6 idx6 h3. i4: first>=8 idx8 h4. i5..8: INF (first>=10 none). d in [4,8]. d=4: u in [1,4]: max(1,2,3,4)=4<=4 ✓. K=4: pairs (1,5)? wait d=4 pairs u with u+4: (1,5):2<=5 ✓,(2,6):4<=6 ✓,(3,7):6<=7 ✓,(4,8):8<=8 ✓. K=4 ✓.

Case where greedy top-bottom split isn't contiguous halves? The lemma handles it since we proved tops can be taken as K smallest and bottoms as K largest. 

Now confirm the binary search monotonicity: predicate P(d) = (maxH(L, R-d) <= d). As d increases by 1, range [L, R-d] shrinks (max can only decrease or stay), and RHS increases. So P monotone nondecreasing → binary search valid.

Sparse table build in Python for N=2e5: st as list of lists, log table precomputed. Fine.

Alternative simpler: segment tree with iterative max; per query O(log N) → total O(Q log^2 N) ≈ 2e5 * 289 ≈ 5.8e7 — too slow in Python. Sparse table O(1) is better: build O(N log N) = 2e5*18 = 3.6e6, queries O(Q log N) with O(1) RMQ = 3.4e6 RMQ ops. Fine.

Micro-optimization: precompute logs. Use array module or plain lists.

Edge: N up to 2e5, values up to 1e9, 2*A up to 2e9 — Python fine.

Let me also double-check the derivation v - u = m - K = d: tops are indices L..L+K-1 (u = L+t-1), bottoms R-K+1..R (v = R-K+t). v-u = R-K+t-L-t+1 = (R-L+1)-K = m-K. ✓. And u ranges over [L, L+K-1] = [L, R-d] since L+K-1 = L + (m-d) - 1 = L + (R-L+1-d) - 1 = R-d. ✓.

Condition 2*A[u] <= A[u+d] for all u in [L, R-d]. h[u] = nxt2[u]-u is the minimal gap d' such that A[u+d'] >= 2*A[u]; since A sorted, condition holds iff d >= h[u]. So need d >= max h over range. ✓.

Everything consistent. Now also confirm sample 2 quickly for one query: query "1 5": A[1..5] = (127,148,170,174,258), m=5, d in [3,5]. h[1]: first >=254 → idx5 (258), h=4. h[2]: first>=296 → idx6 (311), h=4. h[3]: first>=340 → idx7(414)? A=(127,148,170,174,258,311,331,414,...): first >=340 → idx8 (414), h=5. h[4]: first>=348 → idx8, h=4. h[5]: first>=516 → idx11 (517)? A[9]=416,A[10]=436,A[11]=517 → h=6. d=3: u in [1,2]: max(4,4)=4>3 ✗. d=4: u in [1,1]: h=4<=4 ✓. K=5-4=1 ✓ (sample says 1).

Query "1 17": m=17, d in [9,17]. Expected answer 6 → d*=11. Trust it.

One more consideration: reading input fast — use sys.stdin.buffer.read and split.

Now write the plan for next steps.

## worker: Implement the full Python solution: compute h[i] =
- **Lemma**: For a query range of length m, K pairs are achievable iff for all t in 1..K: `2*A[L+t-1] <= A[R-K+t]`.
  - *Necessity*: In any K-matching, the t-th smallest top ≥ t-th smallest element of the range, and the t-th smallest bottom ≤ t-th smallest among the K largest elements; combining gives the inequality.
  - *Sufficiency*: Pair index `L+t-1` with `R-K+t` directly; disjointness holds because 2K ≤ m (K pairs need 2K mochi).
- **Reformulation**: With gap `d = m - K`, the condition becomes: for all u in `[L, R-d]`, `A[u+d] >= 2*A[u]`. Since A is sorted, for each u the set of valid gaps is `d >= h[u]` where `h[u] = nxt2[u] - u` (nxt2 = first index with value ≥ 2*A[u], found via bisect; INF if none). So the condition is `maxH(L, R-d) <= d`.
- **Monotonicity**: As d grows, the range `[L, R-d]` shrinks (max can only decrease) while the RHS grows, so the predicate is monotone → binary search the smallest feasible d in `[ceil(m/2), m]`; answer `K = m - d`. `d = m` gives an empty range (always feasible, K=0), so the search always terminates.
- Verified against all sample-1 queries by hand (e.g., query (7,11): h[7]=4 forces d=4, K=1; full array: max h over [1,5] = 3 ≤ 6, d=6, K=5) and spot-checked sample 2 (query (1,5) → K=1).
- **Complexity**: O(N log N) preprocessing (bisect + sparse table), O(log N) per query with O(1) RMQ → overall O((N+Q) log N), well within limits for N,Q ≤ 2·10⁵.

## worker: Write a brute-force O(m log m) per-query greedy so
- **Brute force 1 (greedy two-pointer)**: classic O(m) scan on the sorted slice — pair smallest unmatched top `i` with the smallest bottom `j ≥ 2·A[i]`; maximal by exchange argument. This is the ground truth.
- **Brute force 2 (lemma + O(K) check)**: independently implements the lemma `K feasible ⟺ ∀t: 2·A[L+t-1] ≤ A[R-K+t]` with binary search over K and a direct O(K) check. This cross-validates the lemma itself against the greedy, so the fast solution (which relies on the lemma + gap reformulation + sparse-table RMQ) is checked against two independent methods.
- **Random tester**: 3000 random arrays across 4 regimes: (0) duplicate-heavy pools {1..3}, (1) INF-heavy huge sparse values up to 1e9 (most `h[i]` = INF), (2) pair-rich slowly growing sequences, (3) mixed small values. N ≤ 12, up to 15 queries per array including tiny ranges (L+1=R). All three methods must agree on every query.
- Ran the tester locally (seed 999): all 3000 tests passed with zero mismatches across all three implementations.
- The `solve()` entry point is the unchanged fast solution from CURRENT WORK; the self-test runs first and aborts on any mismatch (takes ~2-3 s; can be removed for submission if time-critical, but kept here per the task).

## worker: Finalize with fast I/O (sys.stdin.buffer.read), co
- Finalized the validated approach: for a query range of length m, K pairs are achievable iff `2*A[L+t-1] <= A[R-K+t]` for all t in 1..K (necessity by counting argument on sorted tops/bottoms; sufficiency by pairing `L+t-1` with `R-K+t`, disjoint since 2K ≤ m).
- Reformulated with gap `d = m - K`: feasible iff `maxH(L, R-d) <= d`, where `h[u] = nxt2[u] - u` (first index with value ≥ 2·A[u], via bisect; INF = N+1 if none). Predicate is monotone in d (range shrinks, threshold grows), so binary search d in `[ceil(m/2), m]`; `d = m` gives an empty range (always feasible, K = 0).
- Range max via sparse table: O(N log N) build, O(1) query. Per query: O(log N) binary search with O(1) RMQ → total O((N+Q) log N), fast I/O via `sys.stdin.buffer.read`.
- Removed the embedded random tester/brute force from the submission (they validated the lemma and implementation against two independent brute-force methods on 3000 random cases, including duplicate-heavy, INF-heavy, and pair-rich regimes, plus all sample-1 queries by hand and a sample-2 spot check).
- Edge cases handled: m = 2 (d ∈ {1,2}), INF h-values force exclusion of unpairable tops, empty RMQ range when d = m.
