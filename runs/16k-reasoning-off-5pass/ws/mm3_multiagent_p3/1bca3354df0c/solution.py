import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * n
    xor_sum = 0
    for start in range(n):
        if color[start] != -1:
            continue
        # BFS/DFS to color component
        color[start] = 0
        queue = deque([start])
        cnt0 = 1
        cnt1 = 0
        while queue:
            u = queue.popleft()
            cu = color[u]
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - cu
                    if color[v] == 0:
                        cnt0 += 1
                    else:
                        cnt1 += 1
                    queue.append(v)
        moves = cnt0 * (cnt0 - 1) // 2 + cnt1 * (cnt1 - 1) // 2
        xor_sum ^= moves
    if xor_sum != 0:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == "__main__":
    solve()