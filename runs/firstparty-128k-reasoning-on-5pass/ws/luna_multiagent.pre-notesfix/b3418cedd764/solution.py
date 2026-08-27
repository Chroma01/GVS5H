import sys
from collections import deque

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = [x - 1 for x in data[2:2 + n]]

    children = [[] for _ in range(n)]
    indeg = [0] * n

    for v, parent in enumerate(a):
        children[parent].append(v)
        indeg[parent] += 1

    # Remove non-cycle vertices. The resulting order is from leaves
    # toward the cycle, so it is suitable for bottom-up tree DP.
    q = deque(i for i in range(n) if indeg[i] == 0)
    removed_order = []

    while q:
        v = q.popleft()
        removed_order.append(v)

        parent = a[v]
        indeg[parent] -= 1
        if indeg[parent] == 0:
            q.append(parent)

    is_cycle = [indeg[i] > 0 for i in range(n)]

    # dp[v][k] = number of valid assignments in the subtree of v
    # such that x_v <= k + 1.
    dp = [None] * n

    # Process leaves first, then their parents.
    for v in removed_order:
        ways_exact = [1] * m

        for u in children[v]:
            child_dp = dp[u]
            for k in range(m):
                ways_exact[k] = ways_exact[k] * child_dp[k] % MOD
            dp[u] = None

        prefix = 0
        for k in range(m):
            prefix += ways_exact[k]
            if prefix >= MOD:
                prefix -= MOD
            ways_exact[k] = prefix

        dp[v] = ways_exact

    answer = 1
    visited = [False] * n

    for start in range(n):
        if not is_cycle[start] or visited[start]:
            continue

        cycle = []
        v = start
        while not visited[v]:
            visited[v] = True
            cycle.append(v)
            v = a[v]

        contribution = [1] * m

        for c in cycle:
            for u in children[c]:
                if is_cycle[u]:
                    continue

                child_dp = dp[u]
                for k in range(m):
                    contribution[k] = contribution[k] * child_dp[k] % MOD
                dp[u] = None

        component_count = sum(contribution) % MOD
        answer = answer * component_count % MOD

    print(answer)


if __name__ == "__main__":
    solve()