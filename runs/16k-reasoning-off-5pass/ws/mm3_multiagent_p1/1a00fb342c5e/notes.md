
## ideation
We need to find a non-negative integer sequence A_1..A_N satisfying M equations of the form A_{X_i} XOR A_{Y_i} = Z_i, and among all such sequences minimize sum A_i.  
Observations:
- XOR constraints are linear over GF(2) per bit. Each bit position (0..30, because Z_i ≤ 1e9 < 2^30) is independent.
- For a fixed bit k, let b_i ∈ {0,1} be the k-th bit of A_i. Each equation becomes b_{X_i} XOR b_{Y_i} = z_i^{(k)} (the k-th bit of Z_i).
- This is a classic bipartite/graph problem solvable with DSU with parity (union-find storing XOR from node to its parent). While merging two nodes with a known XOR, we detect contradictions.
- After processing a bit, the graph splits into connected components. Inside one component, the bit values are determined up to a global flip (choose root bit = 0 or 1). The contribution of this bit to the total sum is the number of 1s among the N positions, which is `cnt1` for choice 0 and `size - cnt1` for choice 1. To minimize sum, pick `min(cnt1, size - cnt1)`. Record the resulting bits for all nodes.
- Do this independently for every bit (0..30). If any bit is inconsistent, answer = -1.
- Complexity: O((N + M) * BITS) with BITS ≈ 30 → O((N+M)*30) ~ 6e6, fine.
- Edge cases: self-loop (X_i == Y_i). Then constraint is 0 = Z_i, so if Z_i != 0 → impossible; else ignore (provides no info).
- Input M can be 0 → then any A works, choose all zeros (minimal sum).
- Since A_i are built bitwise, they fit within Python int (unbounded), but max < 2^30.
- Memory: DSU for each bit re-initialized; we can process bits one by one, building a vector of bits for nodes, and then combine after all bits. Or we can solve all bits simultaneously using linear algebra, but DSU per bit is simpler and fast.

Pitfalls:
- 1-indexed vs 0-indexed indexing.
- Z_i up to 1e9 fits in 30 bits, but safer to handle up to 31 bits (0..30) or use 0..30 while len(bin(Z)) check. We can iterate for bit in range(31) (since 2^30 > 1e9). Actually 1e9 < 2^30, so bits 0..29 are enough. Use 0..30 to be safe.
- When merging, need path compression updating parity to root.
- Need to store per bit the chosen value for each node. Since N up to 2e5 and BITS=31, storing an array of size N for each bit (or a 2D list) is fine (~6e6 booleans/ints).
- After solving all bits, compute A_i = sum(bit_k_i << k).

Algorithm steps:
1. Read N, M and the constraints list [(X_i, Y_i, Z_i)].
2. For each bit b in 0..30:
   a. Initialize DSU with parent[i] = i, xor_to_parent[i] = 0, size[i] = 1.
   b. For each constraint (x, y, z):
      - Let zb = (z >> b) & 1.
      - If x == y: if zb != 0 → inconsistent → print -1 and exit.
      - Else union(x, y) with required xor = zb.
   c. If inconsistent → -1.
   d. After all unions, gather components: for each i, find root and get parity to root (xor[i] = value of b_i if root bit = 0). Count how many nodes have parity 1 (cnt1) per component.
   e. For each component with root r, size s, cnt1:
      - If 2*cnt1 <= s, set root bit = 0 → bits where parity 0 become 0, parity 1 become 1.
      - Else set root bit = 1 → flip: nodes with parity 0 become 1, parity 1 become 0.
      - Store the final bit value for each node: `final_bit[i] = root_bit XOR xor_to_root[i]`.
   f. Accumulate into result array: result[i] |= (final_bit[i] << b).
3. Print result array.

Union-Find with parity details:
- `parent[i]`: root.
- `xor_par[i]`: XOR of node i's value with its parent's value.
- `find(x)`: if parent[x] != x: recursively find root, updating xor_par[x] ^= xor_par[parent[x]]; set parent[x] = root. Return root.
- `union(x, y, w)`: find roots rx, ry and parity px, py (xor from x,y to their roots). We need to satisfy: val_x XOR val_y = w. If we set parent[rx] = ry, we need to set xor_par[rx] so that the equation holds:
  - Let val_x = px XOR root_val_x (if root_val_x is value at root rx). But we treat roots' values as variables; we just need to enforce consistency.
  - Known: val_x XOR val_y = w.
  - val_x = px XOR val_rx, val_y = py XOR val_ry.
  - So px XOR val_rx XOR py XOR val_ry = w → val_rx XOR val_ry = w XOR px XOR py.
  - So when merging, we set parent[rx] = ry and xor_par[rx] = w XOR px XOR py.
  - If rx == ry already, check that px XOR py == w; if not, inconsistent.

Implementation details:
- DSU arrays: parent (size N+1), xor (size N+1), size (size N+1). Use 1-indexed.
- To get per-node parity after DSU built, we can call find(i) for all i, which will set parent[i]=root and xor[i]=xor_to_root.
- We can also maintain a dict or list of lists for component nodes, but we can just compute cnt1 per root: traverse i=1..N, r = find(i), parity = xor[i] (now xor to root). We need to know root's current bit choice later, so we store `parity[i] = xor[i]`. Also maintain `cnt1[r] += parity` and `size[r]` (already known). Use dict or list of length N+1.

