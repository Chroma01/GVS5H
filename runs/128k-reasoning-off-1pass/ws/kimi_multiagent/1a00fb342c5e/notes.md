
## ideation
The core insight is that XOR constraints decompose bit-by-bit: for each bit position b (0..29, since Z_i ≤ 10^9 < 2^30), the constraint A_{X_i} ⊕ A_{Y_i} = Z_i becomes a parity constraint on bit b of the two endpoints. So per bit, we have a system of equations over GF(2): v_x + v_y = z_b (mod 2). This is a classic DSU-with-parity (weighted union-find) problem.

Key observations:
1. **Consistency check**: Use DSU with parity across ALL constraints simultaneously (the parity of a constraint between x and y is the same variable structure; but wait — the parity differs per bit!). Actually the parity relation differs per bit, so a single DSU-with-parity won't directly work because each edge has 30 different parity values (one per bit). However, we can still use ONE DSU where each edge stores the full Z value as a "potential": maintain pot[v] = A-value XOR from v to its parent conceptually — i.e., we want A_x ⊕ A_y = Z_i, which is exactly a "XOR potential" DSU (like the classic problem of maintaining xor distances). The DSU stores d[v] = xor from v to root. Merging x, y with value z: require d[x] ⊕ d[y] ⊕ z consistent. This handles all bits at once! Inconsistency detected when x, y already in same component and d[x] ⊕ d[y] ≠ z. Self-loops (X_i == Y_i) require Z_i == 0.

2. **Minimization**: Within each connected component, once we fix the value of one vertex (the root, say value t), every other vertex's value is determined as t ⊕ d[v]. So the component's assignment is parameterized by a single value t (any non-negative integer, but only bits up to 2^30 matter — actually bits beyond max Z bit: setting them only increases sum, and constraints don't involve them since d values only have bits from Z's... wait, d[v] is XOR of Z's along paths, so d[v] has bits only where some Z has bits. Choosing t's high bits = 0 is optimal). For each bit b independently, the number of vertices in the component with bit b set is either cnt (those with d[v]'s bit b = 1) if t's bit b = 0, or sz - cnt if t's bit b = 1. Choose whichever is smaller; tie → choose 0 (doesn't matter for sum). This minimizes sum because sum = Σ_b 2^b · (number of vertices with bit b set), separable per bit.

3. **Pitfalls**:
   - Self-loop X_i == Y_i: A_x ⊕ A_x = 0, so need Z_i == 0, else -1. DSU handles this naturally (same root, d[x]⊕d[y]=0 ≠ z → inconsistent).
   - Z up to 10^9 < 2^30, so 30 bits suffice. But careful: could t need bits beyond 30? No — higher bits only add to sum, never help.
   - N up to 2·10^5, M up to 10^5 — DSU is fine. Isolated vertices (no constraints) get value 0.
   - Counting per component per bit: need, for each component, the count of vertices with each bit set in d[v]. 30 bits × N — we can accumulate by iterating vertices, grouping by root. Memory/time: O(N·30) = 6·10^6, fine.
   - Python speed: path compression + union by rank iterative; O((N+M) α) fine. The per-bit counting loop over N vertices × 30 bits in pure Python could be ~6M ops — acceptable but should be written efficiently (e.g., for each vertex, iterate over set bits of d[v] instead of all 30 bits).

4. **Plan**: 
   - Read input, build DSU with xor-potential, detect inconsistency → print -1.
   - Group vertices by root; for each root compute sz and bit counts.
   - For each component compute optimal t (bit b set in t iff sz - cnt_b < cnt_b).
   - A_v = t[root(v)] ⊕ d[v]. Print.

## worker: Implement the full solution: DSU with XOR potentia
- **DSU with XOR potentials**: `pot[v]` stores `A_v XOR A_root(v)`. Union of constraint `A_x ⊕ A_y = z` computes `val = pot[x] ^ pot[y] ^ z` (the required xor between the two roots). If roots coincide, consistency requires `val == 0` — this also handles self-loops (`x == y` requires `z == 0`). Iterative `find` with path compression keeps potentials correct.
- **All bits at once**: Since XOR potentials store full integers, all 30 bits are handled simultaneously by one DSU — no need for 30 separate DSUs.
- **Minimization**: Within a component, fixing the root's value `t` determines every vertex as `t ⊕ d[v]`. The total sum is separable per bit: for bit `b`, if `c` vertices have `d[v]`'s bit `b` set, choosing `t`'s bit `b = 0` contributes `c·2^b`, choosing `1` contributes `(sz - c)·2^b`. Pick the smaller (ties → 0). Bits above bit 29 never help (Z < 2^30, and higher bits only add to the sum), so `t` uses only bits 0..29.
- **Complexity**: O((N + M) α(N)) for DSU, O(N · (number of set bits)) ≤ O(30N) for counting, well within limits for N ≤ 2·10^5, M ≤ 10^5.
- Verified against samples: sample 1 → `0 3 4`; sample 2 → `-1` (inconsistent cycle); sample 3 → `0 2 9 6 0`.

