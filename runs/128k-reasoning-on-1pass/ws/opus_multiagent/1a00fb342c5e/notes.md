
## ideation
**Core structure.** Each constraint `A_{X_i} XOR A_{Y_i} = Z_i` is an edge in an undirected graph. Within a connected component, fixing one vertex's value fixes all others: `A_v = d_v XOR r`, where `d_v` = XOR of edge weights along any spanning-tree path from the component root, and `r` is a free 30-bit offset (one per component). So:
1. **Feasibility** = consistency check: build spanning forest (BFS/DFS), compute `d`, then verify *every* edge satisfies `d_X XOR d_Y == Z` (this automatically catches odd "XOR-cycles", duplicate edges with different Z, and self-loops with Z≠0).
2. **Optimization** decomposes per bit: `sum A = Σ_b 2^b · (#vertices with bit b set)`. For each component and each bit b, let `c` = number of vertices in the component with bit b of `d` set, `s` = component size. Choosing bit b of `r` = 1 turns count into `s - c`. So set it iff `c > s - c`, i.e. `2c > s`. Ties (`2c == s`) → either choice, same sum.

Since Z ≤ 10⁹ < 2³⁰, only bits 0..29 matter (all A values stay < 2³⁰, non-negative — fine).

**Main difficulty is engineering, not algorithmic:** N up to 2·10⁵, M up to 10⁵, 30 bits ⇒ need O((N+M)·30) with small constants in Python. Naive per-vertex-per-bit Python loops (6·10⁶ ops) is borderline but probably OK; numpy makes it safe.

**Candidate approaches.**
- BFS/DFS spanning forest with CSR adjacency (recommended): flat arrays `head/nxt` or numpy-built CSR (`np.argsort` / `np.bincount` prefix sums), iterative traversal with a list-as-stack or `collections.deque`. Recursion is out (depth up to 2·10⁵).
- Weighted DSU (union-find storing XOR-to-parent, path compression): also natural; detects contradictions during union. But then still need `d` values and component ids — a final `find()` pass gives both. Slightly trickier but avoids adjacency building; DSU with path compression in Python on 10⁵ edges is fine.
- Either way, do the edge-consistency verification as one vectorized numpy pass: `np.any(d[X] ^ d[Y] != Z)`.

**Per-bit minimization vectorized.** With `comp` (component id array) and `d` array as numpy int64:
```
sizes = np.bincount(comp, minlength=K)
for b in range(30):
    ones = (d >> b) & 1
    c = np.bincount(comp, weights=ones, minlength=K)   # float, exact up to 2e5
    flip = (2*c > sizes)
    r += flip[comp].astype(np.int64) << b
A = d ^ r
```

**Pitfalls to watch.**
- Self-loops `X_i == Y_i`: need `Z_i == 0`, else -1. The vectorized edge check handles it (`d^d = 0 != Z`), but make sure self-loops don't break BFS (they'd just try to revisit an already-visited node — harmless).
- Multi-edges / parallel edges with conflicting Z — handled by the full edge verification pass.
- M = 0: every vertex isolated, answer all zeros; make sure input parsing and numpy reshape handle empty edge list.
- Isolated vertices: component of size 1, `d=0`, no flip → 0. Correct.
- 1-indexed input → convert to 0-indexed carefully.
- Fast IO: `sys.stdin.buffer.read()` + `np.frombuffer`/`np.array(data.split(), dtype=np.int64)`; output with `' '.join(map(str, A))` via `sys.stdout.write` (avoid printing numpy array directly).
- Don't forget: must print `-1` alone when infeasible.
- Careful: `np.bincount` with `weights` returns float64; comparison `2*c > sizes` mixes float/int — fine, but cast if paranoid.

## worker: Write the complete Python solution in one file: fa
- Each constraint is an undirected edge with XOR weight. Within a connected component, `A_v = d_v XOR r` where `d_v` is the XOR along a spanning-tree path from the component root and `r` is one free offset per component.
- Feasibility: after computing `d` via iterative DFS/BFS over CSR adjacency, verify **all** edges satisfy `d_X ^ d_Y == Z` with one vectorized numpy check. This automatically catches inconsistent cycles, conflicting parallel edges, and self-loops with `Z != 0` (since `d^d = 0 != Z`). Self-loops don't disturb traversal (target already visited).
- Minimization: `sum A = Σ_b 2^b · count_b`, and bits are independent across components. For component with size `s` and `c` vertices having bit `b` set in `d`, choosing bit `b` of `r` gives count `s - c`; pick 1 iff `2c > s`. Ties are indifferent.
- Bits 0..29 suffice since `Z ≤ 10^9 < 2^30`, so all `d`, `r`, `A` fit under `2^30` and stay non-negative.
- Complexity: O((N+M) + N·30) with numpy vectorized per-bit counting; traversal loop is pure-Python over ~N+2M steps using pre-converted lists for speed.
- Edge cases handled: M = 0 (empty arrays, all-zero output), isolated vertices (size-1 components → 0), 1-indexed input conversion, safe parsing via `map(int, ...)` to avoid numpy bytes→int dtype quirks.
