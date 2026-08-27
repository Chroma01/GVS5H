
## ideation
```python
import sys

sys.setrecursionlimit(1 << 20)

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    edges = [(int(next(it)), int(next(it)), int(next(it))) for _ in range(M)]

    # answer sequence (1‑indexed)
    A = [0] * (N + 1)

    # we need bits up to 30 because Z_i ≤ 1e9 < 2^30
    MAX_BIT = 31

    for bit in range(MAX_BIT):
        # DSU with xor‑parity for this bit
        parent = list(range(N + 1))
        xor_to_parent = [0] * (N + 1)
        size = [1] * (N + 1)

        def find(x: int):
            """return (root, xor from x to root)"""
            if parent[x] != x:
                r, p = find(parent[x])
                p ^= xor_to_parent[x]
                parent[x] = r
                xor_to_parent[x] = p
                return r, p
            else:
                return x, 0

        def union(x: int, y: int, w: int) -> bool:
            """enforce A[x] XOR A[y] = w, return False if contradiction"""
            rx, px = find(x)
            ry, py = find(y)
            if rx == ry:
                # already in the same component – check consistency
                return (px ^ py) == w
            # union by size
            if size[rx] < size[ry]:
                rx, ry = ry, rx
                px, py = py, px
            # attach ry under rx
            parent[ry] = rx
            # set xor[ry] so that the constraint holds
            xor_to_parent[ry] = px ^ py ^ w
            size[rx] += size[ry]
            return True

        # process all constraints for this bit
        ok = True
        for x, y, z in edges:
            w = (z >> bit) & 1
            if not union(x, y, w):
                ok = False
                break
        if not ok:
            print(-1)
            return

        # compute root and xor‑to‑root for every node,
        # and count size and number of 1‑parity nodes per component
        root_of = [0] * (N + 1)
        parity_of = [0] * (N + 1)
        comp_size = [0] * (N + 1)
        comp_one = [0] * (N + 1)

        for i in range(1, N + 1):
            r, p = find(i)
            root_of[i] = r
            parity_of[i] = p
            comp_size[r] += 1
            comp_one[r] += p

        # choose the root value (0 or 1) that minimises the number of 1‑bits
        root_bit = [0] * (N + 1)
        for r in range(1, N + 1):
            if comp_size[r] == 0:
                continue
            if comp_one[r] * 2 <= comp_size[r]:
                root_bit[r] = 0
            else:
                root_bit[r] = 1

        # add this bit's contribution to each A_i
        add = 1 << bit
        for i in range(1, N + 1):
            if root_bit[root_of[i]] ^ parity_of[i]:
                A[i] += add

    # output the optimal sequence
    print(' '.join(str(A[i]) for i in range(1, N + 1)))

if __name__ == "__main__":
    solve()
```

## worker: **Read input** – store the `M` triples `(X_i, Y_i,
We treat each bit independently. For a fixed bit `k` the constraints become linear equations over GF(2): `A_{X_i}` XOR `A_{Y_i}` = bit `k` of `Z_i`. A DSU with parity stores for each node the xor to its component’s representative. Merging two components updates the xor of one root to the other; if the two nodes are already in the same component we check consistency. After processing all equations, each connected component is free to choose the value of its root (0 or 1). If a component contains `c` nodes with odd parity (i.e., `d[i]=1`), setting the root to 0 gives `c` ones; setting it to 1 gives `size‑c` ones. To minimise the sum we pick the cheaper option. Repeating for all bits (0…30, enough for `Z_i ≤ 10^9`) yields a feasible sequence with minimal total sum, or detects inconsistency.

The algorithm runs in `O((N+M)·B)` time (`B≈31`) and `O(N)` memory, well within the limits (`N ≤ 2·10^5`, `M ≤ 10^5`).

## worker: finalize
The problem reduces to a system of linear equations over GF(2) for each bit independently.  
For a fixed bit `k`, every constraint `A_x XOR A_y = Z_i^{(k)}` becomes an equation `x XOR y = w` in GF(2).  
A DSU-with-parity maintains for each node its xor-distance to the component's representative. Merging two components sets the xor of one root to the other; if the two endpoints are already in the same component we simply check consistency. Any inconsistency implies the whole instance has no solution.

After all constraints for a bit are processed, each connected component is free to choose the value of its root (0 or 1). If a component has size `s` and contains `c` nodes with odd parity, setting the root to 0 gives `c` ones, setting it to 1 gives `s-c` ones. We pick the cheaper option to minimise the total number of 1-bits for that bit. This greedy choice is optimal because bits are independent and each 1-bit contributes `2^k` to the total sum.

We repeat for all bit positions `0..30` (covering `Z_i ≤ 10^9`). The total complexity is `O((N+M) · B)` with `B=31`, well within limits, and the memory usage is `O(N+M)`.
