
## ideation
Core difficulty: N up to 2e5 contests and Q up to 3e5 queries, so per-query simulation O(NQ) is impossible. Need to precompute the final rating function F(X) for all relevant initial X efficiently.

Key structural facts:
- Each contest applies h_i(v) = v + 1 if L_i <= v <= R_i else v. This is monotone non-decreasing, and h_i(v) - v ∈ {0,1}.
- Compositions preserve: F is monotone non-decreasing, F(X+1) - F(X) ∈ {0,1}, and X <= F(X) <= X + N.
- Therefore the array A[x] = current rating for initial x (over x in [1, 5e5], or extended range) always has differences in {0,1}. For contest i, the set {x : L_i <= A[x] <= R_i} is a contiguous index interval [p, q]. Applying the contest = range add +1 on A[p..q], which preserves the 0/1-difference property.

So we need a data structure supporting:
1. Range add +1 on A[p..q].
2. Find p = first index with A[index] >= L_i, q = last index with A[index] <= R_i (order-statistics / binary search over monotone A).

Candidate implementations:
- Fenwick over the difference array D[x] = A[x] - A[x-1] ∈ {0,1}: range add +1 on A[p..q] = point updates D[p] += 1, D[q+1] -= 1. Finding p, q requires searching by value of A, i.e., find index where prefix-sum of D reaches (value - base). Since A[x] = x + (number of increments applied to x) = x + S[x] where S is a range-incremented array, binary search on A needs A values; with a Fenwick on D we can compute A[x] = x + prefix... Actually simpler: maintain B[x] = A[x] - x (total increments received by initial x). B is non-increasing? No — B[x+1] - B[x] = (A[x+1]-A[x]) - 1 ∈ {-1, 0}, so B is non-increasing, starting at 0. Contest i: find p = first x with x + B[x] >= L_i, q = last x with x + B[x] <= R_i; then B[p..q] += 1. Since B non-increasing and we add +1 on a suffix-ish interval... need care: adding +1 to B[p..q] keeps B non-increasing iff B[p-1] >= B[p]+1... not guaranteed. Hmm, actually the invariant is on A's differences; B[p..q]+=1 gives A[p..q]+=1, differences of A stay in {0,1} automatically because A[p-1] < A[p] boundary: A[p-1] <= L_i - 1 < L_i <= A[p], after increment A[p] <= A[p-1] + ... fine, it's provably consistent.

Data structure options for "binary search on monotone A + range add":
- Segment tree with lazy propagation storing min and max of A in each node. Since A is monotone, min = leftmost value, max = rightmost. To find first index with A >= L: descend using max (if node max < L, skip right). To find last index with A <= R: descend using min. Range add with lazy. Each operation O(log V). Total O((N + Q) log V). V = 5e5 (initial X range); but A values can grow up to 5e5 + N = 7e5, which is fine — we only need A defined on initial domain [1, 5e5]. Wait: do we need indices beyond 5e5? Queries have X <= 5e5, so domain [1, 5e5] suffices. But careful: could an initial x <= 5e5 have trajectory affected by contests with ranges above? Yes, but that's captured in values, not domain. Domain stays [1, 5e5].

Edge cases: p might not exist (all A < L_i → no one increments? if max A < L_i, skip; also if min A > R_i skip). Since A is monotone and contest condition is L <= A <= R, the qualifying set is [first index with A >= L, last index with A <= R], and we must check p <= q.

Alternative simpler approach: process contests in reverse computing inverse thresholds — known solution maintains, for each value v, the minimal initial rating that ends at >= v... Another known approach: binary search answer per query with a "count increments" function — hard because increments depend on trajectory.

Another approach: since Q and V are both ~5e5, could simulate all starting values simultaneously forward using the segment tree above — that's the plan.

Pitfalls:
- 1-indexing and boundary conditions (inclusive ranges).
- p > q case (no initial value qualifies, e.g., A jumps over [L, R] — but since A differences are 0/1, A takes every value between min and max, so if min <= R and max >= L then the qualifying interval is nonempty... actually with 0/1 differences A hits every integer in [A[1], A[V]], so p <= q iff A[1] <= R and A[V] >= L).
- Domain: X from 1 to 5e5, but also X=0? Constraints say X >= 1, L_i >= 1. Keep domain [1, 5e5]; maybe pad index 0 for safety.
- Segment tree size ~5e5, N operations each O(log) — fine in Python with iterative seg tree or recursive with sys.setrecursionlimit; iterative bottom-up with lazy is trickier; a recursive or iterative top-down lazy seg tree in Python should handle 2e5 * ~2 * log(5e5) ≈ 8e6 node visits — might be tight but okay with arrays and iterative loops. Alternative: Fenwick-based order statistics on D with binary lifting: find first index where A >= L means find where prefix sum of D crosses L - 0... A[x] = x + inc[x] where inc from range adds; combining x + Fenwick prefix isn't directly searchable by Fenwick binary lifting. Segment tree with min/max lazy is the clean choice.

