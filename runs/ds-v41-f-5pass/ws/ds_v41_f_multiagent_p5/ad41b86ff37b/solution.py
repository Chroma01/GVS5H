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

    max_cap = max(deg) - 1
    if max_cap <= 0:
        print(n)
        return

    buckets = [[] for _ in range(max_cap + 1)]
    for v in range(n):
        cap = deg[v] - 1
        if cap > 0:
            buckets[cap].append(v)

    cnt = [0] * n
    max_cnt = 0
    best = 0

    for y in range(max_cap, 0, -1):
        for v in buckets[y]:
            for c in adj[v]:
                cnt[c] += 1
                if cnt[c] > max_cnt:
                    max_cnt = cnt[c]

        if max_cnt > 0:
            kept = 1 + (y + 1) * max_cnt
            if kept > best:
                best = kept

    print(n - best)


if __name__ == "__main__":
    main()