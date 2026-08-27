import sys
from collections import deque
from array import array

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())
    a = [int(x) - 1 for x in input().split()]

    rev = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in enumerate(a):
        rev[v].append(u)
        indeg[v] += 1

    # Peel all non-cycle vertices.
    q = deque(i for i in range(n) if indeg[i] == 0)
    is_cycle = [True] * n
    order = []

    while q:
        u = q.popleft()
        is_cycle[u] = False
        order.append(u)
        v = a[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    # dp[u][v] = number of assignments in the non-cycle tree rooted at u
    # when x_u = v+1.
    dp = [None] * n

    def tree_contribution(u):
        res = array('I', [1]) * m
        for child in rev[u]:
            if is_cycle[child]:
                continue
            child_dp = dp[child]
            prefix = 0
            for value in range(m):
                prefix += child_dp[value]
                if prefix >= MOD:
                    prefix -= MOD
                res[value] = (res[value] * prefix) % MOD
        return res

    # In the peeling order, every non-cycle child is processed before its parent.
    for u in order:
        dp[u] = tree_contribution(u)

    seen = [False] * n
    answer = 1

    for start in range(n):
        if not is_cycle[start] or seen[start]:
            continue

        cycle = []
        u = start
        while not seen[u]:
            seen[u] = True
            cycle.append(u)
            u = a[u]

        product = array('I', [1]) * m
        for u in cycle:
            contribution = tree_contribution(u)
            for value in range(m):
                product[value] = (product[value] * contribution[value]) % MOD

        component_count = sum(product) % MOD
        answer = (answer * component_count) % MOD

    print(answer)


if __name__ == "__main__":
    solve()