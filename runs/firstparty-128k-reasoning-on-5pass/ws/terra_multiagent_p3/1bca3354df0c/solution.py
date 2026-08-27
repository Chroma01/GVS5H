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
    total_color0 = 0
    component_count = 0
    odd_component_count = 0

    for start in range(n):
        if color[start] != -1:
            continue

        component_count += 1
        color[start] = 0
        q = deque([start])
        cnt = [1, 0]

        while q:
            v = q.popleft()
            for to in graph[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    cnt[color[to]] += 1
                    q.append(to)

        total_color0 += cnt[0]
        if (cnt[0] + cnt[1]) & 1:
            odd_component_count += 1

    # The only flexible situation is even N with odd-sized components.
    # Their count is necessarily even.  The orientation-control game has:
    # - Aoki wins if there are exactly two odd components, or
    # - Aoki wins if the number of even components is odd.
    # Since odd_component_count is even, parity(component_count) is exactly
    # parity(number of even components).
    if n % 2 == 0 and odd_component_count > 0:
        if odd_component_count == 2 or (component_count & 1):
            print("Aoki")
        else:
            print("Takahashi")
        return

    # Otherwise parity of the final complete bipartite graph is invariant.
    final_edge_parity = (total_color0 & 1) * ((n - total_color0) & 1)
    move_parity = final_edge_parity ^ (m & 1)
    print("Aoki" if move_parity else "Takahashi")


if __name__ == "__main__":
    solve()