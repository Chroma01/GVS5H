import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    best = 0
    for c in range(1, n + 1):
        # neighbor degrees, descending; only degrees >= 2 can serve as middle vertices
        ds = sorted((deg[v] for v in adj[c]), reverse=True)
        best_c = 0
        for i, d in enumerate(ds):
            if d < 2:
                break
            # y = d - 1 leaves per middle vertex; i+1 neighbors have deg >= d
            val = d * (i + 1)
            if val > best_c:
                best_c = val
        kept = 1 + best_c
        if kept > best:
            best = kept

    print(n - best)

main()