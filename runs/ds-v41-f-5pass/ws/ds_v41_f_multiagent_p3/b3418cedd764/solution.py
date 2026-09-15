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
    indeg = [0] * N
    for i, a in enumerate(A):
        rev[a].append(i)
        indeg[a] += 1

    q = deque(i for i in range(N) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    is_cycle = [indeg[i] > 0 for i in range(N)]

    children = [None] * N
    for u in range(N):
        if is_cycle[u]:
            children[u] = [c for c in rev[u] if not is_cycle[c]]
        else:
            children[u] = rev[u]

    visited = [False] * N
    cycles = []
    for i in range(N):
        if is_cycle[i] and not visited[i]:
            comp = []
            u = i
            while not visited[u]:
                visited[u] = True
                comp.append(u)
                u = A[u]
            cycles.append(comp)

    cycle_infos = []
    for comp in cycles:
        cycle_infos.append([children[u] for u in comp])

    D = [0] * N
    comp_sum = [0] * len(cycles)

    for v in range(1, M + 1):
        for u in order:
            prod = 1
            for c in children[u]:
                prod = (prod * D[c]) % MOD
            D[u] = (D[u] + prod) % MOD

        for idx, comp_children in enumerate(cycle_infos):
            comp_prod = 1
            for ch in comp_children:
                prod_u = 1
                for c in ch:
                    prod_u = (prod_u * D[c]) % MOD
                comp_prod = (comp_prod * prod_u) % MOD
            comp_sum[idx] = (comp_sum[idx] + comp_prod) % MOD

    ans = 1
    for s in comp_sum:
        ans = (ans * s) % MOD
    print(ans)

if __name__ == "__main__":
    main()