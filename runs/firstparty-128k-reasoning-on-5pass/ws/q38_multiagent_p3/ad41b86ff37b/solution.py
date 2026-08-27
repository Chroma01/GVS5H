import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    adj = [[] for _ in range(n)]

    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    max_cap = 0
    for a in adj:
        cap = len(a) - 1
        if cap > max_cap:
            max_cap = cap

    buckets = [[] for _ in range(max_cap + 1)]
    for v, a in enumerate(adj):
        cap = len(a) - 1
        if cap >= 1:
            buckets[cap].append(v)

    cnt = [0] * n
    maxc = 0
    best = 0  # maximum kept vertices excluding the center

    for y in range(max_cap, 0, -1):
        for v in buckets[y]:
            for c in adj[v]:
                nv = cnt[c] + 1
                cnt[c] = nv
                if nv > maxc:
                    maxc = nv

        val = (y + 1) * maxc
        if val > best:
            best = val

    print(n - 1 - best)

if __name__ == "__main__":
    main()