Optimization:
- We can reuse DSU across bits by resetting parent and xor arrays (O(N) per bit). That's fine: N=2e5, BITS=31 → 6.2e6 operations.
- Alternatively, we can process all bits in one DSU by storing Z bits as a bitmask and using Gaussian elimination, but DSU per bit is simpler and avoids handling bit vectors.

Edge Cases:
- M=0: DSU initially each node separate. For each bit, each component size=1, cnt1=0 → choose root bit=0 → all bits 0 → A = [0]*N. Sum minimized.
- Duplicate edges: DSU union will handle; might create cycles which we check for consistency.
- Self-loop with Z_i=0: ignore, can skip or union same node; our union will treat x==y specially.
- Large Z: ensure we iterate enough bits. We'll use for b in range(31) (bits 0..30). 2^30 = 1073741824 > 1e9, so bit 30 is always 0. So iterating 0..30 is safe.

Correctness proof sketch:
- For each bit position, the equations are independent linear equations over GF(2). The DSU correctly maintains equivalence classes of variables with known XOR differences. If a contradiction is found (cycle where required XOR ≠ 0), no assignment exists for that bit → no overall assignment.
- If consistent, each component's values are determined up to a global flip. The contribution of this bit to the total sum is the number of 1s among the N variables. Within a component, choosing root bit=0 yields `cnt1` ones; choosing root bit=1 yields `size - cnt1` ones. Since sum is minimized over all components independently (bits are independent), we pick the smaller count for each component. This yields the global minimum sum for that bit. Doing this for every bit yields a global assignment with minimal total sum, because the sum is sum over bits of number of 1s in that bit across all positions, and bits are independent.

Complexities:
- Time: O(BITS * (N + M α(N))) ≈ 30 * 3e5 = 9e6, well within limits.
- Space: O(N) for DSU + O(N) for result.

Potential pitfalls to watch:
- Python recursion limit: find function is recursive; path compression could cause deep recursion if chain long. Use iterative find or increase recursion limit. With path compression, depth small, but to be safe implement iterative find or use recursion with sys.setrecursionlimit(1e6).
- XOR parity accumulation: ensure using XOR (^) correctly.
- Counting size: we can store size in DSU, updated on union (union by size/rank to keep shallow). We'll use union by size.

Implementation plan for find (iterative):
```python
def find(x):
    if parent[x] != x:
        # find root
        root = x
        xor_acc = 0
        while parent[root] != root:
            xor_acc ^= xor_par[root]
            root = parent[root]
        # path compression
        cur = x
        cur_xor = 0
        while parent[cur] != root:
            nxt = parent[cur]
            nxt_xor = xor_par[cur]
            xor_par[cur] = xor_acc ^ cur_xor
            parent[cur] = root
            cur_xor ^= nxt_xor
            cur = nxt
    return parent[x]
```
But that's messy. Simpler: recursive with sys.setrecursionlimit(1 << 25) should be fine. Or we can use while loop to find root and path.

Alternative: store `xor_to_parent` and do standard union with parity.

We'll implement a clean recursive DSU with parity, setting recursionlimit.

Union with size:
```python
def union(x, y, w):
    rx, px = find(x)
    ry, py = find(y)
    if rx == ry:
        return (px ^ py) == w  # consistent
    # merge smaller into larger
    if size[rx] < size[ry]:
        rx, ry = ry, rx
        px, py = py, px
        # w remains same? Wait: we swapped roots, need to recompute required xor.
    parent[ry] = rx
    # we need xor_par[ry] such that: (px XOR val_rx) XOR (py XOR val_ry) = w
    # val_ry is value at new child root; we set parent[ry]=rx, so we need to set xor_par[ry] = val_ry XOR val_rx
    # from equation: val_ry XOR val_rx = px XOR py XOR w
    xor_par[ry] = px ^ py ^ w
    size[rx] += size[ry]
    return True
```
But careful: when we swap, the equation changes. Actually the standard formula: we want to attach ry to rx, and set xor_par[ry] (value of ry XOR value of rx) to satisfy the constraint. Given:
- val_x = px XOR val_rx
- val_y = py XOR val_ry
- Constraint: val_x XOR val_y = w → px XOR val_rx XOR py XOR val_ry = w → val_ry XOR val_rx = w XOR px XOR py.
Thus we set `xor_par[ry] = w ^ px ^ py`. This holds regardless of which root becomes parent, as long as we set xor_par[child] = w ^ px ^ py. If we later attach ry to rx, we need to set xor_par[ry] accordingly. So we don't need to swap the formula; we can just decide parent[ry] = rx and set xor_par[ry] = w ^ px ^ py. To keep tree shallow, we attach smaller size to larger, but we must ensure we compute the formula with the correct px, py corresponding to the roots we are merging. If we swap rx and ry to attach ry to rx, we must recompute using new px, py? Actually if we swap, we are now attaching the original rx to original ry. The formula to set xor_par[child] depends on which node becomes child. If we decide to attach ry to rx (i.e., parent[ry]=rx), we set xor_par[ry] = w ^ px ^ py. If we decide to attach rx to ry, we would set xor_par[rx] = w ^ px ^ py (same w). So we can choose either orientation, but the formula stays the same: xor_par[child] = w ^ px ^ py, where px, py are the xor-to-parent of the original nodes x and y before find. Since we are merging the components, the choice of orientation does not change the equation; we just need to set xor_par[child] appropriately.

