
## ideation
**Restating / core structure.**
`A` is globally sorted, so any contiguous query range `[L,R]` is itself a sorted array. For a sorted multiset the classic exchange argument gives: a matching of size `K` exists iff matching the `K` *smallest* elements, in order, against the `K` *largest* elements, in order, works. I.e. with 0‑indexed `l=L-1`, `r=R-1`, `m=r-l+1`:

> `K` is feasible ⟺ `2*A[l+t] <= A[r-K+1+t]` for all `t = 0..K-1`.

Feasibility is monotone (if `K` works, `K-1` works, since the constraint set shrinks and the right-hand indices all shift right), so binary search on `K ∈ [0, m//2]` is valid.

**Key reduction (makes each feasibility test O(1)).**
Let `f[i] = min{ j : A[j] >= 2*A[i] }` (`= N` if none), and `g[i] = f[i] - i`. Since `A_i >= 1`, `2*A[i] > A[i]` so `f[i] > i` and `g[i] >= 1`.
`2*A[l+t] <= A[r-K+1+t]` ⟺ `r-K+1+t >= f[l+t]` ⟺ `g[l+t] <= (r-l+1) - K = m-K`.
So: **`K` feasible ⟺ `max(g[l .. l+K-1]) + K <= m`** (empty max for `K=0`).
Since `P(K) = max(g[l..l+K-1])` is nondecreasing, `P(K)+K` is strictly increasing → clean binary search / or a segment-tree descent.

**Main difficulty is not the algorithm but Python speed:** `N,Q <= 2e5`, and a per-query Python loop with ~17 iterations of range-max is ~3.4M interpreted steps plus sparse-table lookups — probably too slow in CPython unless vectorized. So the real task is a NumPy-vectorized parallel binary search over all queries at once (≈17 rounds, each round a handful of whole-array NumPy ops → well under a second).

