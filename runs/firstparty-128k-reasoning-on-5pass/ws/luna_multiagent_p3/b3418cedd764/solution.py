import sys
from collections import deque

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = [x - 1 for x in data[2:]]

    children_count = [0] * n
    for p in a:
        children_count[p] += 1

    # dp[v][t] is the product of contributions from already processed
    # non-cycle children of v when x_v = t.
    dp = [[1] * (m + 1) for _ in range(n)]

    queue = deque(i for i in range(n) if children_count[i] == 0)

    while queue:
        v = queue.popleft()
        p = a[v]

        child_dp = dp[v]
        parent_dp = dp[p]

        prefix = 0
        for value in range(1, m + 1):
            prefix += child_dp[value]
            if prefix >= MOD:
                prefix -= MOD
            parent_dp[value] = parent_dp[value] * prefix % MOD

        dp[v] = None
        children_count[p] -= 1
        if children_count[p] == 0:
            queue.append(p)

    # The vertices with positive remaining indegree are exactly the cycle vertices.
    seen = [False] * n
    answer = 1

    for start in range(n):
        if children_count[start] <= 0 or seen[start]:
            continue

        cycle = []
        v = start
        while not seen[v]:
            seen[v] = True
            cycle.append(v)
            v = a[v]

        component_count = 0
        for value in range(1, m + 1):
            ways = 1
            for vertex in cycle:
                ways = ways * dp[vertex][value] % MOD
            component_count += ways
            if component_count >= MOD:
                component_count -= MOD

        answer = answer * component_count % MOD

    print(answer)

if __name__ == "__main__":
    solve()