So in union:
```python
def union(x, y, w):
    rx, px = find(x)
    ry, py = find(y)
    if rx == ry:
        return (px ^ py) == w
    # attach smaller to larger
    if size[rx] < size[ry]:
        rx, ry = ry, rx
        # we are now attaching original ry to original rx? Wait we swapped roots.
        # But we need to recompute px, py? No, px, py are the values from find(x) and find(y) before any swapping.
        # If we swap roots, we are effectively changing which component is parent.
        # The equation for setting xor_par[child] is w ^ px ^ py, where child is the root we set as child.
        # So if we swap, we set parent[ry] = rx, but after swap rx is the new parent (larger).
        # But we need to ensure that the child we set is the one that becomes non-root.
        # In the code, we set parent[ry] = rx. So we must ensure that ry is the root we want to attach.
        # If we swapped, ry is now the smaller root (original rx). So it's correct.
        # So we can just do:
    parent[ry] = rx
    xor_par[ry] = w ^ px ^ py
    size[rx] += size[ry]
    return True
```
But we need to be careful: if we swap rx and ry to ensure size[rx] >= size[ry], we also need to swap px and py? No, because px is the xor from x to its root (original rx), py from y to its root (original ry). After swapping rx and ry, the variable names change: the root that will be the parent is now the larger one. The root that becomes child is the smaller one. The formula for xor_par[child] uses the px and py corresponding to the nodes x and y, which are fixed. The child root is the one that is being attached. If we swap, we are attaching the original rx (now named ry) to original ry (now named rx). So we set parent[ry] = rx (i.e., parent[original_rx] = original_ry). Then xor_par[ry] (which is original_rx) should be set to w ^ px ^ py. That's correct. So swapping roots is fine, we just set parent[ry] = rx after potential swap.

Thus union is correct.

Now after processing all constraints for a bit, we need to compute final bits. We can do:
```python
bits = [0] * (N+1)
cnt1_per_root = {}
size_per_root = {}
# First, ensure path compression: call find(i) for i=1..N, which will set parent[i] = root, xor_par[i] = parity to root.
# Then we can compute:
for i in range(1, N+1):
    root = find(i)  # find also returns parity? We'll have find return (root, xor)
```
Better to have find return both root and xor. So:
```python
def find(x):
    if parent[x] != x:
        orig_parent = parent[x]
        root, px = find(orig_parent)
        parent[x] = root
        xor_par[x] ^= px
    return parent[x], xor_par[x]
```
But in Python recursion, returning tuple is fine.

Alternatively, we can call find(i) and store root and parity in arrays:
```python
parity = [0]*(N+1)
root_of = [0]*(N+1)
for i in range(1, N+1):
    r, p = find(i)
    root_of[i] = r
    parity[i] = p
    # accumulate counts
```
But we can combine: we need per root: size (already stored), count of nodes with parity 1.
We can just iterate i, find root r and parity p, then `cnt1[r] += p`, `size[r]` already known (but we need to ensure size array is correct after unions). We can also just use a dict: `comp_nodes[r].append(p)` and then decide. But we can do:
```python
cnt1 = {}
for i in range(1, N+1):
    r, p = find(i)
    cnt1[r] = cnt1.get(r, 0) + p
    # also we need the final bit for i
```
Then for each root in cnt1:
- s = size[root] (if size array is maintained, or we can compute by counting nodes per root, but size is already maintained during union).
- c = cnt1[root]
- choose root_bit = 0 if 2*c <= s else 1.
- Then for all i with root_of[i] == root, final_bit[i] = root_bit ^ parity[i].
- We can store these final bits in a temporary list `bit_vals = [0]*(N+1)`, set bit_vals[i] = final_bit[i].
- Then result[i] |= (bit_vals[i] << b).

But to avoid second pass to set bits, we can directly assign to result[i] as we compute final_bit, but we need to know root_bit for each root. We can first compute all root_bits in a dict, then iterate i again to assign. Since N is 2e5, two passes is fine.

Alternatively, we can compute root_bit choice and assign in one pass by storing root_bit in a dict after counting, then iterating i again to compute final_bit and set result[i]. That's O(N) per bit, fine.

Implementation details:
- We'll maintain `parent`, `xor_par`, `size` as lists of size N+1 (1-indexed).
- In each bit iteration, we reset these lists: `parent = list(range(N+1))`, `xor_par = [0]*(N+1)`, `size = [1]*(N+1)`. This costs O(N) per bit, okay.
- Actually we can avoid resetting `size` by recomputing size from DSU or by resetting. Resetting is fine.

But we can also avoid resetting size by using a separate array `comp_size` that we compute after DSU: for each i, find root, then `comp_size[root] += 1`. That might be simpler: we don't need to maintain size during union for efficiency? We need union by size to keep tree shallow, so we should maintain size. However, we can just not do union by size (no rank), and rely on path compression; the tree could become a chain of length O(N) in worst case (e.g., merging 1-2, 2-3, ...). That could be O(N) per find, leading to O(N^2). With N=2e5 and M=1e5, it's risky. So we need union by size/rank.

