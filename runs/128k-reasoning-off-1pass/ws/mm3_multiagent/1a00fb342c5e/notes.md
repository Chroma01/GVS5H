
## ideation
**Core difficulty:**  
We have constraints `A_x XOR A_y = Z` on an undirected graph. The problem is to determine if a non‑negative integer assignment exists and, if so, find one that minimizes the total sum of all `A_i`.

**Key observations:**
1. Each constraint is linear over GF(2) per bit: for each bit `k`, `A_x^(k) XOR A_y^(k) = Z^(k)`.  
   So per bit the graph is a system of XOR equations, solvable by DSU with parity (xor‑distance to representative).
2. Because all bits are independent, we can run one DSU on the whole graph storing the xor from each node to its root. If any contradiction occurs, the whole system is unsatisfiable → answer `-1`.
3. For each connected component, once the DSU fixes all `A_i` up to a common global XOR offset `c` (value of the root), the actual values are `A_i = val[i] XOR c` where `val[i]` is the known xor from `i` to the root.  
   The only freedom is the choice of `c` for that component.
4. Minimizing the sum of `A_i` is equivalent to minimizing each bit’s contribution independently. For a given bit `k`, let `cnt1` be the number of `val[i]` that have a 1 in that bit. If we set bit `k` of `c` to 0, the component contributes `cnt1` ones to the sum; if we set it to 1, it contributes `size - cnt1` ones.  
   Hence we choose the bit of `c` to minimize the number of 1s, i.e. set it to 0 if `cnt1 * 2 <= size`, else 1. Doing this for all bits gives the minimal `c` for that component.
5. After fixing `c` per component, we output `A_i = val[i] XOR c`. This yields the global minimum sum because components are independent.

**Pitfalls / Edge cases:**
- Self‑loops (X_i = Y_i): the constraint forces `Z_i = 0`; otherwise unsatisfiable.
- Multiple edges between the same pair are allowed; they must be consistent.
- N up to 2·10⁵, M up to 10⁵ → need O((N+M) log MAX) with small constant.
- Values up to 10⁹, need up to 30 bits.
- The DSU must store the xor value (as integer) from node to its parent; during find we accumulate xor to root.
- When unioning two nodes with known roots, we must ensure the relative xor condition holds; otherwise contradiction.
- M can be 0 → every component is a single node. Then `val[i] = 0`, and we can set `c = 0` (optimal). Output all zeros.

**Candidate approaches:**
- **DSU with xor distance**: standard. Works in near O((N+M) α(N)).
- **Per‑bit majority**: after processing all components, for each component compute bit counts (≤30 bits) and build minimal `c`. Then assign values.
- **Alternative**: BFS/DFS per component keeping xor from root, but DSU is simpler and handles arbitrary graph order.

**Algorithm outline:**
1. Read N, M and edges `(x, y, z)`.
2. Initialize DSU of size N+1 (1‑based) with parent[i]=i and xor_to_parent[i]=0.
3. For each edge:
   - If `x == y`:
     - If `z != 0` → print -1 and exit.
     - Else ignore (no info).
   - Else:
     - Find roots `rx`, `ry` and their accumulated xor to root (`vx`, `vy`).
     - If `rx == ry`:
       - Check if `vx XOR vy == z`; if not → print -1 and exit.
     - Else:
       - Merge: attach `rx` under `ry` (or vice‑versa) and set `xor_to_parent[rx] = vx XOR vy XOR z`.  
         (Because we need `A_x XOR A_y = z` → `(root XOR vx) XOR (root XOR vy) = z` → `vx XOR vy XOR z = xor_between_roots`.)
4. After all edges processed, build the final values:
   - For each node `i` from 1 to N:
     - Find root `r` and accumulated xor `vi` (call it `val[i]`).
   - For each root, we have a list of its members (or we can process in a second pass: after first pass we have root of each node; we can collect per root a list of `val[i]`).
   - For each root:
     - Let `sz` = size of list.
     - For each bit `b` (0..30):
       - Count `ones = sum((val>>b)&1 for val in list)`.
       - If `ones * 2 > sz` set bit `b` of `c` to 1, else 0.
     - For each node in that component, set `A_i = val[i] XOR c`.
5. Output `A_1 … A_N`.

