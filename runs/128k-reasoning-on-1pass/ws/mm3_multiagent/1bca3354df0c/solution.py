import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    graph = [[] for _ in range(N)]
    for _ in range(M):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * N
    components = []
    for i in range(N):
        if not visited[i]:
            # BFS to find component size
            queue = deque([i])
            visited[i] = True
            size = 1
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if not visited[v]:
                        visited[v] = True
                        size += 1
                        queue.append(v)
            components.append(size)
    
    xor_sum = 0
    for size in components:
        xor_sum ^= size
    
    if xor_sum != 0:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == "__main__":
    solve()