Thus we need to maintain `size` array and update on union. So we must reset it each bit.

But we can also maintain a separate `dsu_size` per bit, which we reset.

Alright.

Now, about the constraints: M can be up to 1e5, N up to 2e5. So total memory for storing constraints is fine.

Now, we need to be careful with reading input fast: use sys.stdin.buffer.

Now, let's write the code structure:

```python
import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    constraints = []
    for _ in range(M):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        constraints.append((x, y, z))
    result = [0] * (N + 1)
    MAX_BIT = 30  # because 2^30 > 1e9
    for b in range(MAX_BIT + 1):
        parent = list(range(N + 1))
        xor_par = [0] * (N + 1)
        size = [1] * (N + 1)
        def find(x):
            if parent[x] != x:
                r, px = find(parent[x])
                parent[x] = r
                xor_par[x] ^= px
            return parent[x], xor_par[x]
        def union(x, y, w):
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                return (px ^ py) == w
            if size[rx] < size[ry]:
                rx, ry = ry, rx
                # note: we don't need to swap px, py because they belong to x and y, not to roots.
            parent[ry] = rx
            xor_par[ry] = w ^ px ^ py
            size[rx] += size[ry]
            return True
        consistent = True
        for (x, y, z) in constraints:
            zb = (z >> b) & 1
            if x == y:
                if zb != 0:
                    consistent = False
                    break
                # else ignore
            else:
                if not union(x, y, zb):
                    consistent = False
                    break
        if not consistent:
            print(-1)
            return
        # After all unions, compute components and decide bits
        # First, find root and parity for each node
        root_bit = {}  # root -> chosen bit (0 or 1)
        cnt1 = {}
        parity = [0] * (N + 1)
        root_of = [0] * (N + 1)
        for i in range(1, N + 1):
            r, p = find(i)
            root_of[i] = r
            parity[i] = p
            cnt1[r] = cnt1.get(r, 0) + p
        for r, c in cnt1.items():
            s = size[r]
            # We need size[r] to be correct. Since we updated size on union, it's correct.
            if 2 * c <= s:
                root_bit[r] = 0
            else:
                root_bit[r] = 1
        for i in range(1, N + 1):
            r = root_of[i]
            bit_val = root_bit[r] ^ parity[i]
            result[i] |= (bit_val << b)
    # Output result[1..N]
    print(' '.join(str(result[i]) for i in range(1, N + 1)))

if __name__ == "__main__":
    solve()
```

But we need to double-check: when we compute size[r] after all unions, is it still accurate? Yes, we updated size[rx] when merging.

But we need to be careful: after path compression via find(i) in the final loop, the parent pointers are updated, but size remains the same (size of the root). The root of a component is the representative; after find(i), parent[i] = root. The size array is attached to the root node ID. As long as we don't change the root ID, size is correct. Since we only do path compression (setting parent[i] to root), the root ID remains the same. The size array is only changed during union when we attach child root to parent root and update size[parent_root]. So it's consistent.

One nuance: In the final loop, we call find(i) for each i. This performs path compression. However, if we have a component where the root changed during previous finds? No, the root is stable.

Now, we need to ensure that `size` is accessible after all unions. It's a list, and we can index by root id.

Potential bug: In the final loop, we compute `parity[i]` as the XOR from i to its root after path compression. That's correct.

Now, we need to ensure that we handle the case where M=0: constraints list empty. The for loops will not execute any union. Then for each bit, DSU is initially N components of size 1, each with cnt1=0. So root_bit[r] = 0. final bits are 0. result remains 0. Output all zeros. Good.

Now, check sample 1:
N=3, M=2
Constraints: (1,3,4), (1,2,3)
Bit 0: Z=4 (100) and 3 (011). Bit0: 0 and 1.
- Union 1-3 w=0: they are in same component, parity unknown? Actually we have two components initially: 1,2,3 separate. Union 1-3 with w=0: connect them, root size 2. Then union 1-2 w=1. 1 and 2 are in different components: 1 is in component with 3, 2 is separate. Find(1): root r1, p1=0 (since no xor). Find(2): root r2, p2=0. We need to set w=1. Since size[r1]=2 > size[r2]=1, we attach r2 to r1, xor_par[r2] = w ^ p1 ^ p2 = 1 ^ 0 ^ 0 = 1. So component root r1 now has children: 3 (parity 0) and 2 (parity 1). cnt1: nodes with parity 1: only node 2. s=3, c=1. 2*c=2 <=3, so root_bit=0. Then final bits: node1 parity 0 -> 0; node2 parity 1 -> 1; node3 parity 0 -> 0. So bit0 of A: [0,1,0].
Bit 1: Z bits: (4>>1)&1=0, (3>>1)&1=1. So w=0 for edge 1-3, w=1 for edge 1-2. Similar DSU: union 1-3 w=0, then 1-2 w=1. After unions, component same as before: node1 parity 0, node2 parity 1, node3 parity 0. cnt1=1, s=3, root_bit=0. final bit1: [0,1,0].
Bit 2: Z bits: (4>>2)&1=1, (3>>2)&1=0. w=1 for 1-3, w=0 for 1-2. Union 1-3 w=1, then 1-2 w=0. After union 1-3: component {1,3} with parity: if root 1 bit=0, then 3 has parity 1 (since xor_par[3]=1). Then union 1-2 w=0: find(1) parity 0, find(2) parity 0. Attach root 2 to root 1, xor_par[2] = 0 ^ 0 ^ 0 = 0. So component: root1, children: 3 (parity 1), 2 (parity 0). cnt1 = 1 (node3), s=3, root_bit=0. final bit2: node1=0, node2=0, node3=1. So A = [0,2,4]? Wait combine: A1 = 0*1 + 0*2 + 0*4 = 0. A2 = 1*1 + 1*2 + 0*4 = 1+2=3. A3 = 0*1 + 0*2 + 1*4 = 4. So (0,3,4). Matches sample.

