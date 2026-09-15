import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]
    deg = [0] * n

    idx = 1
    for _ in range(n - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2

        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    del data

    getdeg = deg.__getitem__
    best = 3  # minimum valid snowflake has 3 vertices

    for a in adj:
        if best >= n:
            best = n
            break

        l = len(a)
        if l == 0:
            continue

        if l == 1:
            d = deg[a[0]]
            if d >= 2:
                val = d + 1
                if val > best:
                    best = val
            continue

        if l == 2:
            v0 = a[0]
            v1 = a[1]
            d0 = deg[v0]
            d1 = deg[v1]

            if d0 < d1:
                d0, d1 = d1, d0

            if d0 >= 2:
                val = d0 + 1
                if val > best:
                    best = val

                if d1 >= 2:
                    val = 1 + 2 * d1
                    if val > best:
                        best = val
            continue

        a.sort(key=getdeg, reverse=True)

        x = 0
        for v in a:
            d = deg[v]
            if d <= 1:
                break

            x += 1
            val = 1 + x * d
            if val > best:
                best = val

    if best > n:
        best = n

    print(n - best)


if __name__ == "__main__":
    main()