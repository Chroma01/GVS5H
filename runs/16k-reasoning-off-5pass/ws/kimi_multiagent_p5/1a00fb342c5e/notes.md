
## ideation
The problem asks to find non-negative integers A_i satisfying XOR constraints A_{X_i} ⊕ A_{Y_i} = Z_i, minimizing the sum. Since XOR operates bitwise independently, and the objective sum decomposes as Σ_i Σ_b 2^b · bit_b(A_i), the whole problem decomposes per bit: for each bit b, we have a GF(2) linear system a_{X_i} ⊕ a_{Y_i} = z_{i,b}, and the cost contribution is 2^b · (number of ones). Since bits are independent and costs are separable per bit, minimizing the total = minimizing each bit's one-count independently (no carry/coupling between bits).

Core structure per bit: a graph with N vertices, M edges labeled with parity z. Consistency: every cycle must have even total parity (xor of edge labels around cycle = 0). Self-loop (X_i = Y_i) forces 0 = z bit, i.e., if z bit is 1 → inconsistent; wait — actually a_{x} ⊕ a_{x} = 0 always, so constraint requires z bit = 0; if z bit = 1, no solution. So self-loops only cause inconsistency, never force a value. (My earlier plan note about forcing was wrong.)

For each connected component (of the graph ignoring self-loops), the solution space is exactly 2 assignments (flip all bits), related by global complement within the component. Choose the one with fewer ones; ties either way. Isolated vertices (no constraints) get 0 for all bits.

Efficient implementation: B = 30 bits (Z ≤ 1e9 < 2^30). Naive per-bit DSU is 30 × (N+M) ≈ 9×10^6 union operations — feasible in Python with fast DSU (iterative find, union by rank) but tight; need optimization. Better approach: process bits independently but share the adjacency structure. Alternative: one DSU per bit is simplest to code; 30 passes over M edges with parity DSU. Each pass: initialize parent array of size N (O(N) per bit → 6×10^6 total, fine), union each edge with parity, then a second pass to check consistency. Then for each component, count sizes and ones.

Counting ones per component per bit: after DSU built, for each vertex compute parity to root; group by root. That's O(N α) per bit. Total ~6×10^6 finds — okay.

Optimization trick: we can avoid re-initializing DSU from scratch per bit by noting the component structure (connectivity) is identical across bits — only parity labels differ. So: build connectivity DSU once (ignoring parities). Then for each bit, we need parity consistency within each component. We could do a per-bit BFS/DFS on adjacency: for each component, pick a root, assign parity 0, propagate via edges, check conflicts, count ones. BFS per bit over all edges = 30 × 2M = 6×10^6 edge relaxations. Similar cost. The DSU-per-bit approach is simpler and less error-prone.

Actually a cleaner single-pass idea: process all bits simultaneously with bitmask DSU? Parity DSU where each edge stores the full mask Z_i (xor of values along path as full integers). Union with mask works the same: parent stores xor-to-parent as integer mask. Consistency check: cycle xor must be 0 mask. This handles ALL bits in ONE DSU pass! Then for each component, we know for each vertex a mask m_v = xor from vertex to root (full 30-bit). Assignment: choose root value r (30-bit) freely; vertex value = m_v ⊕ r. Cost per bit b: number of vertices with bit b of (m_v ⊕ r) set = if r_b=0: cnt_b (count of m_v with bit b set), else size - cnt_b. Choose per bit independently: r_b = 1 if size - cnt_b < cnt_b. This is elegant: one DSU with integer xor labels, O((N+M) α(N)) total, then per component aggregate counts per bit.

Per-component bit counting: for each component, need cnt_b = number of vertices whose mask has bit b set, for 30 bits. Doing this naively per vertex × 30 bits = 6×10^6 operations — fine. Implementation: iterate vertices, find root, mask; accumulate into dict per root: size and per-bit counts. Use arrays indexed by root: size array; bit counts as list of 30 arrays? Memory: 30 × N ints too big (6×10^6 ints ~ 200MB in Python lists — too much). Better: per root store a single integer "sum of masks"? No — we need per-bit counts, not xor.