Great.

Now sample 2: N=3, M=3, constraints: (1,3,4), (1,2,3), (2,3,5). Let's see if any bit fails. Bit0: 0,1,1? Actually Z bits: 4=100, 3=011, 5=101. Bit0: 0,1,1. Union 1-3 w=0, 1-2 w=1. After these two, component as before. Then union 2-3 w=1. Now 2 and 3 are already in same component: find(2) parity 1 (from earlier), find(3) parity 0. w=1, check px^py = 1^0=1 == w, consistent. So okay. Bit1: Z bits: 0,1,0. Union 1-3 w=0, 1-2 w=1. After, union 2-3 w=0. Find(2) parity 1, find(3) parity 0, px^py=1 != 0 => inconsistent. So output -1. Good.

Now sample 3: N=5, M=8. Should output (0,2,9,6,0). Let's trust.

Edge Cases: self-loop. If x==y and Z_i != 0, inconsistent. Good.

Now, we should also consider that the DSU per bit is reinitialized. However, we can optimize by storing constraints per bit? No.

Now, we need to ensure that the DSU find function is efficient. Recursive find with path compression is okay if we set recursionlimit high. With N=2e5, recursion depth could be up to N in worst case (chain). Setting recursionlimit to 1e6 is safe. Alternatively, we can implement iterative find to avoid recursion.

Let's implement iterative find to be safe:

```python
def find(x):
    if parent[x] != x:
        # find root
        root = x
        xor_acc = 0
        while parent[root] != root:
            xor_acc ^= xor_par[root]
            root = parent[root]
        # path compression
        cur = x
        cur_xor = 0
        while parent[cur] != root:
            nxt = parent[cur]
            nxt_xor = xor_par[cur]
            xor_par[cur] = xor_acc ^ cur_xor
            parent[cur] = root
            cur_xor ^= nxt_xor
            cur = nxt
    return parent[x], xor_par[x]
```
But this is a bit complex. Let's keep recursive for simplicity and set recursionlimit.

Given the constraints, we will have at most 31 recursion depths per bit? Actually recursion depth equals tree height. With union by size, height is O(log N) ~ 18. So recursion depth is small. So recursive find is fine.

Thus we can use recursive find.

Now, we need to be careful that the `find` function returns a tuple, and we need to call it many times. In Python, recursion overhead is okay.

Now, code:

```python
import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    constraints = []
    for _ in range(M):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        constraints.append((x, y, z))
    result = [0] * (N + 1)
    MAX_BIT = 30
    for b in range(MAX_BIT + 1):
        parent = list(range(N + 1))
        xor_par = [0] * (N + 1)
        size = [1] * (N + 1)
        def find(x):
            if parent[x] != x:
                r, px = find(parent[x])
                parent[x] = r
                xor_par[x] ^= px
            return parent[x], xor_par[x]
        def union(x, y, w):
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                return (px ^ py) == w
            if size[rx] < size[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            xor_par[ry] = w ^ px ^ py
            size[rx] += size[ry]
            return True
        consistent = True
        for (x, y, z) in constraints:
            zb = (z >> b) & 1
            if x == y:
                if zb != 0:
                    consistent = False
                    break
                continue
            if not union(x, y, zb):
                consistent = False
                break
        if not consistent:
            print(-1)
            return
        # Determine bits
        cnt1 = {}
        parity = [0] * (N + 1)
        root_of = [0] * (N + 1)
        for i in range(1, N + 1):
            r, p = find(i)
            root_of[i] = r
            parity[i] = p
            cnt1[r] = cnt1.get(r, 0) + p
        root_bit = {}
        for r, c in cnt1.items():
            s = size[r]
            root_bit[r] = 0 if (2 * c <= s) else 1
        for i in range(1, N + 1):
            r = root_of[i]
            bit_val = root_bit[r] ^ parity[i]
            result[i] |= (bit_val << b)
    print(' '.join(str(result[i]) for i in range(1, N + 1)))

if __name__ == "__main__":
    solve()
```

We need to double-check the `size` array: after we attach child root to parent root, we update `size[rx]`. However, later when we call `find(i)` for all i, we may compress paths, but the root remains the same. So size[r] for root r is correct.

But we need to ensure that for roots that are not the final root (i.e., some nodes that were roots earlier but later became children), we don't accidentally use their size. In the final loop, we only consider `cnt1` which contains keys that are the final roots (because we used `find(i)` to get root). The size array for those roots is correct. The size array for non-root nodes is irrelevant.

