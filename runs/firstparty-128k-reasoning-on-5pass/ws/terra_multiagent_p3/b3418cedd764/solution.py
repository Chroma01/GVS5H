import sys
from collections import deque

MOD = 998244353


def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = [x - 1 for x in map(int, input().split())]

    # Peel all non-cycle vertices. Remaining vertices are precisely cycle vertices.
    indeg = [0] * N
    for to in A:
        indeg[to] += 1

    removed = [False] * N
    q = deque(i for i in range(N) if indeg[i] == 0)

    while q:
        v = q.popleft()
        removed[v] = True
        to = A[v]
        indeg[to] -= 1
        if indeg[to] == 0:
            q.append(to)

    # Contract every remaining directed cycle into one component.
    comp = [-1] * N
    seen_cycle = [False] * N
    comp_count = 0

    for start in range(N):
        if not removed[start] and not seen_cycle[start]:
            v = start
            while not seen_cycle[v]:
                seen_cycle[v] = True
                comp[v] = comp_count
                v = A[v]
            comp_count += 1

    # Every non-cycle vertex forms its own component.
    for i in range(N):
        if removed[i]:
            comp[i] = comp_count
            comp_count += 1

    children = [[] for _ in range(comp_count)]
    parent = [-1] * comp_count

    # An edge i -> A[i] means component(i) is a child of component(A[i]).
    for i in range(N):
        u = comp[i]
        v = comp[A[i]]
        if u != v:
            parent[u] = v

    for u in range(comp_count):
        if parent[u] != -1:
            children[parent[u]].append(u)

    roots = [u for u in range(comp_count) if parent[u] == -1]

    sys.setrecursionlimit(1_000_000)

    # Returns dp[value-1]:
    # number of assignments in this component's subtree when its label is value.
    def dfs(u):
        result = None

        for v in children[u]:
            child_dp = dfs(v)

            prefix = 0
            if result is None:
                # Reuse child_dp as the prefix-sum result to save memory.
                for k in range(M):
                    prefix += child_dp[k]
                    if prefix >= MOD:
                        prefix -= MOD
                    child_dp[k] = prefix
                result = child_dp
            else:
                for k in range(M):
                    prefix += child_dp[k]
                    if prefix >= MOD:
                        prefix -= MOD
                    result[k] = (result[k] * prefix) % MOD

        if result is None:
            return [1] * M
        return result

    ans = 1
    for root in roots:
        root_dp = dfs(root)
        ways = sum(root_dp) % MOD
        ans = (ans * ways) % MOD

    print(ans)


if __name__ == "__main__":
    main()