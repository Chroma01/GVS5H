import sys
from collections import deque
from array import array

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = [x - 1 for x in data[2:]]

    children = [[] for _ in range(n)]
    indeg = [0] * n
    for v, p in enumerate(a):
        children[p].append(v)
        indeg[p] += 1

    q = deque(i for i in range(n) if indeg[i] == 0)
    removed_order = []

    while q:
        v = q.popleft()
        removed_order.append(v)
        p = a[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    is_cycle = [x > 0 for x in indeg]
    dp = [None] * n
    width = m + 1

    # Process all non-cycle vertices from leaves toward the cycles.
    for v in removed_order:
        cur = array('I', [1]) * width

        for ch in children[v]:
            child_dp = dp[ch]
            pref = 0
            for k in range(1, width):
                pref += child_dp[k]
                if pref >= MOD:
                    pref -= MOD
                cur[k] = (cur[k] * pref) % MOD
            dp[ch] = None

        dp[v] = cur

    answer = 1
    seen = [False] * n

    for start in range(n):
        if not is_cycle[start] or seen[start]:
            continue

        cycle = []
        v = start
        while not seen[v]:
            seen[v] = True
            cycle.append(v)
            v = a[v]

        component = [1] * width

        for cv in cycle:
            for ch in children[cv]:
                if is_cycle[ch]:
                    continue

                child_dp = dp[ch]
                pref = 0
                for k in range(1, width):
                    pref += child_dp[k]
                    if pref >= MOD:
                        pref -= MOD
                    component[k] = (component[k] * pref) % MOD
                dp[ch] = None

        component_total = sum(component[1:]) % MOD
        answer = (answer * component_total) % MOD

    print(answer)

if __name__ == "__main__":
    solve()