## worker: Verify edge cases: M=0 → all zeros; self-loop with
Edge-case verification of the existing implementation:

1. **M = 0**: No union calls; every vertex is its own component with `pot[v] = 0`, `sz = 1`, all bit counts 0. For each bit, `sz - c = 1 > 0 = c`, so `t = 0`. Answer is all zeros — correct (empty sum-minimizing assignment).

2. **Self-loop with Z ≠ 0** (e.g., `X_i = Y_i = v`, `Z_i = 5`): `find(x) == find(y)`, `val = pot[x] ^ pot[y] ^ z = 0 ^ 0 ^ 5 = 5 ≠ 0` → union returns False → prints `-1`. Correct, since `A_v ⊕ A_v = 0` can never equal 5. Self-loop with `Z = 0` returns True (no-op) — correct.

3. **Isolated vertices**: Each forms a singleton component with `d = 0`; optimal `t = 0` (choosing any nonzero bit would only add `2^b` to the sum). They get value 0 — correct.

4. **Bit-width sufficiency**: `Z_i ≤ 10^9 < 2^30 = 1073741824`, so all `pot` values are XORs of Z's and have bits only in positions 0..29. For bit `b ≥ 30`, every `d[v]` has bit 0, so `c = 0`, `sz - c = sz > 0` → `t`'s bit `b` is 0. Hence restricting `t` to 30 bits loses nothing; higher bits would only increase the sum. Correct.

5. **Sample 1** (`N=3`: `1⊕3=4`, `1⊕2=3`): one component, root 1, `d = [0,3,4]`. Bit 0: c=1 (vertex 3), sz=3 → sz-c=2 > 1 → t bit 0. Bit 1: c=1 (vertex 2) → t bit 0. Bit 2: c=2 (vertices 2,3) → sz-c=1 < 2 → t bit 2 = 1... wait: `t = 4` gives `A = [4, 7, 0]`, sum 11, vs `t = 0` gives `[0,3,4]`, sum 7. Recheck: bit 2 count: `d[1]=0` (bit2=0), `d[2]=3` (bit2=0), `d[3]=4` (bit2=1) → c=1, not 2. So t=0, `A = [0,3,4]`, sum 7 — matches expected output. (My miscount; code is correct.)

6. **Sample 2**: constraints `1⊕3=4`, `1⊕2=3`, `2⊕3=5`. After first two: `d[2]=3`, `d[3]=4`. Third: `val = 3^4^5 = 6 ≠ 0`, same root → `-1`. Correct.

7. **Sample 3**: includes duplicate constraints (`3 4 15` twice — consistent), a self-loop `3 3 0` (ok), and `2 3 11` / `3 2 11` (consistent). Component {1,2,3,4} with root potentials; vertex 5 connected via `4⊕5=6`. Tracing the DSU yields optimal `t=0` for the big component giving `A = [0,2,9,6,0]` — matches expected output (sum 17, and each bit's minority choice confirmed by the counting logic).

8. **Correctness of the find/compression**: the two-pass iterative `find` first accumulates `acc = pot[x] ⊕ pot[parent[x]] ⊕ ... ⊕ pot[child-of-root]` (xor from x to root), then rewrites each node on the path to point directly at root with the correct suffix xor. Standard weighted-DSU compression; potentials remain consistent.

9. **Minimality argument**: within a component, all valid assignments are exactly `{t ⊕ d[v]}` for free choice of `t` (root value), since constraints fix all relative xors. Sum is separable per bit with weight `2^b`, and per bit the choice is independent: set the bit in `t` iff fewer than half the vertices have that bit in `d`. Ties (`sz - c == c`) choose 0, which is also optimal. Hence the produced sequence attains the global minimum sum.

Complexity: O((N+M)·α(N)) DSU + O(N·ω) bit counting (ω = set bits ≤ 30) + O(30·#components). Memory O(N + 30·#components) ≤ O(31N). Well within limits.
