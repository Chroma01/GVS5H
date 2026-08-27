import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]

    indeg = [0] * N
    for p in A:
        indeg[p] += 1

    in_cycle = [True] * N
    queue = [i for i in range(N) if indeg[i] == 0]
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        in_cycle[u] = False
        p = A[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            queue.append(p)

    children = [[] for _ in range(N)]
    for c in range(N):
        if not in_cycle[c]:
            children[A[c]].append(c)

    child_count = [0] * N
    for u in range(N):
        if not in_cycle[u]:
            child_count[u] = len(children[u])

    queue = [u for u in range(N) if not in_cycle[u] and child_count[u] == 0]
    head = 0
    order = []
    while head < len(queue):
        u = queue[head]
        head += 1
        order.append(u)
        p = A[u]
        if not in_cycle[p]:
            child_count[p] -= 1
            if child_count[p] == 0:
                queue.append(p)

    seen = [False] * N
    cycle_attached = []
    for i in range(N):
        if in_cycle[i] and not seen[i]:
            cur = i
            attached = []
            while not seen[cur]:
                seen[cur] = True
                attached.extend(children[cur])
                cur = A[cur]
            cycle_attached.append(attached)

    g = [0] * N
    totals = [0] * len(cycle_attached)
    mod = MOD
    cycle_count = len(cycle_attached)

    for _ in range(M):
        for u in order:
            prod = 1
            for c in children[u]:
                prod = (prod * g[c]) % mod
            val = g[u] + prod
            if val >= mod:
                val -= mod
            g[u] = val

        for idx in range(cycle_count):
            prod = 1
            for c in cycle_attached[idx]:
                prod = (prod * g[c]) % mod
            val = totals[idx] + prod
            if val >= mod:
                val -= mod
            totals[idx] = val

    ans = 1
    for t in totals:
        ans = (ans * t) % mod
    print(ans)

if __name__ == "__main__":
    main()