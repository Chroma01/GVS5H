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
    odd_component_count = 0
    even_component_odd_side_parity = 0

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        count = [1, 0]
        q = deque([start])

        while q:
            v = q.popleft()
            for to in graph[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    count[color[to]] += 1
                    q.append(to)

        size = count[0] + count[1]
        if size & 1:
            odd_component_count += 1
        else:
            # For an even-sized component, both bipartition sides have
            # the same parity, independent of which side received color 0.
            even_component_odd_side_parity ^= count[0] & 1

    if n & 1:
        # A terminal graph is K(x, n-x). For odd n, x(n-x) is always even.
        # Thus the number of remaining moves has parity M.
        first_wins = (m & 1) == 1
    else:
        value = (m + odd_component_count // 2 + even_component_odd_side_parity) & 1
        first_wins = value == 1

    print("Aoki" if first_wins else "Takahashi")


if __name__ == "__main__":
    solve()