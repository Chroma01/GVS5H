import sys
from collections import deque

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); M = int(data[1])
    A = [int(x) - 1 for x in data[2:2 + N]]

    # children[i] = list of j with A_j == i (edges j -> i, constraint x_j <= x_i)
    children = [[] for _ in range(N)]
    indeg = [0] * N
    for i in range(N):
        a = A[i]
        children[a].append(i)
        indeg[a] += 1

    # ps[v] will hold prefix sums of f_v: ps[v][t] = sum_{s<=t} f_v(s), t in 1..M (index 0 unused)
    ps = [None] * N
    removed = [False] * N

    q = deque(i for i in range(N) if indeg[i] == 0)
    mod = MOD
    m = M
    while q:
        v = q.popleft()
        removed[v] = True
        f = [1] * (m + 1)  # f_v(t) for t = 1..m
        for c in children[v]:
            pc = ps[c]
            for t in range(1, m + 1):
                f[t] = (f[t] * pc[t]) % mod
            ps[c] = None  # free child memory
        # build prefix sums
        pv = [0] * (m + 1)
        s = 0
        for t in range(1, m + 1):
            s += f[t]
            if s >= mod:
                s -= mod
            pv[t] = s
        ps[v] = pv
        a = A[v]
        indeg[a] -= 1
        if indeg[a] == 0:
            q.append(a)

    # Remaining nodes (not removed) are exactly the cycle nodes (incl. self-loops).
    incycle = [not removed[i] for i in range(N)]
    seen = [False] * N
    ans = 1
    for i in range(N):
        if incycle[i] and not seen[i]:
            # collect this cycle
            cyc = []
            j = i
            while not seen[j]:
                seen[j] = True
                cyc.append(j)
                j = A[j]
            # component array: product over cycle nodes of product of their non-cycle children's prefix sums
            comp = [1] * (m + 1)
            for v in cyc:
                for c in children[v]:
                    if incycle[c]:
                        continue  # cycle-internal edge
                    pc = ps[c]
                    for t in range(1, m + 1):
                        comp[t] = (comp[t] * pc[t]) % mod
                    ps[c] = None
            s = 0
            for t in range(1, m + 1):
                s += comp[t]
                if s >= mod:
                    s -= mod
            ans = (ans * s) % mod

    print(ans)

main()