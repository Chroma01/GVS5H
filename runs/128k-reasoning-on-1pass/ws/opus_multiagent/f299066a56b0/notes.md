
## ideation
**Problem restated.** Sorted array `A[0..N-1]`. Pair up disjoint elements (top, bottom) with `2*top <= bottom`. Maximize number of pairs K.

**Core difficulty / key insight.**
- Structural claim: for a fixed K, if K pairs are possible at all, then the specific assignment "the K smallest elements as tops, the K largest as bottoms, matched in order (`A[i]` ↔ `A[N-K+i]`, i=0..K-1)" also works. This is a standard exchange argument: any feasible set of K tops can be replaced element-wise by the K smallest (each is ≤ the original), any feasible set of K bottoms by the K largest, and within fixed sets, sorted-order matching is optimal (Hall's condition / rearrangement).
  - Careful: need tops and bottoms disjoint. With K ≤ N/2 the smallest K and largest K indices don't overlap. Also `2*A[i] <= A[j]` with A ≥ 1 forces `A[i] < A[j]`, so index ordering is fine.
- Feasibility is monotone in K (drop the largest top and smallest bottom from a feasible K-matching ⇒ feasible (K−1)-matching — must verify the residual still matches in order; it does since removing the last pair of the order-matched configuration keeps `2*A[i] <= A[N-K+i] <= A[N-(K-1)+i]`). So binary search on K ∈ [0, N//2] is valid.

**Candidate approaches.**
1. **Binary search + O(N) check** (plan given): check `all(2*A[i] <= A[N-K+i] for i in 0..K-1)`. O(N log N). Safe, easy to argue.
2. **Two-pointer greedy O(N)**: `i=0; cnt=0; for j in range(N): if 2*A[i] <= A[j]: cnt+=1; i+=1`. Classic greedy, matches each candidate bottom with the smallest unused top. Gives the same answer; O(N) but pure-Python loop over 5·10⁵ is fine (~0.2 s) though slower than numpy.
   - Note: need `i < j` guaranteed (true as argued) and stop when `i` reaches j / N.
3. **Numpy vectorized binary search**: keep A as `np.int64` array; check is `np.all(2*A[:K] <= A[N-K:])`. ~20 iterations of vectorized comparisons ⇒ very fast. Best for Python performance.
4. **Direct counting via searchsorted (no binary search)**: for each i, `p[i] = searchsorted(A, 2*A[i], 'left')` = first index that can host `A[i]` as a bottom... then K = max k s.t. `p[i] <= N-k+i` for all i<k, i.e. `k <= min_{i<k}(N + i - p[i])`. Can compute prefix-min of `N + i - p[i]` and find largest k with `k <= prefixmin(k-1)`. O(N log N) fully vectorized, or combine with monotonicity for a scan. Slightly more intricate but elegant.

**Pitfalls.**
- Overflow: none in Python; if using numpy, use int64 (A up to 1e9, 2*A up to 2e9 > int32 range) — must cast explicitly since `np.fromstring/np.array` may pick int64 by default but be explicit.
- Off-by-one in the check indices: pairs are `(A[i], A[N-K+i])` for i in 0..K-1.
- K=0 must be printable (sample 2).
- Input parsing speed: use `sys.stdin.buffer.read().split()` or `np.frombuffer`/`np.array(data[1:], dtype=np.int64)`.
- Strict vs non-strict: condition is `a <= b/2` i.e. `2a <= b` (integers, so no rounding issues). Equal sizes never pair (2a ≤ a impossible for a ≥ 1).
- Don't try to be clever with pairing adjacent halves without proof; also don't assume answer is always achieved by splitting at N//2 (sample 3: N=24, answer 6 < 12).

**Sanity checks (mental, not by running).** Sample 1: N=6, A=[2,3,4,4,7,10]; K=3 ⇒ check 2·2≤4 (A[3]), 2·3≤7, 2·4≤10 ✓. K=4 would need index range overlap (N//2=3), so max is 3 ✓. Sample 2: 2·387 > 389 ⇒ 0 ✓.

## worker: Write the complete Python solution: read input wit
- Parsed input via `sys.stdin.buffer.read().split()`; array is already sorted per constraints.
- Feasibility of K: use the K smallest as tops and K largest as bottoms, matched in order, i.e. `2*A[i] <= A[N-K+i]` for all `i < K`. This is optimal by the standard exchange argument (replace tops by the K smallest, bottoms by the K largest, sorted matching is optimal within fixed sets). Disjointness holds since `K <= N//2`.
- Feasibility is monotone in K (removing the last pair from the order-matched configuration keeps `2*A[i] <= A[N-K+i] <= A[N-K+1+i]`), so binary search over `[0, N//2]` is valid; each check is a vectorized numpy comparison → ~20 passes of O(N), very fast for N = 5·10⁵.
- int64 used explicitly so that `2*A` (up to 2·10⁹) doesn't overflow int32.
- Fallback (if numpy missing) is the equivalent O(N) two-pointer greedy: scan bottoms left to right and consume the smallest unused top whenever `2*A[i] <= A[j]`; the `i < j` guard maintains disjointness (and is never binding since `2a <= b` with `a>=1` forces `a < b`).
- Sanity: sample 1 → K=3 (2·2≤4, 2·3≤7, 2·4≤10); sample 2 → 0; K=0 prints correctly.

## worker: Harden the code against the fragile numpy path: `n
**Fixed a real correctness bug in the previous fallback.** The old pure-Python greedy (`i=0; for j in range(n): if i<j and 2*A[i]<=A[j]: ...`) allows an element to serve both as a bottom and later as a top. Counterexample: `A=[1,2,4]` → it pairs (1,2) and (2,4), reporting 2, but only 3 mochi exist so the answer is 1. So the disjointness must be enforced structurally, not with `i<j`.

**Correct formulation.** For a feasible K we always have `K <= n//2 = h`, and the canonical optimal configuration is tops = K smallest (indices `0..K-1 ⊆ [0,h)`) and bottoms = K largest (indices `n-K..n-1 ⊆ [n-h,n)`), matched in order (`2*A[i] <= A[n-K+i]`). Hence nothing is lost by restricting tops to the first `h` elements and bottoms to the last `h` elements — these two index ranges are disjoint (for odd `n` the middle element is simply unused, which is fine because it can never be needed). On two disjoint sorted lists, the classic greedy "scan bottoms in increasing order, consume the smallest unused top whenever `2*top <= bottom`" produces a maximum matching (standard exchange argument: matching the smallest available top to the smallest usable bottom is never worse).

**Numpy path removed.** `np.array(list_of_bytes, dtype=np.int64)` can raise `ValueError`/`TypeError` on some numpy versions, which `except ImportError` would not catch, crashing the program. The pure-Python path is now the only path, so there is no fragile branch left.

**Complexity / timing.** O(N) total: one `map(int, ...)` over ≤5·10⁵ tokens (~0.1–0.15 s) plus a loop of at most `h = 250000` iterations (~0.05–0.1 s). Well inside typical limits, and memory is one list of 5·10⁵ ints.

**Desk checks.**
- Sample 1: `n=6,h=3`, tops `[2,3,4]`, bottoms `[4,7,10]`: 4≤4 ✓, 6≤7 ✓, 8≤10 ✓ → **3** ✓
- Sample 2: `n=3,h=1`, top `387`, bottom `389`: 774>389 → **0** ✓
- Sample 3: `n=24,h=12`; bottoms 541,571,575,602 fail vs 614; 614≥614 ✓(307), 660≥642 ✓(321), 669≥660 ✓(330), 678≥678 ✓(339), 712≥698 ✓(349), 723<784 ✗, 785≥784 ✓(392), 792<844 ✗ → **6** ✓
- `n=2, [1,2]`: h=1, 2≤2 → **1** ✓; `n=2, [1,1]`: 2>1 → **0** ✓
- `n=3, [1,2,4]`: h=1, top `1`, bottom `4`: 2≤4 → **1** ✓ (old code wrongly gave 2)
