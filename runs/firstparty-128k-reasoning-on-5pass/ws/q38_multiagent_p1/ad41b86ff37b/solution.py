import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    adj = [[] for _ in range(n)]
    deg = [0] * n

    for i in range(1, 2 * n - 1, 2):
        u = int(data[i]) - 1
        v = int(data[i + 1]) - 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    del data

    order = [i for i, d in enumerate(deg) if d >= 2]
    order.sort(key=deg.__getitem__, reverse=True)

    cnt = [0] * n
    best = 0

    for v in order:
        dv = deg[v]
        for c in adj[v]:
            k = cnt[c] + 1
            cnt[c] = k
            val = k * dv + 1
            if val > best:
                best = val

    print(n - best)

if __name__ == "__main__":
    main()