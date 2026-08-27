import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    deg = [0] * (n + 1)

    idx = 1
    for _ in range(n - 1):
        a = data[idx]
        b = data[idx + 1]
        idx += 2
        deg[a] += 1
        deg[b] += 1

    high = [False] * (n + 1)
    high_count = 0
    for i in range(1, n + 1):
        if deg[i] >= 4:
            high[i] = True
            high_count += 1

    if high_count == 0:
        print(-1)
        return

    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        a = data[idx]
        b = data[idx + 1]
        idx += 2
        if high[a] and high[b]:
            adj[a].append(b)
            adj[b].append(a)

    del data

    parent = [0] * (n + 1)
    down = [0] * (n + 1)
    best = [0] * (n + 1)
    max_core = 0

    for s in range(1, n + 1):
        if not high[s] or parent[s] != 0:
            continue

        parent[s] = -1
        stack = [s]
        order = []

        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if v == parent[u]:
                    continue
                if parent[v] == 0:
                    parent[v] = u
                    stack.append(v)

        for u in reversed(order):
            t1 = t2 = t3 = t4 = 0
            max_child_best = 0

            for v in adj[u]:
                if parent[v] == u:
                    val = down[v]

                    if val > t1:
                        t4 = t3
                        t3 = t2
                        t2 = t1
                        t1 = val
                    elif val > t2:
                        t4 = t3
                        t3 = t2
                        t2 = val
                    elif val > t3:
                        t4 = t3
                        t3 = val
                    elif val > t4:
                        t4 = val

                    if best[v] > max_child_best:
                        max_child_best = best[v]

            down[u] = 1 + t1 + t2 + t3
            rooted_at_u = 1 + t1 + t2 + t3 + t4
            best[u] = rooted_at_u if rooted_at_u > max_child_best else max_child_best

            if best[u] > max_core:
                max_core = best[u]

    print(3 * max_core + 2 if max_core > 0 else -1)


if __name__ == "__main__":
    main()