import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    k = N // 2
    
    # Precompute binomials mod P up to max_edges
    max_edges = N * (N - 1) // 2
    C = [[0] * (max_edges + 1) for _ in range(max_edges + 1)]
    for n in range(max_edges + 1):
        C[n][0] = 1 % P
        for r in range(1, n + 1):
            C[n][r] = (C[n-1][r-1] + C[n-1][r]) % P
    
    # Precompute binom for n up to N for choosing subsets
    Cn = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        Cn[n][0] = 1 % P
        for r in range(1, n + 1):
            Cn[n][r] = (Cn[n-1][r-1] + Cn[n-1][r]) % P
    
    # Precompute G_all[I][J] = array of length C(I+J, 2) + 1
    G_all = {}
    for I in range(0, k+1):
        for J in range(0, k+1):
            n = I + J
            e = n * (n - 1) // 2
            if e == 0:
                G_all[(I, J)] = [1 % P]
            else:
                arr = [0] * (e + 1)
                for m in range(e + 1):
                    arr[m] = C[e][m]
                G_all[(I, J)] = arr
    
    # DP arrays
    D = {}
    D[(1, 0)] = [1 % P]
    
    for I in range(1, k+1):
        for J in range(0, k+1):
            if I == 1 and J == 0:
                continue
            base = G_all[(I-1, J)]
            cur_len = len(base)
            res = list(base)
            
            for i in range(1, I+1):
                for j in range(0, J+1):
                    if i == I and j == J:
                        continue
                    coeff = Cn[I-1][i-1] * Cn[J][j] % P
                    d_arr = D[(i, j)]
                    g_arr = G_all[(I-i, J-j)]
                    l1 = len(d_arr)
                    l2 = len(g_arr)
                    conv_len = l1 + l2 - 1
                    if len(res) < conv_len:
                        res.extend([0] * (conv_len - len(res)))
                    for idx1 in range(l1):
                        v1 = d_arr[idx1]
                        if v1 == 0:
                            continue
                        for idx2 in range(l2):
                            v2 = g_arr[idx2]
                            if v2 == 0:
                                continue
                            res[idx1+idx2] = (res[idx1+idx2] - coeff * v1 % P * v2) % P
            # Normalize
            for idx in range(len(res)):
                res[idx] %= P
            D[(I, J)] = res
    
    final = D[(k, k)]
    mult = Cn[N-1][k-1]
    
    max_m = N * (N - 1) // 2
    out = []
    for M in range(N-1, max_m + 1):
        if M < len(final):
            val = final[M] * mult % P
        else:
            val = 0
        out.append(str(val))
    print(' '.join(out))

solve()