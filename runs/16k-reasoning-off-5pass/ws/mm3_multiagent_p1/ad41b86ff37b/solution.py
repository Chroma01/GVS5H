import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
    degree = [0] * (N + 1)
    for i in range(1, N + 1):
        degree[i] = len(adj[i])
    max_kept = 0
    for c in range(1, N + 1):
        leaves = []
        for b in adj[c]:
            leaf = degree[b] - 1
            if leaf >= 1:
                leaves.append(leaf)
        if not leaves:
            continue
        leaves.sort(reverse=True)
        for i, y in enumerate(leaves):
            x = i + 1
            total = 1 + x + x * y
            if total > max_kept:
                max_kept = total
    ans = N - max_kept
    print(ans)

if __name__ == "__main__":
    solve()