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
    odd_components = 0
    complete_edge_parity = 0

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

        a, b = count

        if (a + b) & 1:
            odd_components += 1

        # Parity of a*b, the edge count after completing this component
        # into K_{a,b}.
        if (a & 1) and (b & 1):
            complete_edge_parity ^= 1

    if odd_components == 0:
        # All terminal graphs have one fixed edge-count parity.
        first_wins = (m & 1) != complete_edge_parity
    elif odd_components == 2:
        # Merge the two odd-order components, choosing its orientation
        # so that the resulting k=0 position is losing.
        first_wins = True
    else:
        # This includes every positive odd-component count except 2.
        # The player wins precisely when the current edge count is odd.
        first_wins = bool(m & 1)

    print("Aoki" if first_wins else "Takahashi")


if __name__ == "__main__":
    solve()