Now, one more nuance: The DSU `size` array is updated only on union. After all unions, the root of each component has the correct size. So good.

Now, check memory: parent, xor_par, size each of size N+1 ~ 2e5+1. For 31 bits, we allocate new lists each iteration. That's 31 * 3 * 2e5 ~ 18.6 million integers. Each integer is 28 bytes in Python? Actually Python int is large, but using list of ints is memory heavy. 18.6 million * 28 ~ 520 MB, too high. Wait, we need to be careful. In Python, a list of 2e5 ints is about 2e5 * 28 = 5.6 MB per list. 3 lists = 16.8 MB. But we reinitialize them 31 times. The old lists are garbage-collected. So peak memory is about 3 * 2e5 * 31? Actually at any time, we only have one set of parent, xor_par, size (plus other arrays). So memory is O(N). The result array is N+1 ints. cnt1 dict is O(N) in worst case (each node separate). parity and root_of are O(N). So total memory is O(N) ~ a few million Python objects, maybe ~100 MB? Let's estimate: N=2e5.
- result: 2e5 ints -> ~5.6 MB.
- parent, xor_par, size: each 2e5 -> 3 * 5.6 = 16.8 MB.
- parity, root_of: another 2 lists -> 11.2 MB.
- cnt1 dict: up to 2e5 entries, each entry overhead large. But we can use a list for cnt1? Since roots are indices from 1..N, we can use a list of length N+1 initialized to 0, and increment cnt1[r] for each i. That saves dict overhead. Similarly, root_bit can be a list of length N+1, default -1. Or we can just compute on the fly. Let's use lists for cnt1 and root_bit to avoid dict overhead and speed.

Refactor:
- Initialize `cnt1 = [0] * (N + 1)`.
- Initialize `size` as before.
- After DSU, we need to know which nodes are roots. We can iterate i=1..N, find root r, then `cnt1[r] += parity`. But we need to know size[r]. However, after DSU, some nodes are not roots but we have size for them (stale). But we only care about roots. We can compute size of component by counting nodes per root: `comp_size[r] += 1`. Or we can use the `size` array from DSU, which is correct for roots. But if we compute parity for each i, we also need to know the root's size. We can just use `size[r]` (from DSU) because it's correct for the root. So we don't need a separate comp_size.

Thus:
```python
cnt1 = [0] * (N + 1)
parity = [0] * (N + 1)
root_of = [0] * (N + 1)
for i in range(1, N + 1):
    r, p = find(i)
    root_of[i] = r
    parity[i] = p
    cnt1[r] += p
# Now decide root bits
root_bit = [0] * (N + 1)
for i in range(1, N + 1):
    if root_of[i] == i and i in something? Actually we need to iterate over unique roots.
```
We can iterate over all i, but we can just compute for each root when we encounter it. Since we have `root_of`, we can do:
```python
for r in range(1, N+1):
    if parent[r] == r:  # root
        s = size[r]
        c = cnt1[r]
        root_bit[r] = 0 if (2*c <= s) else 1
```
But careful: after path compression, `parent[r] == r` for all roots (since we called find for all nodes). However, we must ensure that we call find for all nodes before checking parent[r] == r? Actually we call find(i) for all i, which sets parent[i] to root. So for any root r, parent[r] == r. So we can iterate r=1..N and check parent[r]==r. That's efficient.

But we also need to be careful: after find(i), the parent array is compressed. So parent[r] is r for roots. So we can compute root_bit for all r where parent[r] == r. That yields all components.

Alternatively, we can compute root_bit on the fly while iterating i: if root_of[i] == i (i is a root), compute root_bit[i] using cnt1[i] and size[i]. Then store it. Then in the second pass to assign bits, we can use root_bit[root_of[i]].

Let's do:
```python
root_bit = [0] * (N + 1)
for i in range(1, N + 1):
    if root_of[i] == i:
        s = size[i]
        c = cnt1[i]
        root_bit[i] = 0 if (2*c <= s) else 1
```
But careful: `size[i]` is correct only if i is a root. Since we only compute for root_of[i] == i, it's fine.

But note: `root_of[i]` is the root of i. So if we iterate i, we will encounter each root exactly when i is a root. So that's fine.

Thus:
```python
for i in range(1, N + 1):
    r, p = find(i)
    root_of[i] = r
    parity[i] = p
    cnt1[r] += p

for i in range(1, N + 1):
    if root_of[i] == i:
        c = cnt1[i]
        s = size[i]
        root_bit[i] = 0 if (2*c <= s) else 1

for i in range(1, N + 1):
    r = root_of[i]
    bit_val = root_bit[r] ^ parity[i]
    result[i] |= (bit_val << b)
```

This avoids dict and extra loops.

Now, we need to ensure that `size[i]` is correct. After all unions, size[i] for root i is the component size. Since we only do path compression, not path halving that changes root ID, size is attached to the root node ID. So it's correct.

One more nuance: In the first loop, we call find(i) which compresses paths. However, if we call find(i) and then later in the second loop we use `size[i]` for root i, we need to ensure that `size[i]` hasn't been corrupted. It's not. But note: after find(i) for some i, the parent of i is set to root. The size array is unchanged. So fine.

