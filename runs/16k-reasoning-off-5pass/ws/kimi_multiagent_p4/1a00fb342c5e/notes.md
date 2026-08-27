
## ideation
The problem is a system of XOR equations A_x ⊕ A_y = z over non-negative integers. Key observations:

1. **Graph structure**: Build an undirected graph with edges (X_i, Y_i, Z_i). Within a connected component, choosing any one vertex's value fixes all others (A_v = A_root ⊕ dist(v) where dist is XOR along path). Cycles must be consistent: XOR of edge labels around any cycle must be 0. Self-loops (X_i == Y_i) require Z_i == 0. Parallel edges between same pair must have equal Z.

2. **Consistency check**: BFS/DFS assigning each vertex a "potential" p[v] = A_v ⊕ A_root. For each edge (u,v,z), check p[u] ⊕ p[v] == z; if violated → -1.

3. **Minimization**: Sum of integers = sum over bits b of 2^b × (number of vertices with bit b set). Bits are independent under XOR. For each bit b (0..29 since Z ≤ 1e9 < 2^30, but A could need higher bits? No—if all constraints involve only bits < 30, setting higher bits only increases sum, so optimal A has bits only where needed; actually A values are determined by root choice per component: A_v = t ⊕ p[v] for free parameter t per component. Higher bits of t would add to all vertices in component, never beneficial. So t < 2^30 suffices).

4. **Per-component, per-bit optimization**: For component with potentials p[v], choosing root value t gives bit b of A_v = bit b of t ⊕ bit b of p[v]. Let c = count of v with bit b of p[v] = 1, s = component size. If t's bit b = 0 → c ones; if 1 → s−c ones. Choose min. This is independent per bit and per component. So for each component, compute for each bit b: cnt1[b] = number of vertices with bit b set in p. Then optimal t has bit b = 1 iff cnt1[b] > s − cnt1[b] (i.e., cnt1[b] > s/2). Tie: either, choose 0.

5. **Pitfalls**:
   - N up to 2e5, M up to 1e5 — iterative DFS/BFS to avoid recursion limits, or set recursion limit.
   - Z up to 1e9 → 30 bits (bits 0..29). 2^30 = 1073741824 > 1e9, so bit 29 is max.
   - Multiple edges and self-loops handled naturally by the consistency check.
   - Isolated vertices (no edges): component of size 1 with p=0; optimal t=0 → A=0.
   - M=0: all zeros.
   - Union-find could check consistency but BFS with potentials is simpler and gives p directly.
   - Memory: adjacency list with (neighbor, z) pairs, 2M entries.
   - The answer values can be up to < 2^30, sum fits in Python int anyway.

6. **Algorithm outline**:
   - Build adjacency list.
   - visited array; comp id per vertex; potentials p[v].
   - BFS over components; for each edge check consistency; collect vertices per component (or store comp id and group later).
   - For each component, count bits: iterate vertices, for each set bit increment counter. Then compute t, then assign A_v = t ⊕ p[v].
   - Output A space-separated, or -1.

Complexity: O((N+M) × 30) worst case for bit counting — 6e6 ops, fine. Actually counting bits per vertex: iterate bits set in p[v] using while loop, total set bits ≤ 30N.

## worker: Implement the complete Python solution: read input
- **Model**: Each constraint `A_x ⊕ A_y = z` is an edge. Within a connected component, fixing the root's value determines everything: `A_v = A_root ⊕ p[v]` where `p[v]` is the XOR of edge labels along any path from the root.
- **Consistency**: BFS assigns potentials; every already-visited neighbor must satisfy `p[v] == p[u] ^ z`. This catches bad cycles, parallel edges with different `z`, and self-loops with `z ≠ 0` (a self-loop demands `p[u] == p[u] ^ z`, i.e., `z == 0`). On conflict, print `-1`.
- **Minimization**: Bits are independent under XOR, and the sum is `Σ_b 2^b · (#ones at bit b)`. Per component, the only freedom is the root value `t`, which flips bit `b` of every vertex in the component when `t`'s bit `b` is 1. If `cnt[b]` vertices have bit `b` set among potentials, not flipping gives `cnt[b]` ones, flipping gives `s − cnt[b]`; choose the smaller (ties broken toward not flipping). Bits ≥ 30 never help (all `z < 2^30`, so potentials have no such bits; setting them in `t` would only add `2^b · s` to the sum), so `t < 2^30` is optimal. Isolated vertices get `t = 0` → value 0.
- **Sample verification**:
  1. N=3, edges (1,3,4),(1,2,3): p = [_,0,3,4], one component s=3. cnt per bit: bit0: p2=3 has bit0 → 1; bit1: p2 → 1; bit2: p3=4 → 1. None exceed 1.5, so t=0 → A = (0,3,4). ✓
  2. Adds edge (2,3,5): p[2]^p[3] = 3^4 = 7 ≠ 5 → -1. ✓
  3. Component {1,2,3,4,5}: root 1? BFS from 1: edge (3,1,9) → p3=9; (4,2,4),(2,3,11),(3,4,15),(4,5,6),(3,2,11),(3,3,0),(3,4,15). p1=0, p3=9, p2 = 9^11=2, p4 = 9^15=6, check (4,2,4): 6^2=4 ✓, p5 = 6^6=0. Potentials (0,2,9,6,0), s=5. cnt: bit0: p3=9 →1; bit1: p2=2,p4=6 →2; bit2: p4=6 →1; bit3: p3=9 →1. None > 2.5 → t=0 → A=(0,2,9,6,0). ✓ Matches sample.
- **Complexity**: O(N + M) BFS plus O(30·N) bit counting; iterative BFS avoids recursion limits. Memory O(N + M).
