import sys


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    max_m = N * (N - 1) // 2
    half = N // 2

    # Binomial coefficients modulo P.
    # All arguments are <= 435 << P, so Pascal's rule is valid mod P.
    C = [[0] * (max_m + 1) for _ in range(max_m + 1)]
    for n in range(max_m + 1):
        C[n][0] = 1 % P
        C[n][n] = 1 % P
        for k in range(1, n):
            C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % P

    # cross[a][b][t] = coeff of x^t in ((1+x)^a - 1)^b.
    # This is the generating function for edges between a previous BFS layer
    # of size a and a new layer of size b, where every new vertex has at
    # least one edge to the previous layer.
    cross = [[None] * (N + 1) for _ in range(N + 1)]
    for a in range(1, N + 1):
        base = [0] * (max_m + 1)
        for t in range(1, a + 1):
            base[t] = C[a][t]

        cross[a][0] = [1] + [0] * max_m
        for b in range(1, N + 1):
            prev = cross[a][b - 1]
            cur = [0] * (max_m + 1)
            max_prev = a * (b - 1)
            for i in range(max_prev + 1):
                vi = prev[i]
                if vi:
                    lim = min(a, max_m - i)
                    for j in range(1, lim + 1):
                        cur[i + j] = (cur[i + j] + vi * base[j]) % P
            cross[a][b] = cur

    # trans[a][b] = polynomial for appending a new layer of size b after a
    # previous layer of size a:
    #   ((1+x)^a - 1)^b * (1+x)^(b choose 2)
    trans = [[None] * (N + 1) for _ in range(N + 1)]
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            cr = cross[a][b]
            w = b * (b - 1) // 2
            out = [0] * (max_m + 1)
            max_cr = a * b
            for i in range(max_cr + 1):
                vi = cr[i]
                if vi:
                    lim = min(w, max_m - i)
                    for j in range(lim + 1):
                        out[i + j] = (out[i + j] + vi * C[w][j]) % P
            trans[a][b] = out

    # DP over exact BFS layers from vertex 1.
    # State: (used_vertices, even_vertices, last_layer_size, parity_of_next_layer)
    # Value: truncated generating function by number of edges.
    #
    # parity_of_next_layer = 1 means the next layer is odd (L1, L3, ...),
    # parity_of_next_layer = 0 means the next layer is even (L2, L4, ...).
    dp = {(1, 1, 1, 1): [1] + [0] * max_m}

    for used in range(1, N + 1):
        max_used_edges = used * (used - 1) // 2
        for even in range(1, min(half, used) + 1):
            for last in range(1, used + 1):
                for parity in (0, 1):
                    poly = dp.get((used, even, last, parity))
                    if poly is None:
                        continue

                    rem = N - used
                    for b in range(1, rem + 1):
                        neven = even + (b if parity == 0 else 0)
                        if neven > half:
                            continue
                        if used + b == N and neven != half:
                            continue

                        # Choose the labels of the b vertices in the new layer.
                        choose = C[rem][b]
                        tr = trans[last][b]
                        max_tr = last * b + b * (b - 1) // 2

                        res = [0] * (max_m + 1)
                        for i in range(max_used_edges + 1):
                            vi = poly[i]
                            if vi:
                                lim = min(max_tr, max_m - i)
                                for j in range(lim + 1):
                                    tj = tr[j]
                                    if tj:
                                        res[i + j] = (res[i + j] + vi * tj) % P

                        if choose != 1:
                            for i in range(max_m + 1):
                                res[i] = (res[i] * choose) % P

                        key = (used + b, neven, b, parity ^ 1)
                        old = dp.get(key)
                        if old is None:
                            dp[key] = res
                        else:
                            for i in range(max_m + 1):
                                s = old[i] + res[i]
                                if s >= P:
                                    s -= P
                                old[i] = s

    ans = [0] * (max_m + 1)
    for (used, even, last, parity), poly in dp.items():
        if used == N and even == half:
            for m in range(max_m + 1):
                s = ans[m] + poly[m]
                if s >= P:
                    s -= P
                ans[m] = s

    sys.stdout.write(" ".join(str(ans[m] % P) for m in range(N - 1, max_m + 1)))


if __name__ == "__main__":
    main()