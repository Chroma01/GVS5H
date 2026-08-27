import sys
from collections import deque
from array import array

MOD = 998244353


def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = [x - 1 for x in map(int, input().split())]

    indeg = [0] * N
    for p in A:
        indeg[p] += 1

    q = deque(i for i in range(N) if indeg[i] == 0)
    peel_order = []

    while q:
        u = q.popleft()
        peel_order.append(u)
        p = A[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    # acc[v] is the DP vector for v after all already-peeled children
    # have contributed. It is None when its DP is identically one.
    acc = [None] * N

    for u in peel_order:
        dp = acc[u]

        # Convert dp[value] into its prefix sums:
        # pref[value] = sum_{k <= value} dp[k].
        if dp is None:
            pref = array('I', range(1, M + 1))
        else:
            pref = dp
            s = 0
            for j in range(M):
                s += pref[j]
                if s >= MOD:
                    s -= MOD
                pref[j] = s

        p = A[u]
        target = acc[p]

        # Multiply this subtree's prefix contribution into its parent.
        if target is None:
            acc[p] = pref
        else:
            for j in range(M):
                target[j] = (target[j] * pref[j]) % MOD

        acc[u] = None

    # Vertices with positive remaining indegree are precisely cycle vertices.
    # For every cycle, multiply the attached-tree contributions at all cycle
    # vertices, then sum over the common value assigned to that cycle.
    visited = [False] * N
    answer = 1

    for start in range(N):
        if indeg[start] == 0 or visited[start]:
            continue

        cur = start
        cycle_dp = None

        while not visited[cur]:
            visited[cur] = True
            part = acc[cur]

            if part is not None:
                if cycle_dp is None:
                    cycle_dp = part
                else:
                    for j in range(M):
                        cycle_dp[j] = (cycle_dp[j] * part[j]) % MOD

            cur = A[cur]

        if cycle_dp is None:
            component_count = M
        else:
            component_count = sum(cycle_dp) % MOD

        answer = (answer * component_count) % MOD

    print(answer)


if __name__ == "__main__":
    main()