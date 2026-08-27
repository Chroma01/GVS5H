
## ideation
**Core difficulty**

We have a system of equations of the form `A_x XOR A_y = Z`. This is a linear system over GF(2) per bit, but we also need to minimise the integer sum of the assigned values (not just per‑bit). The graph can be large (N up to 2·10⁵, M up to 10⁵), so we need an O((N+M)·log maxZ) or similar solution.

**Key observations**

1. Each connected component of the graph is independent. Within a component, pick an arbitrary root `r`. For every other node `v`, the value `A_v` is forced to be `A_r XOR d(v)`, where `d(v)` is the XOR of edge labels along any path from `r` to `v`. This is well‑defined iff the component is consistent (no contradictory cycle).

2. For a fixed component, once we choose the value of the root `A_r`, all other nodes are determined. There are only two natural choices for `A_r` that can affect the sum: `0` and some “flip” value `F`. Actually, because we are working over integers, the root can be any non‑negative integer, but the optimal one will be either `0` or the bitwise complement of the “forced” part of the component (the standard trick for minimising sum under XOR constraints).

   More precisely, for each node `v` we have two possible values:
   - `v0 = d(v)` (when `A_r = 0`)
   - `v1 = d(v) XOR F` (when `A_r = F`)

   The total sum for choice `A_r = 0` is `S0 = Σ d(v)`. For choice `A_r = F` the sum is `S1 = Σ (d(v) XOR F)`. The optimal `F` is the bitwise complement of the bitwise OR of all `d(v)` (or equivalently, the bitwise NOT of the bitwise OR, masked to relevant bits). This is a known result: to minimise `Σ (x_i XOR F)` over all `F`, choose `F` to have 1‑bits exactly where the OR of all `x_i` has 0‑bits (i.e., `F = ~OR`). Then `x_i XOR F` simply clears those bits, giving the smallest possible sum.

   However, we must also consider that `A_r` itself contributes to the sum. The root's distance `d(r) = 0`. So the two candidate assignments for the component are:
   - `A_r = 0`, others = `d(v)`
   - `A_r = F`, others = `d(v) XOR F`

   We compute both sums and pick the smaller one.

3. Consistency check: while traversing the component (e.g., with BFS/DFS), we maintain the XOR distance from the root. When we encounter an edge `(x, y, z)` where both ends are already visited, we check that `dist[x] XOR dist[y] == z`. If not, the whole instance is impossible.

4. The graph may have self‑loops (`x == y`). Then we require `0 == z`; otherwise impossible.

**Algorithm outline**

- Build adjacency list with edges `(neighbor, label)`.
- Maintain arrays:
  - `dist[v]`: XOR distance from the root of its component (meaningful only after visited).
  - `visited[v]`: bool.
- For each node `v` from 1 to N:
  - If not visited, start a BFS/DFS from `v` as root.
  - Initialise `dist[v] = 0`.
  - During traversal, for each edge `(v, u, z)`:
    - If `u` not visited: set `dist[u] = dist[v] XOR z`, push to queue.
    - Else: check `dist[v] XOR dist[u] == z`. If not, print `-1` and exit.
  - After traversing the whole component, collect all `dist` values of its nodes (including root's 0).
  - Compute `S0 = Σ dist`.
  - Compute `OR = bitwise OR of all dist`.
  - Compute `F = ~OR` (in Python, `F = (~OR) & ((1 << max_bits) - 1)` or simply `F = (~OR)` if we treat it as infinite‑precision; but we only need bits up to the maximum possible bit in any `Z` or `dist`. Since `Z ≤ 10⁹`, 30 bits suffice. We can compute `F = (~OR) & ((1 << 31) - 1)` to keep it non‑negative.
  - Compute `S1 = Σ (dist XOR F)`.
  - Choose the smaller sum. If `S0 <= S1`, set root value = 0 and all `A_v = dist[v]`. Else set root value = F and `A_v = dist[v] XOR F`.
- Store final `A` array.
- After processing all components, output the sequence.

## worker: Implement the DSU-with-parity approach to solve th
We implemented a DSU with parity (XOR distance to parent).  
Processing each edge either merges two components while maintaining the XOR invariant or detects an inconsistency (when both endpoints already belong to the same component, we verify that the implied XOR matches the given label).  
After all unions, we perform path compression for every node to obtain its XOR distance to the component root.  
For each connected component, we collect all distances. The component is independent: if we set the root value to `R`, every node's value becomes `dist[v] XOR R`.  
We consider two candidate choices for the root: `0` and `F = ~OR` (bitwise complement of the OR of all distances, masked to 31 bits). The first choice yields sum `S0 = Σ dist[v]`; the second yields `S1 = Σ (dist[v] XOR F)`. We pick the smaller sum and assign the corresponding values.  
This produces a good sequence with the minimum possible total sum.
