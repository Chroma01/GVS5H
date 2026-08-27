import sys
sys.setrecursionlimit(1 << 25)

def solve():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    T = int(next(it))
    out = []
    for _ in range(T):
        H = int(next(it)); W = int(next(it))
        S = [list(next(it).strip()) for _ in range(H)]
        # Check row parity: number of A's (adjacent, flips) must be even
        row_even = True
        for i in range(H):
            cnt = sum(1 for j in range(W) if S[i][j] == 'A')
            if cnt % 2 == 1:
                row_even = False
                break
        if not row_even:
            out.append("0")
            continue
        # Check column parity
        col_even = True
        for j in range(W):
            cnt = sum(1 for i in range(H) if S[i][j] == 'A')
            if cnt % 2 == 1:
                col_even = False
                break
        if not col_even:
            out.append("0")
            continue
        # Precompute prefix sums of A's for rows and columns
        # p_i,j = parity of A's in row i, columns < j
        # q_i,j = parity of A's in column j, rows < i
        # r_ij = 1 XOR p_ij XOR q_ij for B-cells? Wait: constraint is for B-cells: x_i XOR y_j = r_ij.
        # Actually, the condition for B-cells: a_i,j != c_i,j, i.e., (x_i XOR p_ij) XOR (y_j XOR q_ij) = 1.
        # So x_i XOR y_j = 1 XOR p_ij XOR q_ij.
        # Let r_ij = 1 XOR p_ij XOR q_ij.
        # For A-cells, no constraint.
        # Compute p and q
        p = [[0]*W for _ in range(H)]
        for i in range(H):
            s = 0
            for j in range(W):
                p[i][j] = s
                if S[i][j] == 'A':
                    s ^= 1
        q = [[0]*W for _ in range(H)]
        for j in range(W):
            s = 0
            for i in range(H):
                q[i][j] = s
                if S[i][j] == 'A':
                    s ^= 1
        # Build equations for B-cells: x_i XOR y_j = r_ij
        # We need to check consistency. Use Union-Find with parity (bipartite consistency check).
        # Nodes: 0..H-1 for rows, H..H+W-1 for columns.
        parent = list(range(H+W))
        rankv = [0]*(H+W)
        xor_to_parent = [0]*(H+W)  # xor from node to parent
        def find(x):
            if parent[x] == x:
                return x, 0
            r, val = find(parent[x])
            val ^= xor_to_parent[x]
            parent[x] = r
            xor_to_parent[x] = val
            return parent[x], xor_to_parent[x]
        def unite(x, y, val):
            # x XOR y = val
            rx, vx = find(x)
            ry, vy = find(y)
            if rx == ry:
                if (vx ^ vy) != val:
                    return False
                return True
            # Union by rank
            if rankv[rx] < rankv[ry]:
                parent[rx] = ry
                xor_to_parent[rx] = vx ^ vy ^ val
            else:
                parent[ry] = rx
                xor_to_parent[ry] = vx ^ vy ^ val
                if rankv[rx] == rankv[ry]:
                    rankv[rx] += 1
            return True
        consistent = True
        for i in range(H):
            for j in range(W):
                if S[i][j] == 'B':
                    r = 1 ^ p[i][j] ^ q[i][j]
                    if not unite(i, H+j, r):
                        consistent = False
                        break
            if not consistent:
                break
        if not consistent:
            out.append("0")
            continue
        # Count number of B-cells
        b_cnt = sum(1 for i in range(H) for j in range(W) if S[i][j] == 'B')
        if b_cnt == 0:
            # No constraints, all x_i, y_j free
            ans = pow(2, H+W, MOD)
        else:
            # There is at least one B-cell, so solution space dimension 1 (global flip)
            ans = 2
        out.append(str(ans))
    sys.stdout.write("\n".join(out))

solve()