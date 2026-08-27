import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = [0] * M
    Y = [0] * M
    Z = [0] * M
    for i in range(M):
        X[i] = int(next(it)) - 1
        Y[i] = int(next(it)) - 1
        Z[i] = int(next(it))

    MAX_BIT = 31  # since Z_i <= 1e9 < 2^30, 31 bits safe (0..30)

    # DSU with parity (xor to parent)
    parent = [0] * N
    rank = [0] * N
    xor_to_parent = [0] * N  # xor from node to its parent
    # temporary arrays for per-bit processing
    size = [0] * N  # component size
    count_one = [0] * N  # number of nodes assigned 1 under current base assignment
    # base assignment for each node: 0 or 1, relative to component's root (if xor_to_parent==0, node value = root_value ^ xor_to_parent)
    # We'll store node values after assignment (for counting)

    def find(x):
        # find root and xor from x to root
        if parent[x] != x:
            orig = parent[x]
            root, xrx = find(orig)
            xor_to_parent[x] ^= xrx
            parent[x] = root
        return parent[x], xor_to_parent[x]

    # We'll process bits one by one.
    # For each bit, we need to rebuild DSU from scratch (since values change).
    # Complexity: O((N+M)*MAX_BIT) ~ 6.2M, fine.

    # First, check feasibility and compute per-bit best assignment.
    # best_bit_value[i] = chosen bit (0 or 1) for node i at current bit.
    # We'll store it in a list of lists? No, we can accumulate into final A.
    A = [0] * N

    for b in range(MAX_BIT):
        # Initialize DSU for this bit
        for i in range(N):
            parent[i] = i
            rank[i] = 0
            xor_to_parent[i] = 0
        contradiction = False
        for i in range(M):
            x = X[i]
            y = Y[i]
            w = (Z[i] >> b) & 1
            # find roots and xors
            rx, xrx = find(x)
            ry, yry = find(y)
            if rx == ry:
                # check consistency: x ^ y should be w
                # actual x ^ y = xrx ^ yry
                if (xrx ^ yry) != w:
                    contradiction = True
                    break
            else:
                # union by rank
                # we need to set parent[rx] = ry, and adjust xor_to_parent[rx] so that
                # (value[x] ^ xor_to_parent[rx] ^ something) = w
                # value[x] = val_rx ^ xrx
                # value[y] = val_ry ^ yry
                # we want value[x] ^ value[y] = w
                # => (val_rx ^ xrx) ^ (val_ry ^ yry) = w
                # => val_rx ^ val_ry = w ^ xrx ^ yry
                # we can set parent[rx] = ry, and xor_to_parent[rx] = w ^ xrx ^ yry
                # (so that val_rx = val_ry ^ xor_to_parent[rx])
                if rank[rx] < rank[ry]:
                    parent[rx] = ry
                    xor_to_parent[rx] = w ^ xrx ^ yry
                else:
                    parent[ry] = rx
                    xor_to_parent[ry] = w ^ xrx ^ yry
                    if rank[rx] == rank[ry]:
                        rank[rx] += 1
        if contradiction:
            print(-1)
            return

        # Now, for each component, we have two possible assignments:
        # root_value = 0 or 1. For each node, its value = root_value ^ xor_to_root.
        # We need to count how many nodes have value 0 and value 1 under root=0.
        # Then choose root_value that gives fewer 1s.
        # We'll do a first pass to compute size and count_one (assuming root=0).
        # We need to aggregate per component.
        # Reset size and count_one.
        for i in range(N):
            size[i] = 0
            count_one[i] = 0
        for i in range(N):
            r, xr = find(i)
            size[r] += 1
            # value under root=0 is xr (since root=0, node = 0 ^ xr = xr)
            if xr == 1:
                count_one[r] += 1
        # Now decide best root for each component.
        # We'll compute chosen bit for each node.
        # Iterate again: for each node, its chosen bit = (root_choice) ^ xor_to_root.
        # root_choice is 0 if count_one[r] * 2 <= size[r] (i.e., 1s <= 0s), else 1.
        # Actually we want fewer 1s. If count_one <= size - count_one, choose root=0.
        # If count_one > size - count_one, choose root=1 (which flips all bits, making
        # number of 1s become size - count_one).
        # In case of tie, root=0 is fine.
        # We'll compute root_choice for each root and store in an array.
        root_choice = [0] * N
        for i in range(N):
            if parent[i] != i:
                continue  # not a root
            # i is a root
            if count_one[i] * 2 <= size[i]:
                root_choice[i] = 0
            else:
                root_choice[i] = 1
        # Now assign bits to A.
        for i in range(N):
            r, xr = find(i)
            bit = root_choice[r] ^ xr
            if bit:
                A[i] |= (1 << b)

    # Output A
    print(' '.join(map(str, A)))

if __name__ == "__main__":
    solve()