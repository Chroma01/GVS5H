import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])
    M = N * K

    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    del data

    parent = [0] * (M + 1)
    parent[1] = -1
    order = [1]
    pos = 0
    while pos < len(order):
        v = order[pos]
        pos += 1
        for to in adj[v]:
            if parent[to] == 0:
                parent[to] = v
                order.append(to)

    if len(order) != M:
        print("No")
        return

    sz = [1] * (M + 1)
    kept = bytearray(M + 1)
    kept_deg = [0] * (M + 1)

    for v in reversed(order):
        if v == 1:
            continue
        p = parent[v]
        sz[p] += sz[v]
        if sz[v] % K != 0:
            kept[v] = 1
            kept_deg[v] += 1
            kept_deg[p] += 1

    del sz, order

    for d in kept_deg:
        if d > 2:
            print("No")
            return

    del kept_deg

    seen = bytearray(M + 1)
    for i in range(1, M + 1):
        if seen[i]:
            continue

        stack = [i]
        seen[i] = 1
        size = 0

        while stack:
            v = stack.pop()
            size += 1
            pv = parent[v]

            for to in adj[v]:
                if parent[to] == v:
                    if kept[to] and not seen[to]:
                        seen[to] = 1
                        stack.append(to)
                elif pv == to:
                    if kept[v] and not seen[to]:
                        seen[to] = 1
                        stack.append(to)

        if size != K:
            print("No")
            return

    print("Yes")

if __name__ == "__main__":
    main()