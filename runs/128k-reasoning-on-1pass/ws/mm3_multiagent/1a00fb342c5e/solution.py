import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    edges = [(int(next(it)), int(next(it)), int(next(it))) for _ in range(M)]

    A = [0] * (N + 1)  # answer, 1-indexed

    # Z_i ≤ 1e9 < 2^30, so we need bits 0..29 (30 bits). Use 31 for safety.
    MAX_BIT = 31

    for bit in range(MAX_BIT):
        # DSU with parity for this bit
        parent = list(range(N + 1))
        xor_to_parent = [0] * (N + 1)
        size = [1] * (N + 1)

        def find(x: int):
            """Return (root, xor from x to root)."""
            if parent[x] != x:
                r, p = find(parent[x])
                p ^= xor_to_parent[x]
                parent[x] = r
                xor_to_parent[x] = p
                return r, p
            else:
                return x, 0

        def union(x: int, y: int, w: int) -> bool:
            """Enforce A[x] XOR A[y] = w. Return False if contradiction."""
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

        # Process all constraints for this bit
        ok = True
        for x, y, z in edges:
            w = (z >> bit) & 1
            if not union(x, y, w):
                ok = False
                break
        if not ok:
            print(-1)
            return

        # Compute root and parity for each node, and count component sizes
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

        # Choose root value (0 or 1) that minimises the number of 1-bits
        root_bit = [0] * (N + 1)
        for r in range(1, N + 1):
            if comp_size[r] == 0:
                continue
            if comp_one[r] * 2 <= comp_size[r]:
                root_bit[r] = 0
            else:
                root_bit[r] = 1

        # Add this bit's contribution to each A_i
        add = 1 << bit
        for i in range(1, N + 1):
            if root_bit[root_of[i]] ^ parity_of[i]:
                A[i] += add

    # Output the optimal sequence
    print(' '.join(str(A[i]) for i in range(1, N + 1)))

if __name__ == "__main__":
    solve()