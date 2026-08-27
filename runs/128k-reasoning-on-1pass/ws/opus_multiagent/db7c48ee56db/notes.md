
## ideation
**Restating / key structural facts**

- Constraint `C(N,K) ≤ 10^6` is the whole game. With `N = 2·10^5`, `C(N,2) ≈ 2·10^10 > 10^6`, so for large `N` necessarily `min(K, N−K) ∈ {0,1}`. In general, if `m = min(K, N−K)`, then `C(N,m) = C(N,K) ≤ 10^6`, and:
  - `m = 2 ⇒ N ≲ 1414`
  - `m = 3 ⇒ N ≲ 180`
  - `m` can be at most ~12 (e.g. `N=22, m=11 → 705k`; `N=24, m=12 → 2.7M > 10^6`).
- Complement trick: XOR of a chosen `K`-subset = `TOT ⊕ (XOR of complementary (N−K)-subset)` where `TOT = A_1⊕…⊕A_N`. So we can always enumerate the smaller side `m = min(K, N−K)`.
- **Critical pitfall:** when enumerating complements we must maximize `TOT ⊕ x` over all complement-XORs `x`, **not** compute `TOT ⊕ max(x)`. Take the max after XOR-ing with TOT.

**Layer sizes are safe**: for `j ≤ m ≤ N/2`, `C(N,j) ≤ C(N,m) ≤ 10^6`, and `sum_{j≤m} C(N,j)` is dominated by the last layer (ratio `C(N,j−1)/C(N,j) = j/(N−j+1)` is small), so a layer-by-layer DP over subset sizes does total work `O(C(N,m) · const)` elements, not more.

**DP formulation (avoids quadratic blow-up)**

Let `L_j[i]` = multiset of XORs of size-`j` subsets whose largest index is `i`. Transition:
`L_{j+1}[t] = { v ⊕ A[t] : v ∈ L_j[i], i < t }`.
Implement by flattening `L_j` into one array `F` sorted by last index, with prefix-count offsets `off[t] = #{subsets with last index < t}`; then `L_{j+1}[t] = F[:off[t]] ⊕ A[t]`. Number of produced elements = `C(N,j+1)` exactly — no wasted work. The Python-level loop is over `t ∈ [0,N)` per layer, which is only a problem if `N` is huge — but `N` huge forces `m ≤ 1`, which we special-case. For `m ≥ 2`, `N ≤ 1414`, so ~`1414 × 12 ≈ 17k` numpy slice/concat calls total: fine.

**Special cases to hard-code**
- `m = 0` (i.e. `K = N`): answer = `TOT`.
- `m = 1`: answer = `max(A)` if `K = 1`, else `max(TOT ⊕ A_i)`. (Handles `N = 2·10^5` fast, purely with numpy.)
- Duplicates in `A` are irrelevant (indices distinct, we just enumerate index subsets).
- `K = N−K` tie: either side works.

**Alternative approaches considered**
1. `itertools.combinations` + `functools.reduce(xor)`: up to `10^6 × 12 ≈ 10^7` Python-level ops → likely 5–15 s; too risky for time limit, but could be a fallback for tiny `N`.
2. Meet-in-the-middle / split halves: unnecessary complexity; the layered DP already hits the `C(N,m)` bound.
3. Naive DP `dp[j] = set/list` without last-index bookkeeping would either lose the "distinct indices" property or become `O(N · C(N,j))`.

**Numeric details**
- `A_i < 2^60`, so `np.int64` (or `uint64`) holds values safely; XOR on int64 is fine. Avoid Python-object dtype.
- Memory: a few arrays of ≤ 10^6 int64 = ~8 MB each; keep only current layer + flattened array.

**Other pitfalls**
- Repeated `np.concatenate` inside the inner loop to build a running accumulator is `O(n²)` — instead precompute the flat array once per layer and slice by prefix offsets.
- Beginning layer: `L_1[i] = {A[i]}` (or start from `L_0` = single empty subset with "last index < 0" semantics; careful with the offset indexing).
- Output must be a plain Python int (numpy int64 prints fine, but convert to be safe).
- Fast input reading (`sys.stdin.buffer.read().split()`) since `N` can be 2·10^5.

## worker: Write the complete Python solution: fast input via
- Complement trick: XOR of a chosen K-subset = TOT ⊕ (XOR of complementary (N−K)-subset). We enumerate the smaller side `m = min(K, N−K)`, whose count `C(N,m) = C(N,K) ≤ 10^6`. Crucially, when using complements we compute `max(TOT ⊕ x)` over all enumerated x (not `TOT ⊕ max(x)`).
- Special cases: `m == 0` (K == N) prints TOT; `m == 1` prints `max(A)` (if K==1) or `max(TOT ⊕ A_i)` — this handles N up to 2·10^5 in O(N) with numpy.
- For `m ≥ 2`, `C(N,2) ≤ 10^6` forces `N ≤ 1414`, so a per-layer Python loop over indices (≤ 1414 × 12 ≈ 17k numpy slice ops) is cheap.
- Layered DP: `F` is the flat array of XORs of size-j subsets ordered by their largest index, with exclusive-prefix offsets `off[t]` = number of entries whose last index < t. Then the size-(j+1) block for last index t is exactly `F[:off[t]] ^ A[t]`, and its size is the new `cnt[t] = off[t]`. Total produced elements per layer = C(N, j+1) exactly, so no quadratic blow-up; also `sum_{j≤m} C(N,j)` is dominated by the last layer, so total work is O(C(N,K)).
- Values < 2^60 fit safely in int64; XOR on int64 is exact. Memory: ≤ ~10^6 int64 per layer (~8 MB), only current layer + concatenated parts held.
- Duplicates in A are irrelevant (index subsets are enumerated); K == N−K tie is fine (either side works).
