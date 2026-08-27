import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    K = next(it)
    M = N * K

    adj = [[] for _ in range(M + 1)]
    for _ in range(M - 1):
        u = next(it)
        v = next(it)
        adj[u].append(v)
        adj[v].append(u)

    parent = [0] * (M + 1)
    parent[1] = -1
    order = []
    stack = [1]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            if parent[to] != 0:
                continue
            parent[to] = v
            stack.append(to)

    if len(order) != M:
        print("No")
        return

    size_mod = [0] * (M + 1)
    full = [False] * (M + 1)
    open_ = [False] * (M + 1)

    for v in reversed(order):
        s = 1 % K
        bad = 0
        b1 = 0
        b2 = 0
        valid = True

        for to in adj[v]:
            if parent[to] != v:
                continue

            r = size_mod[to]
            if r == 0:
                if not full[to]:
                    valid = False
            else:
                if not open_[to]:
                    valid = False
                bad += 1
                if bad == 1:
                    b1 = r
                elif bad == 2:
                    b2 = r

            s += r
            if s >= K:
                s -= K

        size_mod[v] = s

        if not valid:
            continue

        if K == 1:
            full[v] = (bad == 0)
            continue

        if s != 0:
            if bad == 0:
                open_[v] = (s == 1)
            elif bad == 1:
                open_[v] = (s == 1 + b1)

        if s == 0:
            if bad == 1:
                full[v] = (b1 == K - 1)
            elif bad == 2:
                full[v] = (b1 + b2 == K - 1)

    print("Yes" if full[1] else "No")

if __name__ == "__main__":
    solve()