**Complexities:**  
- DSU operations: O((N+M) α(N)).  
- Counting per bit: for each node we may look at up to 31 bits, or we can pre‑compute bit counts per root in one pass. Since total N is 2·10⁵ and bits ≤ 30, total operations ≤ 6·10⁶, fine.  
- Memory: O(N) for DSU + O(N) for final array.

**Why this yields the minimum sum:**  
For each component, `A_i = val[i] XOR c`. The sum of `A_i` is sum over bits of `(bit_i XOR c_bit) * 2^bit`. Since bits are independent and contribution of a bit is `2^bit * (#ones_if_c=0 vs #ones_if_c=1)`, we minimize each bit separately by taking the majority of zeros in the bit column. This is exactly the described choice.

**Sanity checks with samples:**
- Sample 1: edges (1,3,4) and (1,2,3). DSU links 1,2,3 into one component. `val[1]=0, val[2]=3, val[3]=4`. Bit counts: bit0: 0,0,0 → 0; bit1: 1,1,0 → ones=2, size=3, set c1=1? Actually 2*ones=4 > 3 → set to 1. bit2: 0,0,1 → ones=1, set to 0. bit3: 0,0,0 → set to 0. c = 0b010 = 2? Wait expected c=0 to get A=(0,3,4). Let's recompute: val[2]=3 (011), val[3]=4 (100). bit0 (2^0): 0,0,0 → ones=0 → c0=0. bit1 (2^1): 1,1,0 → ones=2 > 1.5 → c1=1. bit2 (2^2): 0,0,1 → ones=1 ≤ 1.5 → c2=0. So c=2 (binary 010). Then A = val XOR 2 → A1=2, A2=1, A3=6, sum=9, not minimal. The sample optimal is c=0 giving A=(0,3,4). Why does the majority rule not give 0? Because we are minimizing the sum of the values themselves, not the number of 1 bits. The cost of setting a bit of c to 1 vs 0 depends on the weight of the bit (2^k). We cannot just compare counts; we need to consider weighted contribution! My earlier reasoning was flawed.

