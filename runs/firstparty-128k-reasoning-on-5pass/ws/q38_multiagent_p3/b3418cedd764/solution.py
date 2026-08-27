import sys
from collections import deque

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]

    rev = [[] for _ in range(N)]
    for i, p in enumerate(A):
        rev[p].append(i)

    indeg = [len(r) for r in rev]
    q = deque(i for i, d in enumerate(indeg) if d == 0)
    order = []

    while q:
        u = q.popleft()
        order.append(u)
        p = A[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    is_cycle = [d > 0 for d in indeg]

    seen = [False] * N
    active_children = []
    pure_count = 0

    for i in range(N):
        if is_cycle[i] and not seen[i]:
            cyc = []
            v = i
            while not seen[v]:
                seen[v] = True
                cyc.append(v)
                v = A[v]

            lst = []
            for c in cyc:
                for v in rev[c]:
                    if not is_cycle[v]:
                        lst.append(v)

            if lst:
                active_children.append(lst)
            else:
                pure_count += 1

    cur = [0] * N
    sums = [0] * len(active_children)
    mod = MOD

    for _ in range(M):
        for u in order:
            prod = 1
            for v in rev[u]:
                prod = (prod * cur[v]) % mod
            val = cur[u] + prod
            if val >= mod:
                val -= mod
            cur[u] = val

        for idx, lst in enumerate(active_children):
            prod = 1
            for v in lst:
                prod = (prod * cur[v]) % mod
            val = sums[idx] + prod
            if val >= mod:
                val -= mod
            sums[idx] = val

    ans = pow(M, pure_count, mod)
    for s in sums:
        ans = (ans * s) % mod

    print(ans)

if __name__ == "__main__":
    main()