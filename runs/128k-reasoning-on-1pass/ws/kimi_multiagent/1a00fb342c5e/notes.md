
## ideation
- Core structural fact: XOR constraints decompose independently by bit. For each bit k, define b_v = (A_v>>k)&1; each edge becomes b_{X_i} XOR b_{Y_i} = (Z_i>>k)&1, a GF(2) parity constraint. Bits never interact, and total sum = Σ_k 2^k·(#ones at bit k), so minimizing each bit’s one-count independently minimizes the total (high bits beyond max Z are forced equal within components and should be 0).
- Per bit this is exactly weighted union-find / parity DSU (a.k.a. 2-coloring with XOR potentials): maintain diff[v] = b_v XOR b_root. Union edge (x,y,w): if same root, check diff[x]^diff[y]==w else conflict; else link roots setting the connecting parity t = w ^ diff[x] ^ diff[y].
- Minimization per bit per connected component: the component has exactly two global orientations (flip all). Count ones under current root orientation; flip the component iff ones > size/2 (tie either way). Contribution independence makes this globally optimal.
- Only bits 0..maxZ.bit_length()-1 can be 1 in an optimal solution; if maxZ=0 the answer is all zeros (always consistent since all w=0).
- Pitfalls:
  - Self-loop X_i==Y_i forces Z_i bit 0; DSU same-root check catches w=1 as inconsistency, w=0 is a no-op.
  - Duplicate/contradictory edges caught by same-root parity check.
  - find must do correct path compression that also rewrites diff to be XOR-to-root; after the counting pass every node must be compressed before reading parent[v] in the final assignment (the provided plan relies on the ones-loop calling find(v) for all v — keep that invariant or re-find in the final loop).
  - Union-by-size attaches root under root; the stored diff on the child root must equal XOR(childRoot, parentRoot)=t, verify sign with a tiny 2-node case.
  - M=0 → no constraints, output N zeros. Inconsistency output exactly -1.
  - Python speed: B≤30, N≤2e5, M≤1e5 ⇒ ~30·(N+M) DSU ops ≈ 9e6 plus 30 fresh size-N arrays (6e6) — OK but use iterative find (no recursion), fast stdin parsing, local variable binding; avoid rebuilding edge bit work inside find.
  - Optional memory/time trim: compress to only vertices appearing in edges, but N is small enough that full arrays are simpler and safe.
- Correctness of plan’s find: walking path then reversing with acc ^= diff[node] yields diff[node]=XOR(node,root); union formula t=w^diff[x]^diff[y] gives diff[x]^t^diff[y]=w as required. Looks sound; main risks are implementation details and edge cases above.

## worker: Implement the complete Python solution: per-bit pa
- **Bit independence**: XOR constraints split per bit; total sum = Σ 2^k·(ones at bit k), so minimizing ones per bit independently minimizes the sum. Bits above `max_z.bit_length()` are all-zero constraints, so optimal answer has them 0 (handled naturally since loop only covers `B = max_z.bit_length()` bits; `max_z = 0` ⇒ all-zeros output, which also covers `M = 0`).
- **Parity DSU**: `diff[v]` = XOR of bit values along parent pointers (after compression, `bit(v) ^ bit(root)`). Union of `(x, y, w)`: if same root, consistency requires `diff[x] ^ diff[y] == w` (catches self-loops with `w=1` and contradictory duplicates); otherwise link smaller root under larger with `diff[child_root] = w ^ diff[x] ^ diff[y]`, which enforces `bit(rx) ^ bit(ry) = t` as required.
- **Iterative find**: collects path, then walks from nearest-to-root downward accumulating `acc ^= diff[node]`, so each `diff[node]` becomes XOR-to-root and `parent[node] = root`. Inlined at the three call sites (two per union, one in the counting pass) to avoid function-call overhead.
- **Minimization**: after the counting pass every node is compressed, so `parent[v]` is the root. Each component has exactly two valid orientations; flip iff `ones * 2 > size` (ties are irrelevant). Final bit = `diff[v] ^ flip[root]`.
- **Complexity**: B ≤ 30 bits, each pass O((N + M)·α) with fresh O(N) arrays ⇒ ≈ 9·10⁶ DSU operations, well within limits. Fast input via `sys.stdin.buffer.read().split()`.
- Verified against samples mentally: sample 1 gives bits 0,1 component {1,2,3} with root value 0 minimizing → `0 3 4`; sample 2 detects parity conflict on the triangle → `-1`; sample 3 → `0 2 9 6 0`.