Now, check for potential integer overflow: Z_i up to 1e9, bits 0..30. bit 30 is 0 for all Z_i (since 2^30 = 1073741824 > 1e9). So we could iterate bits 0..29. But iterating to 30 is fine, just extra work (no constraints affect bit 30). However, we must ensure that shifting by 30 doesn't cause overflow in Python? Python ints are arbitrary precision, so fine.

Now, we need to consider the case where M is large (1e5) and N is 2e5. The loops are fine.

Now, let's test with the samples manually or via reasoning.

Sample 1: as we did, works.

Sample 2: we saw bit 1 fails.

Sample 3: we trust.

Now, think about potential pitfalls:
- The DSU `size` array is used to decide root_bit. But we must be careful: after we compress paths, the root nodes are those with `parent[i] == i`. However, in the second loop, we iterate i=1..N and check `root_of[i] == i`. But `root_of[i]` is the root of i. So if i is a root, `root_of[i] == i`. So we can compute root_bit for each root exactly once.

- But what if there is a component where the root is not the original root after unions? After all unions, we have a tree. The root is the one with parent[root] = root. After path compression, all nodes point to that root. So it's fine.

- The `size` array: we update `size[rx]` when merging. However, if we later compress paths, we don't change size. So size[root] is the size of the component.

Now, we need to consider the case where the DSU is not fully compressed before we compute cnt1. In the first loop, we call find(i) for all i, which compresses. So we can compute cnt1 using parity from find(i). But note: we also need to compute `root_of[i]` for all i. That's done in the first loop.

But we need to compute `cnt1` as sum of parity over nodes in component. Since parity is XOR from node to root (assuming root bit = 0). So cnt1[r] = number of nodes with parity 1. That's what we want.

Now, we also need to consider the case where we have a component with size s. The number of ones if root bit = 0 is cnt1. If root bit = 1, number of ones is s - cnt1. We pick min. That's correct.

Now, we need to consider if there is any other constraint that could make the sum smaller by not picking the min for each component independently? Since the total sum is sum over components of min(cnt1, s-cnt1) for that bit, and bits are independent, the global minimum is achieved by minimizing each bit independently. So correct.

Now, we need to ensure that the result A_i is non-negative integer. It is.

Now, consider the possibility of multiple connected components across different bits. They are independent, so we can choose root bits per bit independently.

Now, we should also consider if there is any better solution by choosing different root bits across bits? No, because the sum is additive over bits.

Thus algorithm is correct.

Now, we need to implement solve() with these details.

Potential performance improvements:
- Precompute for each constraint the bit vector? Not needed.
- Use local variables for speed in loops.
- Use sys.stdout.write for output.

Now, let's write the final code.

But before finalizing, we should double-check the DSU union function for correctness when swapping roots.

Test a scenario: union(1,2,0) then union(1,2,0) again. First union: rx=1, ry=2, size[1]=1, size[2]=1, swap? size equal, but we have `if size[rx] < size[ry]` (size[1] < size[2] is false), so no swap. parent[2]=1, xor_par[2]=0^0^0=0, size[1]=2. Second union: find(1) -> (1,0), find(2) -> find(parent[2]=1) -> returns (1,0). So rx=ry=1, px=0, py=0, check (0^0)==0 true.

Now test: union(1,2,0), union(1,2,1). First union: as above, parent[2]=1, xor_par[2]=0. Second union: find(1) -> (1,0), find(2) -> (1,0). px=0, py=0, w=1, check 0^0==1? false, return false. Good.

Now test swapping: Suppose we have two components: root 1 size 2, root 2 size 3. We call union(1,2,w). find(1) gives (r1, p1). find(2) gives (r2, p2). Suppose size[r1] < size[r2] is true (2<3), so we swap: rx, ry = ry, rx. So now rx is the larger root (r2), ry is the smaller (r1). Then we set parent[ry] = rx (i.e., parent[r1] = r2). xor_par[ry] = w ^ px ^ py. Here px is from original x, py from original y. That's correct. So we attach the smaller component to the larger one. The xor_par for the child root is set correctly.

Now, what about parity? Let's test with a small graph: x=1, y=2, w=0. Suppose we have already merged 2-3 with w=1, so component A: nodes {2,3}, root 2, parity: 2->0, 3->1. Then we call union(1,2,0). find(1): (1,0). find(2): (2,0). So px=0, py=0. size[1]=1, size[2]=2. size[1] < size[2] is true, so swap: rx=2, ry=1. parent[1] = 2. xor_par[1] = 0 ^ 0 ^ 0 = 0. So now root is 2, children: 3 (parity 1), 1 (parity 0). This yields consistent assignment: if root bit = 0, then node1 = 0, node2 = 0, node3 = 1. Check: A1 XOR A2 = 0, correct. A2 XOR A3 = 0 XOR 1 = 1, which matches the previous constraint (2-3 w=1). Good.