Complexity: O((N + Q) log V) time, O(V) memory.

## worker: Implement the full solution in Python: a lazy segm
- Maintains array A[x] = current rating for initial rating x over domain [1, 5e5], initialized A[x]=x.
- Key invariant: A is monotone non-decreasing with consecutive differences in {0,1}, so for contest i the set {x : L_i <= A[x] <= R_i} is a contiguous index interval [p, q]; applying the contest is a range +1 on A[p..q], which preserves the invariant.
- Lazy segment tree stores min/max per node (for a monotone array, node min = leftmost leaf, max = rightmost leaf). 
  - p = first index with A >= L_i: descend, skipping nodes whose max < L_i.
  - q = last index with A <= R_i: descend, skipping nodes whose min > R_i.
  - Range add +1 with standard lazy propagation.
- Padding leaves (indices 0 and > 5e5) get sentinel min=+inf, max=-inf so searches never select them; p, q are clamped to [1, V] and skipped if empty.
- Each contest costs O(log V); total O((N + Q) log V) ≈ 2e5 * 19 node visits per operation — fine.
- Verified logic against Sample 1 mentally: trajectories match (3→6, 2→6, 5→8).

## worker: Verify correctness against the provided samples by
**Verification against Sample 1 (hand-trace):**

Contests: (1,5),(1,3),(3,6),(2,4),(4,7). Initial A[x]=x for x∈[1,5e5].

- Contest 1 (L=1,R=5): p = first index with A≥1 → 1; q = last with A≤5 → 5. Add +1 to A[1..5]: A = [2,3,4,5,6,7,8,...] (indices 1..8).
- Contest 2 (L=1,R=3): p = first with A≥1 → 1; q = last with A≤3 → 2 (A[2]=3, A[3]=4). Add to A[1..2]: A=[3,4,4,5,6,7,...].
- Contest 3 (L=3,R=6): p = first with A≥3 → 1; q = last with A≤6 → 5 (A[5]=6). Add to A[1..5]: A=[4,5,5,6,7,7,...].
- Contest 4 (L=2,R=4): p = first with A≥2 → 1; q = last with A≤4 → 1 (A[1]=4, A[2]=5). Add to A[1..1]: A=[5,5,5,6,7,7,...].
- Contest 5 (L=4,R=7): p = first with A≥4 → 1; q = last with A≤7 → 6 (A[6]=7, A[7]=8). Add to A[1..6]: A=[6,6,6,7,8,8,8,...].

Queries: A[3]=6 ✓, A[2]=6 ✓, A[5]=8 ✓. Matches expected output 6/6/8.

**Sample 2 spot-check:** X=500000: only contest 7 (2000..500000) matches initially at 500000 → +1 = 500001; later contest 10 is 1600..2799, no. Expected 500001 ✓ (A[500000] starts at 500000, gets exactly one increment). X=1: contests 1,2,4,5,6,8,9 (all 1..1999) = 7 increments → 8 ✓. X=2000: contests 3 (1200..2399, at 2000→2001), 7 (2000..500000, at 2001→2002), 10? 1600..2799 at 2002→2003 → total 2003 ✓.

**Edge cases checked:**
- **X=1, X=5e5:** both inside domain [1, V]; padding leaves (index 0 and >V) have mn=+inf/mx=-inf so searches never return them; q is clamped to V and p>V is skipped.
- **L_i = R_i:** degenerate interval works fine — p = first index with A≥L, q = last with A≤L; since A has 0/1 differences it hits value L on a contiguous run, p≤q.
- **Values exceeding 5e5:** A values can grow to 5e5+N=7e5; mn/mx store values (unbounded ints), only the *domain* is capped — correct.
- **p>q:** with 0/1 differences A hits every integer in [A[1], A[V]], so if A[1]≤R and A[V]≥L the interval is nonempty; the `if p <= q` guard handles any residual case safely (e.g., q=-1 when all A>R).
- **Invariant preservation:** adding +1 on exactly {x : L≤A[x]≤R} keeps differences in {0,1}: at left boundary A[p-1]<L≤A[p] so gap can only shrink from 1 to 0 or stay; at right boundary A[q]≤R<A[q+1] similarly. Monotone search validity is maintained inductively.
- **Sentinel + lazy:** padding leaves get +inf/-inf; range_add never touches them (q≤V, p≥1), and pushes only propagate values within updated ranges, so sentinels stay intact. find_first_ge on padding: mx=-inf < val → skipped; find_last_le: mn=+inf > val → skipped. ✓
- **Complexity:** each contest does two O(log V) searches and one O(log V) range add; queries O(log V) each. Total ≈ (3N+Q)·log(5e5) ≈ 1.7e7 recursive calls worst case — acceptable in Python with sys.stdin.buffer and array-based tree.
