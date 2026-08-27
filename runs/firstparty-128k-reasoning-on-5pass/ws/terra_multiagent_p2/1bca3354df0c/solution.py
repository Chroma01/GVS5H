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
    odd_component_count = 0
    fixed_x_parity = 0

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        cnt = [1, 0]
        que = deque([start])

        while que:
            v = que.popleft()
            for to in graph[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    cnt[color[to]] += 1
                    que.append(to)

        size = cnt[0] + cnt[1]
        if size & 1:
            odd_component_count += 1
        else:
            # Both side sizes have equal parity for an even-sized component,
            # so this is unchanged if its bipartition is flipped.
            fixed_x_parity ^= (cnt[0] & 1)

    if n & 1:
        # For odd N, X(N-X) is always even in every terminal K_{X,N-X}.
        first_wins = bool(m & 1)
    elif odd_component_count:
        # The number of odd components is even when N is even.
        first_wins = (odd_component_count % 4 == 2)
    else:
        # The parity of the final complete-bipartite edge count is fixed.
        first_wins = bool(fixed_x_parity ^ (m & 1))

    print("Aoki" if first_wins else "Takahashi")


if __name__ == "__main__":
    solve()