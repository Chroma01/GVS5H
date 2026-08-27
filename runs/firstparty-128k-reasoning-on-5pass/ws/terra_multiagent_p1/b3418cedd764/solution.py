import sys
from collections import deque
from array import array

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    parent = [x - 1 for x in data[2:2 + n]]

    indeg = [0] * n
    for p in parent:
        indeg[p] += 1

    q = deque(i for i in range(n) if indeg[i] == 0)
    removed_order = []

    while q:
        v = q.popleft()
        removed_order.append(v)
        p = parent[v]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    is_cycle = [indeg[i] > 0 for i in range(n)]

    # acc[v] is the product of contributions from all already processed
    # non-cycle children, indexed by the value assigned to v.
    acc = [None] * n

    for v in removed_order:
        cur = acc[v]

        if cur is None:
            # A leaf has DP[value] = 1, whose prefix sums are 1, 2, ..., M.
            pref = array('I', range(1, m + 1))
        else:
            pref = array('I', [0]) * m
            s = 0
            for i, value in enumerate(cur):
                s += value
                if s >= MOD:
                    s -= MOD
                pref[i] = s

        acc[v] = None
        p = parent[v]

        if acc[p] is None:
            acc[p] = pref
        else:
            target = acc[p]
            for i in range(m):
                target[i] = (target[i] * pref[i]) % MOD

    visited = [False] * n
    answer = 1

    for start in range(n):
        if not is_cycle[start] or visited[start]:
            continue

        cycle = []
        v = start
        while not visited[v]:
            visited[v] = True
            cycle.append(v)
            v = parent[v]

        ways = 0
        for value_index in range(m):
            contribution = 1
            for node in cycle:
                if acc[node] is not None:
                    contribution = (contribution * acc[node][value_index]) % MOD
            ways += contribution
            if ways >= MOD:
                ways -= MOD

        answer = (answer * ways) % MOD

    print(answer)

if __name__ == "__main__":
    main()