**Pitfalls to watch.**
1. `f` via `np.searchsorted(A, 2*A, side='left')` — must be `'left'` (first `j` with `A[j] >= 2A[i]`), not `'right'`. Use int64 for `2*A` (values up to 2e9 exceed int32).
2. `g[i]` can be up to `N - i` (when `f=N`), which correctly makes those positions infeasible; no need for a sentinel `INF`, but check the arithmetic `g <= m-K` still rejects properly (it does, since `g = N-i > m-K` whenever no valid partner exists... verify carefully: if `f[i]=N` then `g[i]=N-i` and `m-K <= m <= N-l <= N-i`? need `N-i > m-K`; since `i >= l`, `m-K < m = r-l+1 <= N-l <= N-i` when `i>=l` — holds strictly as long as `K>=1`. OK, but re-derive rather than trust.)
3. During vectorized binary search, candidate `K` may exceed `m//2` or push `l+K-1` past `N-1`; **must clip indices** before fancy-indexing the sparse table, then invalidate with a mask (`cand <= m//2`).
4. `K=0` must never trigger a range-max query (log of length 0). Structure the doubling search as `ans=0; for b in 17..0: cand=ans+2^b; ...` so `cand >= 1` always.
5. Sparse table log lookup: precompute `LOG` array up to `N+1`, index by `cand` (length of range), use `max(st[k][a], st[k][a+cand-2^k])`.
6. Fast IO: read all of `sys.stdin.buffer` and parse with `np.frombuffer`/`np.array(buf.split(), dtype=...)`; output via `'\n'.join(map(str, ans.tolist()))` (avoid `savetxt`, it's slow).
7. Note `1 <= L < R`, so `m >= 2`; answer 0 is possible and common.
8. Duplicates (`A_i = A_{i+1}`) are fine — the `2a <= b` condition handles equality of sizes naturally (`1,1` gives 0).

**Sanity checks done mentally on sample 1:** query `(1,11)`: `g[0..4] = 2,1,2,3,3`, `K=5` needs `max<=6` ✓, capped by `m//2=5` → 5 ✓. Query `(7,11)`: `g[6]=4`, `K=1` needs `<=4` ✓; `K=2` needs `max(g[6],g[7])=4 <= 3` ✗ → 1 ✓.

**Alternative approaches (fallbacks).**
- Segment-tree descent on `g` from position `l` finding the largest prefix with `max(g)+K <= m`: O(log N) per query but hard to vectorize; only if binary search proves wrong.
- Offline monotonicity tricks (answer changes by ≤1 when `R`→`R+1`) — more complex, no benefit.
- If NumPy vectorization is still too slow, consider PyPy-style micro-optimizations or a flat 1-D sparse table (`st[k*N + i]`) to avoid list-of-arrays indexing overhead.

## worker: Write the complete Python solution in one file: pa
- **Correctness of greedy/binary search:** array is globally sorted, so a query range is sorted. A matching of size `K` exists iff the `K` smallest elements of the range pair in order with the `K` largest: `2*A[l+t] <= A[r-K+1+t]` for `t=0..K-1`. Feasibility is monotone in `K`.
- **O(1) test:** with `f[i]=min{j: A[j] >= 2A[i]}` (searchsorted `'left'`, computed on int64 so `2*A` up to 2e9 is fine) and `g[i]=f[i]-i`, the condition becomes `max(g[l..l+K-1]) <= m-K`. Since `A_i>=1`, `g[i]>=1`. If `f[i]=N` then `g[i]=N-i >= N-r >= ...`; concretely `m-K < m = r-l+1` and `N-i >= N-r`; the check still correctly rejects because for a position `i` in `[l, l+K-1]` we need `i+g[i] <= r+1-K <= N`, impossible when `g[i]=N-i` unless `K=0`. So no sentinel needed.
- **Index safety:** `mid <= hi = m//2` always, hence `l+mid-1 <= r <= N-1`; sparse-table indices `a=l` and `b=l+len-2^k` are in `[0,N-1]` (extra `np.clip` kept as a cheap guard).
- **Vectorization:** parallel binary search over all queries; ≤20 rounds, each a constant number of NumPy ops (2 fancy-index gathers into a flat `(LEV,N)` int32 table). No per-query Python loop; only `O(log N)` Python-level loops for table construction.
- **`mid==0`** is treated as feasible explicitly and `length = max(mid,1)` prevents zero-length range queries.
- Verified by hand on sample 1: `(7,11)` → `g[6]=4`, `K=1` needs `<=4` ✓, `K=2` needs `max(g[6],g[7])=4 <= 3` ✗ → 1; `(1,11)` → `max(g[0..4])=3 <= 6` with `K=5=m//2` → 5.

## worker: Harden the final code without changing the algorit
- **(a) Robust parsing.** `parse_ints` tries the fast bulk `np.array(tokens, dtype=np.int64)` conversion (works on the NumPy versions where bytes→int casting is supported) and validates dtype/size; on *any* exception (or mismatch) it falls back to `np.fromiter(map(int, tokens), dtype=np.int64, count=len(tokens))`, which is version-independent and parses ~6·10⁵ tokens in roughly 0.05–0.10 s. Empty input returns immediately.
- **(b) Dead code / clips removed.** Deleted `np.clip(a, 0, N-1, out=a) if False else None` and both `np.clip` calls. Justification (also written as a comment in the code): `a = l = L-1 >= 0`; with `length = max(mid,1)` and `p = 2^⌊log2 length⌋ ≤ length`, we get `b = l + length - p ∈ [l, l+length-1]`, and `l + length - 1 ≤ N-1` because either `mid = 0` (length 1, index `l ≤ r ≤ N-1`) or `mid ≤ hi = m//2` so `l + mid - 1 ≤ l + m - 1 = r ≤ N-1`. Hence all four sparse-table indices lie in `[0, N-1]` and both `ST[k][a]`, `ST[k][b]` cover exactly `[a, a+p-1] ∪ [b, b+p-1] = [l, l+length-1]` with only *valid* (non-padded) table entries, since padding at level `k` starts at index `N-2^{k-1}` and any queried index `i` satisfies `i + 2^k - 1 ≤ N-1`.
- **(c) Degenerate guards.** Explicit early return when the token stream is empty or `Q <= 0`; if the `L/R` block is truncated, `Q` is reduced to the number of complete pairs (and returns if none). `L`/`R` are `.copy()`d so they are contiguous own-data arrays (safe for the arithmetic and fancy indexing). Binary-search updates now use an `active = lo < hi` mask, so already-finalized queries can never have `hi` pushed below `lo` by a spurious round — a strict hardening of the previous version (the invariant held before by monotonicity, but is now explicit).
- Algorithm unchanged: sparse-table range max on `g[i] = f[i] - i` plus a NumPy-vectorized parallel binary search (≤20 rounds, each O(Q) vector ops). Complexity `O((N+Q) log N)` time, `O(N log N)` int32 memory (~14 MB at N=2·10⁵).
- Hand-checked on sample 1: query `(7,11)` → `g[6]=4`; `K=1` needs `4 ≤ 4` ✓, `K=2` needs `max(g[6],g[7])=4 ≤ 3` ✗ → 1. Query `(1,11)` → `max(g[0..4]) = 3 ≤ 6` at `K=5=m//2` → 5.