**Correct approach to minimize sum:**  
We need to choose integer `c` (0..∞) to minimize `Σ (val[i] XOR c)`. This is a classic problem: for each bit independently, if the bit of `c` is 0, the contribution of that bit to the sum is `2^k * (number of val[i] with bit k = 1)`. If it is 1, the contribution is `2^k * (number with bit k = 0)`. Since `2^k` is positive, the decision for each bit is still independent: we compare the two costs. So we set bit k of c to 0 if `2^k * ones_k <= 2^k * zeros_k` i.e. if `ones_k <= zeros_k`, else set to 1. Wait, that's exactly the majority rule (c bit 0 gives cost = ones_k, c bit 1 gives cost = zeros_k). So we want to pick the smaller cost. So if `ones_k <= zeros_k`, set c_k = 0; else set c_k = 1. That is majority zeros. In sample 1:  
- size = 3.  
- bit0: ones=0 <= 3 → c0=0.  
- bit1: ones=2 > 1 (zeros=1) → c1=1.  
- bit2: ones=1 <= 2 → c2=0.  
So c = 0b010 = 2, giving sum 9, but sample says optimal sum is 7 (0+3+4). Something is wrong: maybe my `val[i]` are not correct? Let's recompute DSU:  
Edges: (1,3,4) → 1 XOR 3 = 4. If we set A1 = 0, then A3 = 4.  
(1,2,3) → 1 XOR 2 = 3. If A1=0, A2=3. So A = (0,3,4). Sum=7.  
Now DSU: root 1, val[1]=0, val[2]=3, val[3]=4.  
Cost for c=0: sum = 0+3+4=7.  
Cost for c=2 (binary 010): A = 0^2=2, 3^2=1, 4^2=6 → sum=9.  
Why is c=0 not chosen by the bitwise majority rule? Because c is an integer, not a bitmask of per‑component decisions? Wait, the decision for each bit is independent: we can set each bit of c arbitrarily. So for bit1, setting it to 1 adds cost 1 (zeros) and setting to 0 adds cost 2 (ones). So 1 is cheaper, so we set bit1=1. That's correct. For bit2, setting to 0 adds cost 1 (ones), setting to 1 adds cost 2 (zeros). So 0 is cheaper. So the bitwise optimal c is 2, giving sum 9. But the global optimal c is 0 giving sum 7. How can 0 be better than 2? Let's compute sum for c=0: bit0 cost=0, bit1 cost=2, bit2 cost=1 → total=3 (in number of 1‑bits? No, weighted). Actually sum = 0*1 + 2*2 + 1*4 = 0+4+4=8? Wait, A values: 0 (00), 3 (11), 4 (100). Sum = 0 + 3 + 4 = 7. Let's break by bits:  
- bit0 (2^0=1): 0+1+0 = 1.  
- bit1 (2^1=2): 0+1+0 = 2.  
- bit2 (2^2=4): 0+0+1 = 4.  
Total = 1+2+4 = 7.  
For c=2 (binary 010): A = 2 (010), 1 (001), 6 (110).  
- bit0: 0+1+0 = 1.  
- bit1: 1+0+1 = 2.  
- bit2: 0+0+1 = 1.  
Weighted: 1*1 + 2*2 + 4*1 = 1+4+4=9.  
So indeed c=0 is better. But according to per‑bit independent optimization, bit1 should be 1 because zeros (1) < ones (2). But here c=0 means bit1=0, which gives cost 2 (ones). If we set bit1=1, cost becomes 1 (zeros). So why is total sum smaller with bit1=0? Because the value of c itself (0 vs 2) affects all bits? No, each bit is independent in c. The confusion: When we change a bit of c, we flip that bit in all `A_i`. The cost change for bit k is:  
new_cost = old_cost - (ones_k) * 2^k + (zeros_k) * 2^k = old_cost - (ones_k - zeros_k) * 2^k.  
If ones_k > zeros_k, changing c_k from 0 to 1 reduces cost by (ones_k - zeros_k) * 2^k, which is positive. So setting c_k=1 is always beneficial if ones_k > zeros_k. Here for k=1, ones_k=2, zeros_k=1, so setting c1=1 should reduce cost. Let's check:  
Start with c=0: cost_bit1 = 2 * 2^1 = 4.  
Set c1=1 (c=2): cost_bit1 = 1 * 2^1 = 2. Reduction of 2.  
But total sum increased from 7 to 9. Why? Because we also changed c2? No, c2 stayed 0. Wait, setting c1=1 also affects other bits? No, bits are independent. Let's compute total cost difference:  
Original (c=0): sum = 7.  
New (c=2): sum = 9. Increase of 2.  
But our bitwise analysis says bit1 decreased by 2, bit2 unchanged (0 vs 0), bit0 unchanged (0 vs 0). So net change should be -2. Something is inconsistent.

Let's recalc val bits:  
val[1]=0: bits 00  
val[2]=3: bits 11  
val[3]=4: bits 100 (i.e., bit2=1, bit1=0, bit0=0).  
So:  
- bit0: 0,1,0 → ones=1, zeros=2.  
- bit1: 0,1,0 → ones=1, zeros=2.  
- bit2: 0,0,1 → ones=1, zeros=2.  
Wait! I earlier said val[2]=3 has bits 11. That's true: 3 in binary is 011. So bit0=1, bit1=1, bit2=0.  
val[3]=4 is 100: bit0=0, bit1=0, bit2=1.  
val[1]=0: 000.  
So the bit columns are:  
- bit0: 0,1,0 → ones=1.  
- bit1: 0,1,0 → ones=1.  
- bit2: 0,0,1 → ones=1.  
All bits have exactly one 1 among three values. Then for each bit, ones=1, zeros=2. Since ones < zeros, we set c_k = 0 for all bits, giving c=0. That matches the optimal.  
My earlier mistake: I thought val[2]=3 had bit1=1 and val[3]=4 had bit1=0, but val[3] also has bit1=0. Actually both have bit1=1? No, val[2] bit1 is 1 (since 3=11_2), val[3] bit1 is 0 (since 4=100_2). So bit1 column: 0,1,0 → ones=1. Good.  
Thus the majority rule works: for each bit, if number of ones <= number of zeros, set c bit to 0; else set to 1. Since `ones <= zeros` is equivalent to `ones * 2 <= size`, we set c_k = 0 if `cnt1*2 <= size`, else 1. This is the correct rule.

