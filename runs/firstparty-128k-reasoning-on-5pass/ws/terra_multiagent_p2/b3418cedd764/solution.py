import sys
from collections import deque
from array import array

MOD = 998244353


def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = [x - 1 for x in map(int, input().split())]

    # Remove non-cycle vertices. Vertices left with positive indegree are on cycles.
    indeg = [0] * N
    for v in range(N):
        indeg[A[v]] += 1

    q = deque(v for v in range(N) if indeg[v] == 0)
    while q:
        v = q.popleft()
        p = A[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    is_cycle = [indeg[v] > 0 for v in range(N)]

    # DSU: merge each directed cycle into one contracted vertex.
    dsu = list(range(N))

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    def union(x, y):
        x = find(x)
        y = find(y)
        if x != y:
            dsu[y] = x

    for v in range(N):
        if is_cycle[v]:
            union(v, A[v])

    # Assign compact IDs to contracted vertices.
    comp_id = {}
    comp_of = [0] * N
    for v in range(N):
        root = find(v) if is_cycle[v] else v
        if root not in comp_id:
            comp_id[root] = len(comp_id)
        comp_of[v] = comp_id[root]

    K = len(comp_id)
    children = [[] for _ in range(K)]
    parent = [-1] * K

    # Each non-contracted edge is a child -> parent relation.
    for v in range(N):
        c = comp_of[v]
        p = comp_of[A[v]]
        if c != p:
            parent[c] = p
            children[p].append(c)

    roots = [v for v in range(K) if parent[v] == -1]

    # Obtain a parent-before-child order, then process it in reverse.
    order = []
    stack = roots[:]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children[v])

    dp = [None] * K
    answer = 1

    # dp[v][k-1] = number of assignments in v's subtree if x_v = k.
    for v in reversed(order):
        cur = array('I', [1]) * M

        for ch in children[v]:
            child_dp = dp[ch]
            prefix = 0
            for i in range(M):
                prefix += child_dp[i]
                if prefix >= MOD:
                    prefix -= MOD
                cur[i] = (cur[i] * prefix) % MOD
            dp[ch] = None

        if parent[v] == -1:
            ways_for_root = sum(cur) % MOD
            answer = (answer * ways_for_root) % MOD
        else:
            dp[v] = cur

    print(answer)


if __name__ == "__main__":
    solve()