Alternative: for each root, keep a list/array of 30 counters in a dict only for roots — number of roots ≤ N, each with 30-int list → up to 6×10^6 ints worst case (all isolated vertices are roots, but isolated vertices have mask 0, contributing nothing; we can skip vertices with no edges). Number of non-isolated vertices ≤ 2M = 2×10^5, and roots among them ≤ that. So dict root → [size, [30 counters]] with at most 2×10^5 entries but typically far fewer roots. Worst case components = 1e5 (pairs), each with 30-counter list = 3×10^6 ints — heavy but maybe okay (~100MB?). Risky.

Better memory approach: process per component. After DSU, group vertices by root (dict root → list of vertices). Then for each component, iterate its vertices' masks and accumulate 30 counters as a local list, then decide root value bits and assign final A values. Grouping: total vertices stored ≤ N. Per-component work: size × 30 worst case → 6×10^6. Fine.

Even better: avoid 30× per-vertex inner loop by using bit tricks? We need popcount per bit across masks. Could iterate bits set in mask (while mask: lowbit) — total set bits across all masks ≤ 30 × vertices anyway. Just do the straightforward loop over 30 bits; 6×10^6 simple ops in Python ≈ 2-4 seconds. Hmm, might be tight. Alternative: accumulate counts using sum of (mask >> b) & 1... same thing.

Faster: for each component, we only need, per bit, count of set bits among masks. We can compute by iterating vertices and for each set bit incrementing counter indexed by bit: `while m: b = (m & -m).bit_length()-1; cnt[b]+=1; m &= m-1`. Total iterations = total set bits, average 15 per mask → 3×10^6. Similar.

Then reconstruct: for each component, root value r (30-bit int) built bit by bit choosing minority. Then A_v = mask_v ⊕ r. Isolated vertices: A_v = 0.

Edge cases:
- M = 0: all A_i = 0.
- Self-loop with Z_i ≠ 0 → inconsistent (since x⊕x=0 ≠ Z). Self-loop with Z_i = 0 → no constraint, ignore.
- Duplicate edges with conflicting Z → caught by DSU parity check.
- Z up to 1e9 < 2^30, so 30 bits suffice. A values could be up to 2^30-1.

Consistency check with mask DSU: when unioning x,y with required xor z: find x → (rx, mx), find y → (ry, my). If rx == ry: require mx ⊕ my == z, else -1. Else merge, setting parent xor appropriately: parent[rx] = ry, xor[rx] = mx ⊕ my ⊕ z (standard weighted DSU).

After processing all edges: for each vertex with edges, compute (root, mask to root) via find. Group by root. For each group: size s, counts per bit. r bits: choose r_b = 0 if cnt_b ≤ s - cnt_b else 1 (strictly: choose 1 if s - cnt_b < cnt_b). Then assign.

Complexity: O((N+M) α(N)) for DSU + O(total set bits) for counting. Very efficient — single DSU pass instead of 30.

Pitfalls:
- Recursion: use iterative find with path compression.
- Input parsing speed: use sys.stdin.buffer.read and split.
- Output: join with spaces.
- Vertices with no edges: A=0, skip entirely.
- Make sure find returns (root, xor-to-root) and path compression updates xor correctly.

