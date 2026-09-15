import sys
from collections import deque

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = [x - 1 for x in data[2:2 + n]]

    indeg = [0] * n
    for p in a:
        indeg[p] += 1

    q = deque([i for i, d in enumerate(indeg) if d == 0])
    dp = [None] * n

    mod = MOD
    rng = range(m)
    base = [i % mod for i in range(1, m + 1)]

    while q:
        u = q.popleft()

        arr = dp[u]
        if arr is None:
            # Leaf: original dp is all 1, so its prefix contribution is 1,2,...,M.
            arr = base.copy()
        else:
            # Convert original dp values into prefix sums in-place.
            s = 0
            for i in rng:
                s += arr[i]
                if s >= mod:
                    s -= mod
                arr[i] = s

        p = a[u]
        par = dp[p]
        if par is None:
            dp[p] = arr
        else:
            for i in rng:
                par[i] = (par[i] * arr[i]) % mod

        dp[u] = None
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    visited = [False] * n
    ans = 1

    for i in range(n):
        if indeg[i] > 0 and not visited[i]:
            cycle = []
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cycle.append(cur)
                cur = a[cur]

            prod = None
            for u in cycle:
                arr = dp[u]
                if arr is not None:
                    if prod is None:
                        prod = arr.copy()
                    else:
                        for j in rng:
                            prod[j] = (prod[j] * arr[j]) % mod
                    dp[u] = None

            if prod is None:
                total = m % mod
            else:
                total = sum(prod) % mod

            ans = (ans * total) % mod

    print(ans)

if __name__ == "__main__":
    main()