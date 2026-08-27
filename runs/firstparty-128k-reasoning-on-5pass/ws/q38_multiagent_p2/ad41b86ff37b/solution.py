import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    adj = [[] for _ in range(n)]
    deg = [0] * n

    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    del data

    best = 0

    for c in range(n):
        lst = adj[c]
        m = len(lst)

        if m == 0:
            continue

        if m == 1:
            d = deg[lst[0]]
            if d >= 2 and d > best:
                best = d
            continue

        if m == 2:
            d0 = deg[lst[0]]
            d1 = deg[lst[1]]
            if d0 > d1:
                d0, d1 = d1, d0

            if d0 >= 2:
                v = d0 * 2
                if v > best:
                    best = v

            if d1 > d0 and d1 >= 2:
                if d1 > best:
                    best = d1
            continue

        vals = [deg[v] for v in lst]
        vals.sort()

        i = 0
        while i < m:
            d = vals[i]
            if d >= 2:
                v = d * (m - i)
                if v > best:
                    best = v
            i += 1
            while i < m and vals[i] == d:
                i += 1

    print(n - (best + 1))

if __name__ == "__main__":
    main()