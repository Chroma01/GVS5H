import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)

    for i in range(1, len(data), 2):
        u = data[i]
        v = data[i + 1]
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    del data

    best = 0
    adj_l = adj
    deg_l = deg

    for v in range(1, n + 1):
        d = deg_l[v]

        if d == 0:
            continue

        if d == 1:
            u = adj_l[v][0]
            c = deg_l[u] - 1
            if c > 0:
                kept = c + 2
                if kept > best:
                    best = kept

        elif d == 2:
            a, b = adj_l[v]
            ca = deg_l[a] - 1
            cb = deg_l[b] - 1

            if ca > 0:
                kept = ca + 2
                if kept > best:
                    best = kept

            if cb > 0:
                kept = cb + 2
                if kept > best:
                    best = kept

            if ca > 0 and cb > 0:
                m = ca if ca < cb else cb
                kept = 2 * m + 3
                if kept > best:
                    best = kept

        else:
            caps = [deg_l[u] - 1 for u in adj_l[v] if deg_l[u] > 1]
            m = len(caps)

            if m == 0:
                continue

            if m == 1:
                kept = caps[0] + 2
                if kept > best:
                    best = kept

            elif m == 2:
                c0, c1 = caps
                if c0 < c1:
                    c0, c1 = c1, c0

                kept = c0 + 2
                if kept > best:
                    best = kept

                kept = 2 * c1 + 3
                if kept > best:
                    best = kept

            else:
                caps.sort(reverse=True)
                for k, c in enumerate(caps, 1):
                    kept = 1 + k * (c + 1)
                    if kept > best:
                        best = kept

    sys.stdout.write(str(n - best) + "\n")


if __name__ == "__main__":
    solve()