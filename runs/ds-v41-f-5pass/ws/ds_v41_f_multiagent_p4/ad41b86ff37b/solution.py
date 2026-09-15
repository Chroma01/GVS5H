import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    adj = [[] for _ in range(n)]

    idx = 1
    for _ in range(n - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    deg = [len(adj[i]) for i in range(n)]

    best = 0

    for c in range(n):
        vals = [deg[m] - 1 for m in adj[c]]
        if not vals:
            continue
        vals.sort(reverse=True)

        for i, y in enumerate(vals):
            if y >= 1:
                cand = 1 + (i + 1) * (y + 1)
                if cand > best:
                    best = cand

    print(n - best)


if __name__ == "__main__":
    main()