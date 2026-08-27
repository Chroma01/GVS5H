import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        H, W = map(int, input().split())
        S = [input().strip() for _ in range(H)]
        
        # a[i][j] = 1 if A else 0
        a = [[1 if c == 'A' else 0 for c in row] for row in S]
        
        # Check row parity
        ok = True
        for i in range(H):
            xor = 0
            for j in range(W):
                xor ^= a[i][j]
            if xor != 0:
                ok = False
                break
        if not ok:
            print(0)
            continue
        
        # Check column parity
        for j in range(W):
            xor = 0
            for i in range(H):
                xor ^= a[i][j]
            if xor != 0:
                ok = False
                break
        if not ok:
            print(0)
            continue
        
        # Compute P[i][j]: prefix XOR of a[i][k] for k=1..j
        P = [[0]*W for _ in range(H)]
        for i in range(H):
            for j in range(1, W):
                P[i][j] = P[i][j-1] ^ a[i][j]
        
        # Compute Q[j][i]: prefix XOR of a[k][j] for k=1..i
        Q = [[0]*H for _ in range(W)]
        for j in range(W):
            for i in range(1, H):
                Q[j][i] = Q[j][i-1] ^ a[i][j]
        
        # DSU with parity
        parent = list(range(H + W))
        parity = [0] * (H + W)
        size = [1] * (H + W)
        components = H + W
        contradiction = False
        
        def find(x):
            if parent[x] == x:
                return x, 0
            # Iterative path compression
            root = x
            par = 0
            while parent[root] != root:
                par ^= parity[root]
                root = parent[root]
            # Now root is the actual root, par is parity from x to root
            # Path compression
            while parent[x] != x:
                next_x = parent[x]
                next_par = parity[x]
                parent[x] = root
                parity[x] = par
                par ^= next_par
                x = next_x
            return root, par
        
        for i in range(H):
            for j in range(W):
                if S[i][j] == 'B':
                    # Equation: x_i XOR y_j = c
                    c = 1 ^ P[i][j] ^ Q[j][i]
                    # Union i and H+j with parity c
                    ri, pi = find(i)
                    rj, pj = find(H + j)
                    if ri == rj:
                        if (pi ^ pj) != c:
                            contradiction = True
                            break
                    else:
                        # Union by size
                        if size[ri] < size[rj]:
                            ri, rj = rj, ri
                            pi, pj = pj, pi
                        parent[rj] = ri
                        # parity[rj] = pi XOR pj XOR c
                        parity[rj] = pi ^ pj ^ c
                        size[ri] += size[rj]
                        components -= 1
            if contradiction:
                break
        
        if contradiction:
            print(0)
        else:
            print(pow(2, components, MOD))

solve()