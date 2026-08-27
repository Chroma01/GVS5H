import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, K = data[0], data[1]

    if K == 1:
        print("Yes")
        return

    M = N * K
    adj = [[] for _ in range(M)]

    for i in range(2, 2 + 2 * (M - 1), 2):
        u = data[i] - 1
        v = data[i + 1] - 1
        adj[u].append(v)
        adj[v].append(u)
    del data

    parent = [-1] * M
    parent[0] = -2
    order = [0]
    idx = 0
    while idx < len(order):
        v = order[idx]
        idx += 1
        pv = parent[v]
        for to in adj[v]:
            if to == pv:
                continue
            if parent[to] != -1:
                continue
            parent[to] = v
            order.append(to)

    size_mod = [0] * M
    open_state = [False] * M
    complete_state = [False] * M

    for v in reversed(order):
        sm = 1
        open_children = 0
        ok = True

        for to in adj[v]:
            if parent[to] == v:
                if not (open_state[to] or complete_state[to]):
                    ok = False
                    break
                sm = (sm + size_mod[to]) % K
                if open_state[to]:
                    open_children += 1

        if not ok:
            continue

        size_mod[v] = sm
        if sm == 0:
            complete_state[v] = (1 <= open_children <= 2)
        else:
            open_state[v] = (open_children <= 1)

    print("Yes" if complete_state[0] else "No")

if __name__ == "__main__":
    main()