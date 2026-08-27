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
        # capacities: how many leaf-children each neighbor m can provide
        caps = [deg[m] - 1 for m in adj[c] if deg[m] >= 2]
        if not caps:
            continue
        caps.sort(reverse=True)
        cur = 0
        # choose k middles with largest capacities; y = k-th largest capacity
        for k in range(1, len(caps) + 1):
            val = k * (1 + caps[k - 1])  # k middles + k*y leaves
            if val > cur:
                cur = val
        if cur + 1 > best:  # +1 for the center itself
            best = cur + 1

    print(n - best)

main()