import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    n = next(it)

    adj = [[] for _ in range(n + 1)]
    for u, v in zip(it, it):
        adj[u].append(v)
        adj[v].append(u)

    deg = [0] * (n + 1)
    maxd = 0
    for i in range(1, n + 1):
        d = len(adj[i])
        deg[i] = d
        if d > maxd:
            maxd = d

    buckets = [[] for _ in range(maxd + 1)]
    for i in range(1, n + 1):
        d = deg[i]
        if d >= 2:
            buckets[d].append(i)

    cnt = [0] * (n + 1)
    best = 0

    for d in range(maxd, 1, -1):
        for v in buckets[d]:
            for c in adj[v]:
                cnt[c] += 1
                val = 1 + d * cnt[c]
                if val > best:
                    best = val

    sys.stdout.write(str(n - best))

if __name__ == "__main__":
    main()