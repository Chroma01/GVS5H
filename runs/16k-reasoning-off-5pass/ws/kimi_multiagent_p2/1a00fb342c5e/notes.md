
## ideation
The problem reduces to a graph constraint satisfaction problem: vertices are sequence indices, edges are XOR constraints. Key observations:

1. **Component decomposition**: Each connected component is independent. Within a component, fixing any one vertex's value determines all others uniquely (via XOR propagation along paths).

2. **Consistency check**: For each edge (u,v,Z), we need d_u XOR d_v == Z where d_v is the XOR-distance from root. If violated anywhere, output -1. Self-loops (X_i == Y_i) require Z_i == 0.

3. **Minimization**: A_v = r XOR d_v for root value r. Sum = sum over bits k of 2^k * (count of vertices with bit k set). Since bits are independent under XOR, we can choose each bit of r independently: for bit k, if we set r's bit to 0, the count is c_k (number of d_v with bit k set); if set to 1, count is (size - c_k). Choose whichever is smaller.

4. **Pitfalls**:
   - Z_i up to 10^9 means up to 30 bits (bit 0 through 29, since 2^30 > 10^9). Actually 10^9 < 2^30, so bits 0..29 suffice, but safer to use 30 or 31 bits.
   - N up to 2×10^5, M up to 10^5 — need iterative DFS/BFS (recursion limit) or set recursion limit high.
   - Multiple edges between same pair must all be consistent.
   - Isolated vertices (no constraints): d_v = 0, component size 1, choose r = 0.
   - Need to count per-component per-bit: for each component, count how many d_v have each bit set.

5. **Complexity**: O((N+M) * B) where B ≈ 30 bits — fine.

## worker: Write the complete Python solution: parse input wi
- Built adjacency list from the M constraints; ran iterative DFS per component assigning `d[v] = d[u] ^ z` along edges.
- Verified every edge satisfies `d[x] ^ d[y] == z`; on mismatch printed -1 (covers self-loops requiring z=0 and multi-edge conflicts).
- For each component, counted per-bit set counts among `d` values (31 bits covers Z ≤ 10^9 < 2^30, plus margin). Chose root bit = 1 only when it strictly reduces the count (`size - c < c`), giving minimum sum since bits are independent under XOR.
- Reconstructed `A_v = r ^ d_v` per component and output.
- Complexity O((N+M)·31), memory O(N+M). Iterative DFS avoids recursion limits.

## worker: Review and test the current solution for correctne
- **Fixed inefficiency**: The original code stored members during DFS but then discarded them, rebuilt `members_of` in a second pass, and reused `comp_bits` slots to store root values (confusing and error-prone). Now `comp_members` is stored directly during DFS, eliminating the second pass and making the code cleaner.
- **Bit length**: 31 bits (0..30) is safe since Z ≤ 10⁹ < 2³⁰, and XOR of values < 2³⁰ stays < 2³⁰. The `while dv` loop in bit counting handles any set bits correctly regardless.
- **Self-loops**: An edge (v, v, z) adds two adjacency entries but DFS skips already-visited v; the consistency check `d[v] ^ d[v] == z` i.e. `z == 0` correctly rejects nonzero self-loops.
- **M = 0**: All vertices are isolated components of size 1 with d = 0; bit counts are all 0, so r = 0 and answer is all zeros — correct minimum.
- **Correctness of minimization**: Within a component, A_v = r ⊕ d_v. For each bit independently, setting r's bit to 0 yields c set bits, to 1 yields size − c. Choosing the smaller minimizes the sum; bits are independent under XOR so per-bit greedy is globally optimal.
- **Consistency**: BFS assigns d along a spanning forest; any edge violating d_x ⊕ d_y = z makes the system unsatisfiable (since XOR constraints around a cycle must compose to 0), correctly detected.
- **Complexity**: O((N + M)·31) time, O(N + M) memory. Iterative DFS avoids recursion limits.
