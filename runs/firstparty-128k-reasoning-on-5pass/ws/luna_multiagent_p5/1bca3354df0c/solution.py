import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * n
    sum_color_zero = 0
    has_odd_component = False

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        queue = deque([start])
        cnt = [1, 0]

        while queue:
            v = queue.popleft()
            for to in graph[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    cnt[color[to]] += 1
                    queue.append(to)

        if (cnt[0] + cnt[1]) % 2 == 1:
            has_odd_component = True
        sum_color_zero += cnt[0]

    if n % 2 == 1:
        first_wins = (m % 2 == 1)
    elif has_odd_component:
        first_wins = True
    else:
        first_wins = ((m + sum_color_zero) % 2 == 1)

    print("Aoki" if first_wins else "Takahashi")

if __name__ == "__main__":
    solve()