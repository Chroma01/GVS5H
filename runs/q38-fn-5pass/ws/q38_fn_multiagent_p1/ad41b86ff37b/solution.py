import sys


def main():
    input = sys.stdin.buffer.readline
    line = input()
    if not line:
        return

    n = int(line)
    adj = [[] for _ in range(n)]
    deg = [0] * n

    for _ in range(n - 1):
        u, v = input().split()
        u = int(u) - 1
        v = int(v) - 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # deg[v] becomes the capacity of v as a middle vertex:
    # number of possible leaves when its parent/center is excluded.
    deg = [d - 1 for d in deg]

    cap = deg
    adj_local = adj
    best = 0

    for c in range(n):
        adj_c = adj_local[c]
        d = len(adj_c)

        if d == 1:
            a = cap[adj_c[0]]
            if a > 0:
                size = a + 2
                if size > best:
                    best = size

        elif d == 2:
            a = cap[adj_c[0]]
            b = cap[adj_c[1]]
            if a < b:
                a, b = b, a

            if a > 0:
                size = a + 2
                if size > best:
                    best = size

                if b > 0:
                    size = b * 2 + 3
                    if size > best:
                        best = size

        else:
            caps = []
            for nb in adj_c:
                v = cap[nb]
                if v > 0:
                    caps.append(v)

            if caps:
                if len(caps) == 1:
                    size = caps[0] + 2
                    if size > best:
                        best = size
                else:
                    caps.sort(reverse=True)
                    k = 1
                    for v in caps:
                        size = 1 + k * (v + 1)
                        if size > best:
                            best = size
                        k += 1

        if best == n:
            break

    print(n - best)


if __name__ == "__main__":
    main()