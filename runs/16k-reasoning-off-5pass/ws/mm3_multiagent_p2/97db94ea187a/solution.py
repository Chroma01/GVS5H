import sys
from math import comb
from collections import defaultdict

def solve():
    N, P = map(int, sys.stdin.readline().split())
    half = N // 2
    maxM = N * (N - 1) // 2
    max_n = N

    # Precompute bp[a][b][t]: number of bipartite graphs between a left and b right vertices
    # such that every right vertex has degree >= 1, with exactly t edges.
    bp = [[[0] * (max_n * max_n + 1) for _ in range(max_n + 1)] for _ in range(max_n + 1)]
    for a in range(1, max_n + 1):
        for b in range(1, max_n + 1):
            for j in range(0, b + 1):
                sign = -1 if j % 2 == 1 else 1
                c1 = comb(b, j)
                max_edges = a * (b - j)
                for t in range(0, max_edges + 1):
                    bp[a][b][t] = (bp[a][b][t] + sign * c1 * comb(max_edges, t)) % P
            for t in range(a * b + 1):
                bp[a][b][t] %= P
                if bp[a][b][t] < 0:
                    bp[a][b][t] += P

    # Precompute internal edges: number of graphs on n labeled vertices with exactly e edges
    internal = [[0] * (maxM + 1) for _ in range(max_n + 1)]
    for n in range(0, max_n + 1):
        e_max = n * (n - 1) // 2
        for e in range(0, e_max + 1):
            internal[n][e] = comb(e_max, e) % P

    # DP: process levels 0, 1, 2, ...
    # State: (edges_used, even_vertices, total_vertices, last_level_size)
    dp = defaultdict(int)

    # Initialize with level 0 (contains the root vertex 1)
    for n0 in range(1, N + 1):
        ways_choose = comb(N - 1, n0 - 1)
        e0_max = n0 * (n0 - 1) // 2
        for e0 in range(0, e0_max + 1):
            count = ways_choose * internal[n0][e0] % P
            # Level 0 is even (distance 0), so all n0 vertices are even
            dp[(e0, n0, n0, n0)] = (dp[(e0, n0, n0, n0)] + count) % P

    # Process subsequent levels
    for i in range(1, N + 1):
        new_dp = defaultdict(int)
        parity = i % 2
        for (e_prev, k_prev, v_prev, n_prev), cnt in dp.items():
            remaining = N - v_prev
            if remaining < 0:
                continue
            for n_curr in range(0, remaining + 1):
                ways_choose = comb(remaining, n_curr)
                e_int_max = n_curr * (n_curr - 1) // 2
                for e_int in range(0, e_int_max + 1):
                    if n_curr == 0:
                        e_new = e_prev + e_int
                        if e_new > maxM:
                            continue
                        k_new = k_prev
                        v_new = v_prev
                        total = cnt * ways_choose % P
                        total = total * internal[n_curr][e_int] % P
                        new_dp[(e_new, k_new, v_new, n_curr)] = (new_dp[(e_new, k_new, v_new, n_curr)] + total) % P
                    else:
                        max_bip = n_prev * n_curr
                        for e_bip in range(0, max_bip + 1):
                            if e_bip > maxM:
                                continue
                            num_bip = bp[n_prev][n_curr][e_bip]
                            if num_bip == 0:
                                continue
                            e_new = e_prev + e_int + e_bip
                            if e_new > maxM:
                                continue
                            k_new = k_prev + (n_curr if parity == 0 else 0)
                            v_new = v_prev + n_curr
                            total = cnt * ways_choose % P
                            total = total * internal[n_curr][e_int] % P
                            total = total * num_bip % P
                            new_dp[(e_new, k_new, v_new, n_curr)] = (new_dp[(e_new, k_new, v_new, n_curr)] + total) % P
        dp = new_dp
        if not dp:
            break
        all_done = all(v == N for (e, k, v, n) in dp.keys())
        if all_done:
            break

    # Collect answers
    ans = [0] * (maxM + 1)
    for (e, k, v, n), cnt in dp.items():
        if v == N and k == half:
            if N - 1 <= e <= maxM:
                ans[e] = (ans[e] + cnt) % P

    # Output from M = N-1 to N(N-1)/2
    output = []
    for M in range(N - 1, maxM + 1):
        output.append(str(ans[M]))
    print(" ".join(output))

if __name__ == "__main__":
    solve()