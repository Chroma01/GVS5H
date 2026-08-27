import sys

def solve():
    input = sys.stdin.readline
    N = int(input().strip())
    adj = [[] for _ in range(N)]
    for _ in range(N - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
    
    deg = [len(neighbors) for neighbors in adj]
    
    max_kept = 0
    for c in range(N):
        # Collect degrees of neighbors with degree >= 2
        neighbor_degrees = [deg[v] for v in adj[c] if deg[v] >= 2]
        if not neighbor_degrees:
            continue
        neighbor_degrees.sort(reverse=True)
        # For each x from 1 to len(neighbor_degrees)
        for x in range(1, len(neighbor_degrees) + 1):
            y = neighbor_degrees[x - 1] - 1
            if y < 1:
                break  # Since degrees are sorted descending, smaller x will have larger y, so we can break
            kept = 1 + x * (1 + y)
            if kept > max_kept:
                max_kept = kept
    
    print(N - max_kept)

if __name__ == "__main__":
    solve()