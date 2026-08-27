import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = [x - 1 for x in map(int, input().split())]

    indeg = [0] * N
    for v in A:
        indeg[v] += 1

    queue = [i for i in range(N) if indeg[i] == 0]
    order = []

    for v in queue:
        order.append(v)
        to = A[v]
        indeg[to] -= 1
        if indeg[to] == 0:
            queue.append(to)

    is_cycle = [indeg[i] > 0 for i in range(N)]

    children = [[] for _ in range(N)]
    for v in range(N):
        if not is_cycle[v]:
            children[A[v]].append(v)

    dp = [None] * N

    # The peeling order goes from leaves toward the cycles,
    # so children are processed before their parents.
    for v in order:
        cur = [1] * (M + 1)
        first = True

        for u in children[v]:
            arr = dp[u]
            s = 0

            if first:
                for k in range(1, M + 1):
                    s += arr[k]
                    if s >= MOD:
                        s -= MOD
                    cur[k] = s
                first = False
            else:
                for k in range(1, M + 1):
                    s += arr[k]
                    if s >= MOD:
                        s -= MOD
                    cur[k] = cur[k] * s % MOD

        dp[v] = cur

    answer = 1
    seen = [False] * N

    for start in range(N):
        if not is_cycle[start] or seen[start]:
            continue

        cycle = []
        v = start
        while not seen[v]:
            seen[v] = True
            cycle.append(v)
            v = A[v]

        contribution = [1] * (M + 1)

        for v in cycle:
            for u in children[v]:
                arr = dp[u]
                s = 0
                for k in range(1, M + 1):
                    s += arr[k]
                    if s >= MOD:
                        s -= MOD
                    contribution[k] = contribution[k] * s % MOD

        component_answer = sum(contribution[1:]) % MOD
        answer = answer * component_answer % MOD

    print(answer)

if __name__ == "__main__":
    solve()