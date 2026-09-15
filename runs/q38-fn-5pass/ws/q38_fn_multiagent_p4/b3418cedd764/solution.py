import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]

    children = [[] for _ in range(N)]
    indeg = [0] * N
    for i, a in enumerate(A):
        children[a].append(i)
        indeg[a] += 1

    # Peel indegree-zero nodes. Remaining nodes are exactly cycle nodes.
    q = [i for i, d in enumerate(indeg) if d == 0]
    head = 0
    in_cycle = [True] * N
    order = []

    while head < len(q):
        u = q[head]
        head += 1
        in_cycle[u] = False
        order.append(u)

        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

    mod = 998244353
    M1 = M + 1
    rng = range(1, M1)

    # dp[u][v] for non-cycle u:
    # number of valid assignments in u's in-tree subtree with x_u <= v.
    # Leaves use this shared base array: dp[v] = v.
    base = list(range(M1))
    dp = [None] * N

    # Process non-cycle nodes bottom-up.
    for u in order:
        ch = children[u]
        l = len(ch)

        if l == 0:
            dp[u] = base

        elif l == 1:
            c = ch[0]
            arr = dp[c]
            dp[c] = None

            # Never modify the shared base array in-place.
            if arr is base:
                arr = arr.copy()

            s = 0
            for v in rng:
                s += arr[v]
                if s >= mod:
                    s -= mod
                arr[v] = s
            arr[0] = 0
            dp[u] = arr

        else:
            first = ch[0]
            arr = dp[first]
            dp[first] = None

            if arr is base:
                arr = arr.copy()

            # Multiply cumulative arrays of the remaining children.
            for idx in range(1, l):
                c = ch[idx]
                child = dp[c]
                dp[c] = None
                for v in rng:
                    arr[v] = (arr[v] * child[v]) % mod

            # Convert exact-value counts to cumulative at-most-v counts.
            s = 0
            for v in rng:
                s += arr[v]
                if s >= mod:
                    s -= mod
                arr[v] = s
            arr[0] = 0
            dp[u] = arr

    del order, indeg, q

    ans = 1
    visited = [False] * N

    # Process each directed cycle component.
    for i in range(N):
        if in_cycle[i] and not visited[i]:
            cur = i
            cycle = []
            while not visited[cur]:
                visited[cur] = True
                cycle.append(cur)
                cur = A[cur]

            # comp[v] = product of attached non-cycle subtree contributions
            # when the common cycle value is v.
            comp = None

            for c in cycle:
                for child in children[c]:
                    if not in_cycle[child]:
                        child_arr = dp[child]
                        dp[child] = None
                        if child_arr is None:
                            continue

                        if comp is None:
                            comp = child_arr
                        else:
                            if comp is base:
                                comp = comp.copy()
                            for v in rng:
                                comp[v] = (comp[v] * child_arr[v]) % mod

            if comp is None:
                comp_sum = M % mod
            elif comp is base:
                comp_sum = (M * (M + 1) // 2) % mod
            else:
                s = 0
                for v in rng:
                    s += comp[v]
                    if s >= mod:
                        s -= mod
                comp_sum = s

            ans = (ans * comp_sum) % mod

    print(ans)


if __name__ == "__main__":
    solve()