
## ideation
The problem is a system of XOR constraints on N variables.  
For each edge (X_i, Y_i, Z_i) we need A_{X_i} xor A_{Y_i} = Z_i.

**1. Consistency of the system**  
The constraints form an undirected graph (possibly with self‑loops).  
For each connected component we can fix one node as root, set its value to an unknown variable `x`, and propagate:
- If we go from a node with already known value `v` to a neighbor `u` via edge with value `Z`, we must set `u = v xor Z`.
- This works iff all cycles have XOR of `Z`s equal to `0`.  
During DFS we can check this on the fly: when we encounter an already visited neighbor, the XOR along the current path must equal the already assigned value.

If any inconsistency is found, answer = -1.

**2. Parameterising solutions of a component**  
When the component is consistent, every node `v` has an `offset[v]` (a non‑negative integer) such that any valid assignment can be written as  
`A_v = x xor offset[v]` where `x` is a common non‑negative integer (0 … 2^K‑1, K enough to cover bits of Z).  
Thus the whole component is a family of assignments parametrised by a single integer `x`.  
The sum of the component for a given `x` is `S(x) = Σ (x xor offset[v])`.

**3. Minimising Σ (x xor offset_i)**  
We need the `x` that minimises `S(x)`. The function is bitwise‑separable: the contribution of bit `b` to the sum depends only on the number of `offset` values that have a `1` at bit `b`.  
A classic way to compute the minimum in `O(K * size)` (K ≈ 30) is a **binary trie DP**:

- Insert all `offset` values of the component into a binary trie (bits from most significant, e.g. 30 down to 0).
- Recursively solve the trie: at a node representing bit `b` we have two children `L` (bit 0) and `R` (bit 1). Let `cntL`, `cntR` be the number of numbers that went to each child.  
  If we set the current bit of `x` to `0`, the cost added by this bit is `cntR * 2^b` (numbers in `R` now have a 1, numbers in `L` stay 0).  
  If we set the current bit of `x` to `1`, the cost added is `cntL * 2^b`.  
  Recurse to the chosen child, adding its computed minimal cost of lower bits.
- The optimal decision is `min( cost0 + recurse(L), cost1 + recurse(R) )`.  
  This yields both the minimal sum and the actual bits of `best_x`.

After the best `x` is known, each node’s value is `A_v = x xor offset[v]`.  
The total minimal sum over the whole graph is the sum of the minima of its components.

**4. Algorithm outline**
```
read N, M
build adjacency list: for each edge store (neighbor, Z)
visited[N+1] = false
component_id[N+1] = -1
offset[N+1] = 0
best_x[comp] = 0   // optimal x for each component
answers[N+1] = 0

for v in 1..N:
    if not visited[v]:
        start new component
        run DFS/BFS from v, assigning offset[neighbor] = offset[current] xor Z
        if contradiction: print -1 and exit
        collect list of offsets of this component

        // build trie and compute best_x
        root = empty trie node
        for off in offsets:
            insert(off) into trie
        best_x[comp] = solve_trie(root, max_bit=30)  // returns optimal x and its cost

        // fill answers
        for node in component:
            answers[node] = best_x[comp] xor offset[node]

print answers[1..N]
```

**5. Pitfalls and details**
- Self‑loops (`X_i == Y_i`) are allowed. Consistency requires `Z_i == 0`; otherwise impossible.
- Values can be up to `10^9`, so we need bits up to 30 (since 2^30 > 10^9). Using 30 is safe; could use 31 to be extra safe.
- The graph may be disconnected; treat each component independently.
- Use 64‑bit integer (`int` in Python is unbounded) for sums (the total sum may be up to N·2^30 ≈ 2e5·1e9 ≈ 2e14, still fine).
- Memory: adjacency list with up to 2·M edges, fine for constraints.
- DFS recursion depth could be up to N (2e5). Use iterative BFS/stack or set recursion limit in Python.

**6. Complexity**
- Graph building & DFS: `O(N + M)`.
- Trie DP per component: `O(K * size_of_component)`. Summed over all components = `O(K * N)` ≤ ~6·10^6, well within limits.
- Overall: `O((N + M) * 30)` time, `O(N + M)` memory.

## worker: Implement the input parsing, adjacency list constr
This is a partial implementation covering the first part of the task: input parsing, adjacency list construction, BFS traversal to assign per-node offsets within each connected component, and consistency checking. It correctly detects contradictions (including self‑loops) and prints -1 if any are found. The final assignment of optimal `x` per component and filling the answer array is left for the next step.

## worker: Implement the binary trie DP to compute, for each 
- The graph is processed with BFS to assign each node an `offset` value relative to an arbitrary root, detecting contradictions (including self‑loops) on the fly.
- For each connected component, a binary trie is built from all `offset` values. The recursive DP `dfs(node, bit)` decides the optimal bit of `x` at each level: choosing `0` costs `cnt_right * 2^b` (because all numbers with a `1` at this bit become `1` in the XOR result), choosing `1` costs `cnt_left * 2^b`. The function returns the best prefix of `x` and the minimal cost for lower bits, yielding the optimal `x` for the component.
- The final value for a node is `A_v = best_x xor offset[v]`. This guarantees the sum over the component is minimized.
- Complexity: `O(N + M)` for BFS, plus `O(N * MAX_BIT)` for the trie DP (MAX_BIT = 30), well within limits. Memory usage is `O(N + M)`.
- Edge case: self‑loops are handled by the consistency check; if `X_i == Y_i` and `Z_i != 0`, the system is infeasible.
- The `MAX_BIT = 30` covers numbers up to 2^30 > 10^9; Python integers are unbounded so no overflow issues.
