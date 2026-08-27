import sys

MOD = 998244353
sys.setrecursionlimit(10000)

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = [x - 1 for x in data[2:]]

    rev = [[] for _ in range(n)]
    indeg = [0] * n
    for i, p in enumerate(a):
        rev[p].append(i)
        indeg[p] += 1

    queue = [i for i in range(n) if indeg[i] == 0]
    head = 0
    while head < len(queue):
        v = queue[head]
        head += 1
        p = a[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            queue.append(p)

    in_cycle = [indeg[i] > 0 for i in range(n)]

    def tree_dp(v):
        result = None

        for child in rev[v]:
            if in_cycle[child]:
                continue

            child_dp = tree_dp(child)

            running = 0
            for t in range(m):
                running += child_dp[t]
                if running >= MOD:
                    running -= MOD
                child_dp[t] = running

            if result is None:
                result = child_dp
            else:
                for t in range(m):
                    result[t] = result[t] * child_dp[t] % MOD
                del child_dp

        if result is None:
            result = [1] * m

        return result

    visited_cycle = [False] * n
    answer = 1

    for start in range(n):
        if not in_cycle[start] or visited_cycle[start]:
            continue

        cycle = []
        v = start
        while not visited_cycle[v]:
            visited_cycle[v] = True
            cycle.append(v)
            v = a[v]

        component_dp = None
        for v in cycle:
            current = tree_dp(v)
            if component_dp is None:
                component_dp = current
            else:
                for t in range(m):
                    component_dp[t] = component_dp[t] * current[t] % MOD
                del current

        component_count = sum(component_dp) % MOD
        answer = answer * component_count % MOD

    print(answer)

if __name__ == "__main__":
    solve()