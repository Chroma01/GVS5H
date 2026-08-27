import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    adj = [[] for _ in range(n + 1)]

    idx = 1
    for _ in range(n - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    deg = [len(lst) for lst in adj]

    # Branch vertices must have at least one neighbor other than the center.
    order = [v for v in range(1, n + 1) if deg[v] >= 2]
    order.sort(key=deg.__getitem__, reverse=True)

    cnt = [0] * (n + 1)
    best = 0  # maximum x * (y + 1)

    for v in order:
        d = deg[v]
        for c in adj[v]:
            nv = cnt[c] + 1
            cnt[c] = nv
            val = nv * d
            if val > best:
                best = val

    print(n - best - 1)

if __name__ == "__main__":
    main()