So the algorithm is correct. The error in my manual trace was miscounting bit1 ones.

**Edge case: large values**  
We need enough bits to cover max possible value: Z_i up to 10^9 (~2^30), and XORs can produce up to 2^30-1, plus the global c can also be up to similar range. So 31 bits (0..30) suffices (since 2^30 ≈ 10^9). We can loop up to 31 or 32 bits to be safe. Actually 10^9 < 2^30, but XOR of two values up to 10^9 can be up to ~2^30, and adding c could reach ~2^31? Let's check: If val[i] is up to 2^30-1, and c is up to 2^30-1, then A_i = val XOR c can be up to (2^30-1) which is < 2^30. So 30 bits (0..29) might be enough for values < 2^30, but XOR of two 30-bit numbers can be 30-bit. However, if we set c to have a high bit, the result could have that high bit set. But the values are bounded by the constraints? Actually Z_i ≤ 10^9 < 2^30, so all Z_i have bits 0..29. The DSU stores xor values which are XORs of some Z's, so still < 2^30. Then val[i] < 2^30. c is chosen to minimize sum, it will also be < 2^30. So 30 bits is enough. We can safely use 31 bits (0..30) to avoid overflow.

**Implementation details:**
- Use recursion or iterative find with path compression, accumulating xor.
- When unioning, we need to compute the xor to set on the edge connecting the two roots. Let `rx`, `ry` be roots, `vx` = xor from `x` to `rx`, `vy` = xor from `y` to `ry`. We need `xor[rx] XOR vx XOR vy XOR xor[ry] = z`. If we attach `rx` to `ry`, we set `parent[rx] = ry` and `xor_to_parent[rx] = vx XOR vy XOR z`. This ensures that after union, the relation holds.
- For self-loop x==y: check z==0.
- To collect components, after DSU we can iterate i=1..N, find root r and vi (xor to root). Store in a dictionary: `comp[r].append(vi)`. Also track that we have the value for that node. Since we may have many nodes, we can use a list of lists sized N+1, but many may be empty. Better to use dict or after first pass we can group by root using a dict. Since N is 2e5, dict of vectors is fine.
- For each component, compute counts per bit. We can precompute for each node its bit representation or just count on the fly. Since we have up to 30 bits, for each node we can add its bits to a running count array per root. Implementation: for each root, maintain a list of vals. After gathering, compute bit counts by iterating the list. This is O(N * B) total, B=30, which is fine (6e6 ops).
- Then compute c for each root, and produce output.
- Finally, output array A[1..N] as space-separated.

**Potential issues:**
- If the graph is disconnected, each component is independent, and we minimize each independently, which yields the global minimum because the sum splits additively.
- DSU with xor is standard; ensure that during find we compute the xor correctly. We can store `xor_to_parent[i]` as the xor from `i` to `parent[i]`. Then `find(i)` returns root and also the accumulated xor. We can implement:

```python
def find(x):
    if parent[x] == x:
        return x, 0
    # path compression
    orig_parent = parent[x]
    root, xor_to_root = find(orig_parent)
    parent[x] = root
    xor_to_parent[x] ^= xor_to_root
    return parent[x], xor_to_parent[x]
```

But we need to be careful: `xor_to_parent[x]` is the xor from `x` to its immediate parent. When we recursively get root and xor from parent to root, the new xor from `x` to root is `xor_to_parent[x] XOR xor_parent_to_root`.

We can also write iterative.

**Test with sample 3:**
Input:
5 8
4 2 4
2 3 11
3 4 15
4 5 6
3 2 11
3 3 0
3 1 9
3 4 15

We need to check if algorithm yields the sample output. But the sample output may not be unique; we just need any optimal. Let's trust the logic.

**Alternative approach: linear algebra (Gaussian elimination over GF(2) for each bit)**
Could also be done but DSU is simpler and handles all bits at once.

**Conclusion:**
The solution is:
1. DSU with xor-distances to check consistency and compute val[i] for each node.
2. Group nodes by component, compute per-bit counts, determine minimal c for each component.
3. Output A_i = val[i] XOR c.

**Complexities:**
- Time: O((N+M) α(N) + N * B) ≈ 2e5 * 30 = 6e6, well within limits.
- Memory: O(N) for DSU and arrays.

