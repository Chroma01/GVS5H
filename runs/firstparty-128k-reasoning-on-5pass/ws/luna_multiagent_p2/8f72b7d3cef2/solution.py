import sys


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n

    # Max Cartesian tree.
    # Popping on <= makes the rightmost occurrence the ancestor among equals.
    stack = []
    for i, value in enumerate(a):
        last = -1
        while stack and a[stack[-1]] <= value:
            last = stack.pop()

        if stack:
            right[stack[-1]] = i
            parent[i] = stack[-1]

        if last != -1:
            left[i] = last
            parent[last] = i

        stack.append(i)

    root = stack[0]

    # Obtain preorder, then process in reverse for bottom-up DP.
    order = []
    st = [root]
    while st:
        v = st.pop()
        order.append(v)
        if left[v] != -1:
            st.append(left[v])
        if right[v] != -1:
            st.append(right[v])

    subtree = [0] * n
    basin = [0] * n

    for v in reversed(order):
        total = a[v]
        strict_mass = a[v]

        lc = left[v]
        rc = right[v]

        if lc != -1:
            total += subtree[lc]
            if a[lc] < a[v]:
                strict_mass += subtree[lc]

        if rc != -1:
            total += subtree[rc]
            if a[rc] < a[v]:
                strict_mass += subtree[rc]

        subtree[v] = total
        basin[v] = strict_mass

    # good[v] means that, after already obtaining the whole subtree of v,
    # the parent of v can be absorbed.
    good = [False] * n
    for v in range(n):
        p = parent[v]
        if p != -1:
            good[v] = subtree[v] > a[p]

    log = n.bit_length()
    jump = [[-1] * n for _ in range(log)]

    for v in range(n):
        if good[v]:
            jump[0][v] = parent[v]

    for k in range(1, log):
        prev = jump[k - 1]
        cur = jump[k]
        for v in range(n):
            x = prev[v]
            if x != -1:
                cur[v] = prev[x]

    ans = [0] * n

    for v in range(n):
        p = parent[v]

        # Before reaching any Cartesian-tree ancestor, v can absorb exactly
        # the region whose maximum is strictly smaller than a[v].
        if p == -1 or basin[v] <= a[p]:
            ans[v] = basin[v]
            continue

        # The first ancestor is reachable using basin[v].
        cur = p

        # Thereafter, each successful transition starts with the complete
        # subtree sum of the current node.
        for k in range(log - 1, -1, -1):
            nxt = jump[k][cur]
            if nxt != -1:
                cur = nxt

        ans[v] = subtree[cur]

    print(*ans)


if __name__ == "__main__":
    solve()