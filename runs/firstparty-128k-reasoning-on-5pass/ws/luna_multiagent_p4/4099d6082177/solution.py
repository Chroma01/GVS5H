import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n_groups, k = data[0], data[1]
    total = n_groups * k

    if k == 1:
        print("Yes")
        return

    adj = [[] for _ in range(total)]
    pos = 2
    for _ in range(total - 1):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        adj[u].append(v)
        adj[v].append(u)

    parent = [-1] * total
    order = [0]
    parent[0] = total

    for v in order:
        for to in adj[v]:
            if to != parent[v]:
                parent[to] = v
                order.append(to)

    # dp[v]:
    #   -1 : impossible
    #    0 : subtree is completely decomposed
    #  1..K-1 : one unfinished path of this many vertices ends at v
    dp = [0] * total

    possible = True

    for v in reversed(order):
        residuals = []

        for to in adj[v]:
            if to == parent[v]:
                continue

            state = dp[to]
            if state == -1:
                possible = False
                break
            if state > 0:
                residuals.append(state)
                if len(residuals) > 2:
                    possible = False
                    break

        if not possible:
            break

        if len(residuals) == 0:
            dp[v] = 1
        elif len(residuals) == 1:
            length = residuals[0] + 1
            dp[v] = 0 if length == k else length
        else:
            if residuals[0] + residuals[1] + 1 != k:
                possible = False
                break
            dp[v] = 0

    if possible and dp[0] == 0:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    solve()