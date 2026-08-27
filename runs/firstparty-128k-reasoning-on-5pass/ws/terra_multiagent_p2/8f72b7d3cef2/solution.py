import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n
    stack = []

    # Max Cartesian tree.
    # Equal values are not popped, so an earlier equal value becomes
    # an ancestor of a later equal value.
    for i in range(n):
        last = -1
        while stack and a[stack[-1]] < a[i]:
            last = stack.pop()

        if stack:
            p = stack[-1]
            right[p] = i
            parent[i] = p

        if last != -1:
            left[i] = last
            parent[last] = i

        stack.append(i)

    roots = [i for i in range(n) if parent[i] == -1]

    # Iterative DFS order for subtree sums and top reachable ancestors.
    order = []
    dfs = roots[:]
    while dfs:
        v = dfs.pop()
        order.append(v)
        if left[v] != -1:
            dfs.append(left[v])
        if right[v] != -1:
            dfs.append(right[v])

    sub = [0] * n
    for v in reversed(order):
        s = a[v]
        if left[v] != -1:
            s += sub[left[v]]
        if right[v] != -1:
            s += sub[right[v]]
        sub[v] = s

    # top[v]:
    # Assuming the entire Cartesian subtree of v has been absorbed,
    # this is the highest ancestor whose whole subtree can also be
    # absorbed by repeatedly crossing eligible parent boundaries.
    top = list(range(n))
    for v in order:
        for ch in (left[v], right[v]):
            if ch == -1:
                continue
            if sub[ch] > a[v]:
                top[ch] = top[v]
            else:
                top[ch] = ch

    ans = [0] * n
    for v in range(n):
        initial = a[v]

        # Before crossing an equal-or-larger Cartesian edge, v can fully
        # absorb exactly its direct child subtrees with strictly smaller root.
        if left[v] != -1 and a[left[v]] < a[v]:
            initial += sub[left[v]]
        if right[v] != -1 and a[right[v]] < a[v]:
            initial += sub[right[v]]

        if initial == a[v]:
            ans[v] = a[v]
        else:
            ans[v] = sub[top[v]]

    print(*ans)

if __name__ == "__main__":
    solve()