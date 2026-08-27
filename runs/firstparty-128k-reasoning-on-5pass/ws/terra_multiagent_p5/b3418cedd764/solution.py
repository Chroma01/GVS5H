import sys
from collections import deque
from array import array

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    to = [x - 1 for x in data[2:2 + n]]

    # Remove all non-cycle vertices by indegree peeling.
    indeg = [0] * n
    for v in to:
        indeg[v] += 1

    alive = [True] * n
    q = deque(i for i in range(n) if indeg[i] == 0)

    while q:
        v = q.popleft()
        alive[v] = False
        p = to[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    # Contract every remaining directed cycle into one component.
    comp = [-1] * n
    roots = []
    comp_count = 0

    for start in range(n):
        if alive[start] and comp[start] == -1:
            cur = start
            while comp[cur] == -1:
                comp[cur] = comp_count
                cur = to[cur]
            roots.append(comp_count)
            comp_count += 1

    # Every non-cycle vertex is its own component.
    for i in range(n):
        if comp[i] == -1:
            comp[i] = comp_count
            comp_count += 1

    # Build the contracted reverse forest: child -> parent.
    parent = [-1] * comp_count
    children = [[] for _ in range(comp_count)]

    for i in range(n):
        u = comp[i]
        v = comp[to[i]]
        if u != v:
            parent[u] = v
            children[v].append(u)

    # Bottom-up DP.
    # dp[u][value-1] is the number of assignments in u's subtree
    # when component u has the given value.
    remaining_children = [len(ch) for ch in children]
    q = deque(i for i in range(comp_count) if remaining_children[i] == 0)
    dp = [None] * comp_count

    answer = 1

    while q:
        u = q.popleft()

        if dp[u] is None:
            # Leaf: it may take any fixed value in exactly one way.
            dp[u] = array('I', [1]) * m

        p = parent[u]

        if p == -1:
            # A cycle component is a root of one connected component.
            total = 0
            for x in dp[u]:
                total += x
                if total >= MOD:
                    total -= MOD
            answer = (answer * total) % MOD
            dp[u] = None
            continue

        if dp[p] is None:
            dp[p] = array('I', [1]) * m

        child_dp = dp[u]
        parent_dp = dp[p]

        # For parent value v, this child contributes:
        # sum(child_dp[0 : v]).
        prefix = 0
        for j in range(m):
            prefix += child_dp[j]
            if prefix >= MOD:
                prefix -= MOD
            parent_dp[j] = (parent_dp[j] * prefix) % MOD

        dp[u] = None
        remaining_children[p] -= 1
        if remaining_children[p] == 0:
            q.append(p)

    print(answer)

if __name__ == "__main__":
    main()