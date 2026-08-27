
## ideation
**Restating.** Root the tree anywhere (say vertex 1). Every path in a decomposition, when rooted, has a unique highest vertex; below that vertex it descends into at most **two** child-subtrees (a "V" shape). So a path = one upward chain, or two upward chains glued at their common top.

**Why the DP is forced (core insight).** Process vertices in post-order. For vertex `v` let `f(v)` = number of vertices already in the (unique) path piece containing `v` that still needs to be extended through the parent edge, or `0` if that path is already completed (exactly `K` vertices) inside `v`'s subtree. If a child `c` returns `f(c) = t > 0`, the only edge leaving `c`'s subtree is `c–parent(c) = c–v`, so that partial path **must** be extended through `v`. There is no choice at all → the DP is deterministic, hence a single pass either succeeds or the answer is "No". This is the standard argument that makes the greedy provably correct.

**Recurrence.** Let `c` = number of children with `f(child) > 0`, and `s = 1 + Σ f(child)` over those children.
- `c > 2` → **No** (a path cannot branch three ways at `v`).
- `s > K` → **No**.
- `c == 2` → the path is topped at `v`; it can no longer go up, so we must have `s == K`, otherwise **No**; return `0`.
- `c <= 1` → return `0` if `s == K`, else return `s`.

Answer is "Yes" iff no failure occurred and `f(root) == 0`.

⚠️ **Critical pitfall in the stated plan**: the plan says "return `0` if `s == K` else `s`" without special-casing `c == 2`. That is a bug — with two merged child chains the path is already "closed at the top" and cannot be extended to the parent, so `c == 2 && s < K` must be rejected, not returned as `s`. Must fix this.

**Other pitfalls.**
- Recursion depth up to 2·10⁵ → must use an explicit stack / reverse BFS order, no `sys.setrecursionlimit` hacks (or at least avoid recursion for speed).
- `K == 1`: trivially "Yes"; the DP naturally handles it (every vertex gets `s = 1 = K` → 0), but a direct early return is safe.
- `N == 1, K == 1`: `NK - 1 = 0` edges — input parsing must tolerate an empty edge list.
- `N*K` up to 2·10⁵, but `N` and `K` individually can be as large as 2·10⁵ (e.g., `N=1`, `K=200000`, a path graph): don't assume small `K`.
- Note the problem says "path of length K" but means **K vertices** (sample: K=2 paths are single edges). Use vertex count.
- Vertex count is exactly `N*K`, so no divisibility check is needed; but a sanity guard doesn't hurt.
- Performance: use `sys.stdin.buffer.read().split()` (or `numpy.frombuffer`/`fromstring` parsing), build CSR adjacency with flat arrays (counting sort of edge endpoints) rather than lists of lists; do a BFS from root recording order + parent, then iterate the order in reverse accumulating `f` into arrays `sum_ch[]` and `cnt_ch[]` on the parent.

**Sanity checks (mental, per samples).**
- Sample 1 (`N=3,K=2`, edges 1-2,2-3,3-4,2-5,5-6): leaves 4,6→1; 3: s=2=K→0; 5: s=2→0; 2: no nonzero children → s=1 → returns 1; root 1: s=2=K→0 → **Yes**. ✔
- Sample 2 (edges 1-2,2-3,3-4,2-5,3-6): vertex 3 has two nonzero children (4,6), s=3>K=2 → **No**. ✔
- Extra test for the `c==2` fix: star-ish tree where two chains of total size `< K` meet — must print No.

## worker: Write the complete Python solution: parse input wi
- Implemented the forced bottom-up DP exactly as planned, with the corrected recurrence:
  - For vertex `v`: `c` = number of children that returned a nonzero (incomplete) chain, `s = 1 + Σ` those chain sizes.
  - Fail if `c > 2` (a path can't branch 3 ways at its top) or `s > K`.
  - If `s == K` the path is complete inside the subtree → return 0 (nothing propagated).
  - If `s < K` it must extend to the parent; this is impossible when `c == 2` (path already topped at `v`, both ends go down) → fail; also impossible when `v` is the root → fail.
- Determinism argument: a child's incomplete chain can only leave its subtree through the single edge to `v`, so all nonzero child chains must be merged at `v`; no choices exist, so one pass decides.
- `K == 1` and `NK == 1` handled immediately (empty edge list tolerated).
- Iterative BFS + CSR flat arrays, `sys.stdin.buffer.read().split()`; O(NK) time, no recursion.
- Manual checks: sample 1 → Yes, sample 2 → No (vertex 3 gets s=3>K=2). A tree where two short chains meet with total `< K` correctly rejected via the `c == 2` branch.
