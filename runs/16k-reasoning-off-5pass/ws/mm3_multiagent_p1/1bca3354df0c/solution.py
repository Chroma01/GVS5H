import sys
from sys import setrecursionlimit
setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    adj = [[] for _ in range(N)]
    # edges per component, but we can count per vertex and avoid double-count later
    # We'll store edges in a set to count same-color edges, but M up to 2e5, using list is fine.
    edges = []
    for _ in range(M):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))
    
    color = [-1] * N
    components = []  # list of (size_side0, size_side1, same_color_edges)
    
    from collections import deque
    for start in range(N):
        if color[start] != -1:
            continue
        # BFS
        q = deque([start])
        color[start] = 0
        cnt = [1, 0]  # cnt[0], cnt[1]
        same_color_edges = 0
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    cnt[color[v]] += 1
                    q.append(v)
                else:
                    if color[v] == color[u]:
                        same_color_edges += 1
        # same_color_edges counts each intra-side edge twice (once from each endpoint)
        same_color_edges //= 2
        components.append((cnt[0], cnt[1], same_color_edges))
    
    xor_sum = 0
    for a, b, same in components:
        total_possible = a * (a - 1) // 2 + b * (b - 1) // 2
        available = total_possible - same
        xor_sum ^= available
    
    if xor_sum != 0:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == "__main__":
    solve()