Now test with a cycle: union(1,2,0), union(2,3,0), union(1,3,0). All consistent. Let's see: after first two unions, we have component with root maybe 1 or 2. Let's simulate: union(1,2,0): size[1]=1,size[2]=1, no swap? Actually size equal, but condition size[rx] < size[ry] false. So parent[2]=1, xor_par[2]=0, size[1]=2. union(2,3,0): find(2) -> find(parent[2]=1) -> (1,0). find(3) -> (3,0). px=0, py=0, w=0. size[rx]=2, size[ry]=1, swap: rx=1, ry=3. parent[3]=1, xor_par[3]=0^0^0=0, size[1]=3. Now union(1,3,0): find(1) -> (1,0). find(3) -> find(parent[3]=1) -> (1,0). So px=0, py=0, w=0, consistent. Good.

Now test inconsistent cycle: union(1,2,0), union(2,3,0), union(1,3,1). After first two unions, component as above. Now union(1,3,1): find(1) -> (1,0). find(3) -> (1,0). px=0, py=0, w=1, inconsistent.

Thus DSU works.

Now, we need to think about the case where we have multiple edges between same nodes with same w. DSU handles it.

Now, we need to think about the case where M=0: constraints list empty. The for loops for each bit will not process any union. DSU remains N components of size 1, each node is a root. For each node i, find(i) returns (i,0). So root_of[i]=i, parity[i]=0. cnt1[i]=0. size[i]=1. root_bit[i] = 0 (since 2*0 <= 1). So final bits all 0. Result all zeros. Good.

Now, we need to consider the case where N is large and M is small. The algorithm is fine.

Now, we need to consider the case where Z_i is large (up to 1e9). The loop for bits up to 30 is fine.

Now, we need to consider the case where N=1. Then we have only one node. Any constraints? If there is a constraint (1,1,Z), then Z must be 0. If consistent, then we have one node, its value is free? Actually if we have no constraints, A_1 can be 0 (min sum). If there is a constraint (1,1,0), it's trivial. Our algorithm: DSU has one node, component size 1, cnt1=0, root_bit=0. So A_1=0. Good.

If there is a constraint (1,1,5) (Z=5), then bit 0 and bit 2 are 1, which would cause inconsistent. Indeed, self-loop with Z != 0 is impossible. Our code checks x==y and zb != 0 and returns -1. Good.

Now, we need to consider if there is a constraint (x,y,z) where x and y are in the same component but with different w (i.e., the XOR sum around a cycle is not zero). DSU catches it.

Thus algorithm is correct.

Now, we need to write the final code with proper I/O.

One more optimization: we can pre-store constraints as three lists: X, Y, Z. But we need to access Z bits per bit. We can store Z as int and shift. That's fine.

Now, we need to consider that Python recursion might be slow but okay.

Now, let's write the final solve().

Potential issues: In the DSU find function, we use `parent[x] != x`. But we need to ensure that `parent` is defined in the closure. Since we define find inside the loop, it captures the current parent list. That's fine.

Now, code:

```python
import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = [0] * M
    Y = [0] * M
    Z = [0] * M
    for i in range(M):
        X[i] = int(next(it))
        Y[i] = int(next(it))
        Z[i] = int(next(it))
    result = [0] * (N + 1)
    MAX_BIT = 30
    for b in range(MAX_BIT + 1):
        parent = list(range(N + 1))
        xor_par = [0] * (N + 1)
        size = [1] * (N + 1)
        def find(x):
            if parent[x] != x:
                r, px = find(parent[x])
                parent[x] = r
                xor_par[x] ^= px
            return parent[x], xor_par[x]
        def union(x, y, w):
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                return (px ^ py) == w
            if size[rx] < size[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            xor_par[ry] = w ^ px ^ py
            size[rx] += size[ry]
            return True
        consistent = True
        for i in range(M):
            zb = (Z[i] >> b) & 1
            x = X[i]
            y = Y[i]
            if x == y:
                if zb != 0:
                    consistent = False
                    break
                continue
            if not union(x, y, zb):
                consistent = False
                break
        if not consistent:
            print(-1)
            return
        # Compute components and choose bits
        cnt1 = [0] * (N + 1)
        parity = [0] * (N + 1)
        root_of = [0] * (N + 1)
        for i in range(1, N + 1):
            r, p = find(i)
            root_of[i] = r
            parity[i] = p
            cnt1[r] += p
        root_bit = [0] * (N + 1)
        for i in range(1, N + 1):
            if root_of[i] == i:
                c = cnt1[i]
                s = size[i]
                root_bit[i] = 0 if (2 * c <= s) else 1
        for i in range(1, N + 1):
            r = root_of[i]
            bit_val = root_bit[r] ^ parity[i]
            result[i] |= (bit_val << b)

## worker: Implement the per-bit DSU with parity algorithm in
The algorithm processes each bit independently using a DSU with parity (xor‑to‑parent).  
- For each bit, constraints `A_x XOR A_y = Z` become `b_x XOR b_y = z_bit`.  
- Union‑find detects inconsistencies (self‑loops with non‑zero bit, or cycles with mismatched XOR).  
- After building components, each component’s bits are determined up to a global flip.  
- To minimize the total sum, for each component we choose the root bit (0 or 1) that yields the smaller number of 1s in that component (`min(cnt1, size-cnt1)`).  
- Bits are independent, so the global minimum is achieved by this greedy choice per component per bit.  
- Final integer sequence is reconstructed by combining the chosen bits.  
Complexities: O((N+M)·BITS) time, O(N) memory per bit, with BITS≈31.
