import sys
from collections import deque

def solve():
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * n
    sum_products = 0
    odd_components = 0

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        cnt = [1, 0]
        q = deque([start])

        while q:
            v = q.popleft()
            for to in graph[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    cnt[color[to]] += 1
                    q.append(to)

        sum_products += cnt[0] * cnt[1]
        if (cnt[0] + cnt[1]) & 1:
            odd_components += 1

    if n & 1:
        # Every terminal complete bipartite graph has an even number of edges.
        winning = (m & 1) == 1
    else:
        # odd_components is necessarily even when N is even.
        winning = ((sum_products - m + odd_components // 2) & 1) == 1

    print("Aoki" if winning else "Takahashi")

if __name__ == "__main__":
    solve()