## worker: Implement the full solution: fast input parsing; w
- XOR constraints decompose bitwise, and the sum objective is separable per bit, so minimizing total sum = minimizing the number of 1-bits per bit independently.
- Instead of 30 separate GF(2) DSUs, a single weighted DSU is used where each node stores the full integer xor-mask to its parent. Union of edge (x,y,z): if roots differ, link with `xr[root_y] = mx ^ my ^ z`; if same root, consistency requires `mx ^ my == z`, else print -1. Self-loop with z≠0 is immediately inconsistent; z==0 is a no-op.
- After all unions, every vertex in a component has mask m_v = xor to root. Choosing root value r gives A_v = m_v ^ r. Per bit b, ones count is cnt_b if r_b=0 else size-cnt_b; pick the smaller per bit (ties → 0).
- Counting per component iterates only set bits of each mask (total ≤ 30·|component|). Isolated vertices stay 0.
- Complexity: O((N+M)·α(N)) DSU + O(total set bits) counting; memory O(N). Iterative find with path compression; fast input via buffer read/split.
- Verified logic against samples mentally: sample1 component {1,2,3}, masks m1=0,m2=3,m3=4; counts per bit: bit0:1, bit1:1, bit2:1, size3 → all minority is 1s? cnt=1, s-c=2 → keep r_b=0 → A=(0,3,4). Sample2: edges force 1⊕3=4,1⊕2=3 ⇒ 2⊕3 must be 7≠5 → -1. Sample3 yields (0,2,9,6,0).

## worker: Verify the implementation against all three sample
**Verification of `find` path compression (the trickiest part):**
- First loop: walks x → root, accumulating `acc` = xor from x to root. Correct.
- Second loop: invariant `cur` = xor from x to `node` along original links. Initially node=x, cur=0 ✓. We set `xr[node] = acc ^ cur`. Since acc = xor(x→root) = cur ⊕ xor(node→root), we get xor(node→root) = acc ⊕ cur ✓. Then `cur ^= nxr` updates cur to xor(x→nxt) ✓. Terminates when node's parent is root (already correct). Verified on chains of length 1, 2, 3 by hand.

**Union logic:** merging ry under rx with `xr[ry] = mx ^ my ^ z`: check A_y = my ⊕ xr[ry] ⊕ (value of rx) and A_x = mx ⊕ (value of rx); A_x ⊕ A_y = mx ⊕ my ⊕ xr[ry] = z ✓. Swap case swaps mx,my symmetrically ✓.

**Sample 1:** edges (1,3,4),(1,2,3). Union: parent[3]=1, xr[3]=4; parent[2]=1, xr[2]=3. Masks: m1=0,m2=3,m3=4; s=3; bit counts: bit0:1 (m2), bit1:1 (m2), bit2:1 (m3). For each bit c=1, s−c=2 ≥ 1 → rval=0. A=(0,3,4) ✓ matches expected.

**Sample 2:** third edge (2,3,5): find(2)=(1,3), find(3)=(1,4); mx^my=7≠5 → -1 ✓.

**Sample 3:** traced: component {1,2,3,4} (vertex 5 touched by edge 4-5 but consistent), vertex 5 gets value 6⊕A_4... Let me verify: edges give A3⊕A1=9, A4⊕A2=4, A2⊕A3=11, A3⊕A4=15, A4⊕A5=6, A3⊕A3=0 (ok). Root 3: m3=0, m1=9, m2=11, m4=15, m5=15⊕6=9. s=5. Counts: bit0: m1,m2,m4,m5 → 4 → s−c=1<4 → rval bit0=1. bit1: m1? 9=1001 no; m2=1011 yes, m4=1111 yes, m5=1001 no → c=2, s−c=3 ≥2 → 0. bit2: m2 no(1011 bit2=0? 1011: bits 0,1,3) → m4 yes → c=1 → 0. bit3: m1,m2,m4,m5 → 4 → rval bit3=1. rval=9. A: A3=9, A1=0, A2=2, A4=6, A5=0 → "0 2 9 6 0" ✓ matches expected.

**Edge cases:**
- M=0: no touched vertices, groups empty, all A=0 → prints N zeros ✓.
- Self-loop z=0: skipped, vertex touched but isolated → gets 0 ✓. Self-loop z≠0 → -1 ✓.
- Conflicting duplicates caught by same-root check ✓.
- Tie-breaking: `s-c < c` strictly → ties choose 0, valid minimum ✓.
- Z=1e9 < 2^30, B=30 sufficient ✓.
- `touched` includes self-loop-only vertices; they form singleton groups with mask 0 → A=0 ✓.

Complexity: O((N+M)α(N)) DSU, O(N + total set bits) counting. Well within limits.