**Corner Cases:**
- N=1, M=0: component with single node, val[1]=0, c=0, output 0.
- N=1, M=1, X=Y=1, Z=5: inconsistent, output -1.
- Large N, M=0: all zeros, c=0, output zeros.
- Graph with multiple components: each processed independently.
- Self-loops: only allowed if Z=0.

**Implementation Steps in Python:**
1. Read input.
2. Initialize DSU arrays: parent = list(range(N+1)), xor_par = [0]*(N+1).
3. Define find(x) that returns (root, xor_to_root).
4. For each edge:
   - If X == Y:
     - if Z != 0: print -1; return.
   - Else:
     - rx, vx = find(X)
     - ry, vy = find(Y)
     - if rx == ry:
       - if (vx ^ vy) != Z: print -1; return.
     - else:
       - parent[rx] = ry
       - xor_par[rx] = vx ^ vy ^ Z
5. After processing, build components:
   - comp_vals = dict() mapping root -> list of (node_index, val)
   - Or better: we can just compute A directly: for each node, we have root and val. But we need to compute c for each component first. So we must group.
   - comp_vals = {}
   - for i in 1..N:
       r, v = find(i)
       comp_vals.setdefault(r, []).append((i, v))
6. For each component:
   - size = len(list)
   - bit_counts = [0]*31
   - for (i, v) in list:
       for b in 0..30:
           if (v>>b) & 1: bit_counts[b] += 1
   - c = 0
   - for b in 0..30:
       if bit_counts[b] * 2 > size:  # more ones than zeros
           c |= (1 << b)
   - For each (i, v) in list:
       A[i] = v ^ c
7. Print A[1:].

**Potential micro-optimizations:**
- Instead of dict of lists, we can use a list of lists of size N+1, but that might use O(N) memory even for empty lists (list objects). Dict is fine.
- For bit counts, we can precompute for each integer its bitset or just loop over bits. Since 30 bits is small, loop is fine.

**Testing on samples:**
We should manually test with the provided samples after implementation.

**Additional checks:**
- The DSU union operation must be consistent with the xor we set. Let's verify the union formula:  
  We have nodes x and y. We know the xor from x to its root rx is vx, from y to its root ry is vy. We want to enforce: A_x XOR A_y = Z.  
  Let the value of root rx be R_x, root ry be R_y (unknown). Then A_x = R_x XOR vx, A_y = R_y XOR vy.  
  So (R_x XOR vx) XOR (R_y XOR vy) = Z → R_x XOR R_y = vx XOR vy XOR Z.  
  If we set parent[rx] = ry, we need to store the xor from rx to ry such that when we compute xor from x to new root, we get the correct relation.  
  Currently, if we set parent[rx] = ry, then the xor from rx to its new parent ry should be the xor between R_x and R_y, which is `vx XOR vy XOR Z`. So `xor_par[rx] = vx XOR vy XOR Z`. That's what we did.  
  After this, when we later find x, we will get vx' = vx XOR xor_par[rx] (since path: x -> rx -> ry). And for y, we have vy (unchanged). Then (vx' XOR vy) should equal Z. Let's check: vx' = vx XOR (vx XOR vy XOR Z) = vy XOR Z. Then vx' XOR vy = (vy XOR Z) XOR vy = Z. Good.

- For self-loop x==x: we have A_x XOR A_x = 0, so Z must be 0. We can just check.

**One more thing:** The DSU find with path compression should update the xor correctly. Let's write the find function carefully.

```python
def find(x):
    if parent[x] == x:
        return x, 0

## worker: Implement the DSU with XOR distance, process input
The implementation uses a DSU with XOR distances to verify consistency of all constraints. Each node's value is expressed as `val[i] XOR c_comp`, where `val[i]` is the known XOR of the node with its component root and `c_comp` is a free global XOR for the whole component. For each component, the optimal `c_comp` is built bit by bit: for each bit position, if more than half of the `val[i]` have a 1 in that bit, we set the bit of `c_comp` to 1 (to make the majority become 0), otherwise we set it to 0. This minimizes the total sum because bits are independent and the weight `2^k` is positive. The algorithm runs in O((N+M) α(N) + N·B) time with B=31 bits, well within limits, and uses O(N) memory.
