import sys

def solve() -> None:
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    NK = N * K

    # K = 1: every vertex itself is a path of length 1
    if K == 1:
        print("Yes")
        return

    # build adjacency list (1‑based)
    adj = [[] for _ in range(NK + 1)]
    for _ in range(NK - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # ---------- iterative DFS to get parent and order ----------
    parent = [0] * (NK + 1)
    order = []                     # preorder, reversed later gives postorder
    stack = [1]
    parent[1] = -1                  # mark root
    while stack:
        v = stack.pop()
        order.append(v)
        for nb in adj[v]:
            if nb == parent[v]:
                continue
            parent[nb] = v
            stack.append(nb)

    # ---------- DP from leaves upwards ----------
    # dp[v] = -1 : impossible (propagate upwards)
    # dp[v] =  0 : subtree of v is already fully covered by closed paths
    # dp[v] =  x (1 ≤ x < K) : an open segment of length x ends at v
    dp = [0] * (NK + 1)

    for v in reversed(order):       # postorder
        # collect lengths of open parts coming from children
        active = []
        bad = False
        for nb in adj[v]:
            if nb == parent[v]:
                continue
            if dp[nb] == -1:
                bad = True
                break
            if dp[nb] != 0:         # non‑zero means an open segment is waiting
                active.append(dp[nb])
        if bad:
            dp[v] = -1
            continue

        m = len(active)

        if parent[v] == -1:         # ----- root -----
            if m == 0:
                dp[v] = 0           # only possible when K == 1 (handled before)
            elif m == 1:
                dp[v] = 0 if active[0] == K - 1 else -1
            elif m == 2:
                dp[v] = 0 if active[0] + active[1] == K - 1 else -1
            else:
                dp[v] = -1
        else:                       # ----- non‑root -----
            if m == 0:
                dp[v] = 1           # start a new open segment of length 1
            elif m == 1:
                x = active[0]
                if x == K - 1:
                    dp[v] = 0      # the path finishes here
                elif x < K - 1:
                    dp[v] = x + 1   # continue the open segment
                else:
                    dp[v] = -1
            elif m == 2:
                dp[v] = 0 if active[0] + active[1] == K - 1 else -1
            else:
                dp[v] = -1

    print("Yes" if dp[1] == 0 else "No")


if __name__ == "__main__":
    solve()