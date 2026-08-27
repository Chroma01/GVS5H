
## ideation
The core insight is that XOR constraints decompose bitwise: for each bit k (0..29, since Z_i ≤ 1e9 < 2^30), constraint A_{X_i} ⊕ A_{Y_i} = Z_i becomes a parity constraint bit(X_i) ⊕ bit(Y_i) = bit_k(Z_i). This is a 2-coloring problem per bit, solvable with a parity union-find (weighted DSU) per bit, or a single DSU handling all bits simultaneously by storing a 30-bit mask of "difference" per edge (since each bit's parity is independent, we can store the XOR-difference of full values: parent relation stores value v such that A_x = A_root ⊕ v; merging edge (x,y,z) requires A_x ⊕ A_y = z, i.e., diff[x] ⊕ diff[y] = z relative to root). Actually a single DSU storing full integer XOR differences works: each node keeps `d[v]` = A_v ⊕ A_root. Union(x, y, z): find roots rx, ry with dx, dy; need A_x ⊕ A_y = z → (dx ⊕ A_rx) ⊕ (dy ⊕ A_ry) = z → set A_ry = A_rx ⊕ dx ⊕ dy ⊕ z, i.e., parent[ry]=rx, d[ry] = dx ⊕ dy ⊕ z. Consistency check when rx==ry: need dx ⊕ dy == z. Self-loop x==y: need z==0. This handles all bits at once — elegant and fast (O((N+M) α)).

After DSU, each connected component has a free "root value" t (any non-negative integer, but bits beyond 29 would only add to sum, so t ∈ [0, 2^30)). Then A_v = t ⊕ d[v] for all v in component. Sum over component = Σ_v (t ⊕ d[v]). Minimizing over t: per bit independently, count how many d[v] in the component have bit k set (call c); if we set t's bit k = 1, those c become 0 and (size - c) become 1, contributing (size - c)·2^k; else contributes c·2^k. Choose bit k of t = 1 iff (size - c) < c, i.e., c > size/2. So t's bit k = majority of d[v]'s bit k. This is per-component independent.

Pitfalls:
- Need component member lists: after all unions, group vertices by root. N up to 2e5, fine.
- Z_i can be up to 1e9 < 2^30, so 30 bits suffice; t should have no bits above 29 (they'd only increase sum, and d values have none). But careful: could setting higher bits ever help? No — higher bits of t flip nothing in d (d has zero there), so all members get that bit → strictly increases sum. So t < 2^30.
- M=0: each vertex isolated, d=0, majority of zeros → t=0 → all zeros. Correct.
- Inconsistency → print -1.
- Path compression must maintain d correctly: standard weighted DSU find returns root and updates d[v] to be XOR to root.
- Iterative find or recursion with sys.setrecursionlimit; iterative safer.
- Output format: N space-separated integers.

Complexity: O((N+M) α(N)) time, O(N) memory. Fine.

## worker: Implement the full solution in Python: weighted DS
- **Weighted DSU over full XOR values**: `d[v]` stores `A_v ⊕ A_root`. Union of edge `(x, y, z)`: find roots with accumulated diffs `dx, dy`; if same root, consistency requires `dx ⊕ dy == z` (this also covers self-loops `x == y`, requiring `z == 0`). Otherwise attach smaller root under larger, setting `d[ry] = dx ⊕ dy ⊕ z` so the constraint holds. This handles all 30 bits simultaneously.
- **Minimization**: within a component, `A_v = t ⊕ d[v]` for a free root value `t`. Sum decomposes per bit; for bit `k` with `c` members having that bit set in `d`, choosing `t`'s bit = 1 costs `(sz - c)·2^k` vs `c·2^k`. Pick the minority side (set bit iff `c > sz/2`). Bits ≥ 30 never help (all `d` have 0 there, so they'd add `sz·2^k`), so `t < 2^30`.
- **Complexity**: `O((N+M)·α(N))` for DSU plus `O(30·N)` for majority counting; memory `O(N)`.
- Edge cases: `M = 0` → all components singletons with `d=0`, `t=0` → all zeros. Isolated vertices → 0. Inconsistency → `-1`.
- The `find` uses two-pass path compression: first pass accumulates xor from `x` to root, second pass rewrites parents and sets each node's xor-to-root correctly (`d[v] = (xor x→v) ⊕ (xor x→root)`).

## worker: Fix the broken early-exit input-consumption logic 
- **Fixed early-exit bug**: replaced the broken `for _ in range(_, M - 1)` consumption loop with a clean pattern: the loop always reads the three tokens per constraint via `next(it)`, and only performs union work while `ok` is still true. Once an inconsistency is found, remaining tokens are consumed but ignored, then `-1` is printed.
- **Removed dead code**: deleted the incorrect first `find()` and renamed `find2` to `find`.
- **Algorithm** (unchanged, verified correct):
  - Weighted DSU where `d[v] = A_v ⊕ A_root`. Union of `(x, y, z)`: if same root, require `dx ⊕ dy == z` (covers self-loops: `x == y` needs `z == 0`). Else attach with `d[ry] = dx ⊕ dy ⊕ z`.
  - Per component, `A_v = t ⊕ d[v]`; per bit, choose `t`'s bit to put 1s on the minority side (`t` bit set iff count of `d` with that bit > half the component size). Bits ≥ 30 never help since all `d` values are 0 there.
- **Verification against samples** (traced mentally):
  - Sample 1: edges (1,3,4), (1,2,3). Component {1,2,3} with `d = {1:0, 2:3, 3:4}`. Bit 0: c=1 (d=3), sz=3 → t bit 0 = 0. Bit 1: c=1 → 0. Bit 2: c=1 → 0. t=0 → A = (0, 3, 4). ✓
  - Sample 2: third edge (2,3,5): dx=3, dy=4, dx⊕dy=7 ≠ 5 → -1. ✓
  - Sample 3: edges force component {1,2,3,4} (3⊕3=0 self-loop ok), vertex 5 isolated. d: 3:0, 2:11, 4:15, 1:9. Bit counts: bit0: d values 0,11,15,9 → bits: 0,1,1,1 → c=3 > 2 → t bit0=1. bit1: 0,1,1,0 → c=2, not > 2 → 0. bit2: 0,0,1,0 → c=1 → 0. bit3: 0,1,1,1 → c=3 → t bit3=1. t=9. A: 1:9⊕9=0, 2:9⊕11=2, 3:9⊕0=9, 4:9⊕15=6, 5:0 → `0 2 9 6 0`. ✓ Matches expected output.
- **Edge cases**: M=0 → all singletons, d=0, t=0 → all zeros. Self-loop z=0 → consistent (dx⊕dx=0). Self-loop z≠0 → -1. Single edge (x,y,z): d={x:0,y:z}, per bit c∈{0,1}, sz=2, c>1 never → t=0 → A_x=0, A_y=z, minimal. Majority flip: component of 3 with d bits {1,1,0} → t bit set → values {0,0,1}, sum 1 < 2. ✓
- Complexity: O((N+M)·α(N) + 30N) time, O(N) memory.
