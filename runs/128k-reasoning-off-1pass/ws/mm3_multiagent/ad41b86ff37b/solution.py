import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    adj = [[] for _ in range(N+1)]
    deg = [0] * (N+1)
    for _ in range(N-1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
    
    max_kept = 0
    for c in range(1, N+1):
        lst = []
        for v in adj[c]:
            k = deg[v] - 1
            if k > 0:
                lst.append(k)
        if not lst:
            continue
        lst.sort(reverse=True)
        best = 0
        for i, k in enumerate(lst):
            val = (i+1) * (1 + k)
            if val > best:
                best = val
        kept = 1 + best
        if kept > max_kept:
            max_kept = kept
    
    print(N - max_kept)

if __name__ == "__main__":
    solve()