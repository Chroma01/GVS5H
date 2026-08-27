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
    has_odd_component = False
    odd_odd_components = 0

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

        size = cnt[0] + cnt[1]
        if size & 1:
            has_odd_component = True
        elif (cnt[0] & 1) and (cnt[1] & 1):
            odd_odd_components += 1

    # A maximal position is a complete bipartite graph on one component.
    # If its color classes have sizes A and B, the number of moves made is AB-M.
    #
    # Aoki wins exactly when some possible orientation/merging of the
    # initial components gives AB-M odd.
    if n & 1:
        winning = (m & 1) == 1
    elif has_odd_component:
        # An odd-sized component can be flipped to change the parity of A.
        # Hence AB can be made odd, so AB-M can be odd iff M is even.
        winning = (m & 1) == 0
    else:
        # Every component has even size, so the parity of A is fixed.
        # It is odd precisely for components whose two color classes are odd.
        ab_parity = odd_odd_components & 1
        winning = ab_parity != (m & 1)

    print("Aoki" if winning else "Takahashi")


if __name__ == "__main__":
    solve()