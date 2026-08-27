import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    adj = [[] for _ in range(N)]
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))
    
    color = [-1] * N
    count0 = 0
    count1 = 0
    for start in range(N):
        if color[start] == -1:
            color[start] = 0
            count0 += 1
            q = deque([start])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = color[u] ^ 1
                        if color[v] == 0:
                            count0 += 1
                        else:
                            count1 += 1
                        q.append(v)
    
    total_possible = count0 * count1
    remaining = total_possible - M
    if remaining % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == "__main__":
    solve()