import sys
from array import array

def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    parent = array('i', [-1]) * n
    left = array('i', [-1]) * n
    right = array('i', [-1]) * n

    # Max Cartesian tree, breaking equal-value ties to the left:
    # an earlier equal value becomes the ancestor of a later equal value.
    stack = []
    for i, x in enumerate(a):
        last = -1
        while stack and a[stack[-1]] < x:
            last = stack.pop()

        if stack:
            p = stack[-1]
            parent[i] = p
            right[p] = i

        if last != -1:
            parent[last] = i
            left[i] = last

        stack.append(i)

    root = stack[0]

    # Iterative DFS order, followed by reverse order, obtains subtree sums.
    order = array('i')
    dfs = [root]
    while dfs:
        v = dfs.pop()
        order.append(v)
        lv = left[v]
        rv = right[v]
        if lv != -1:
            dfs.append(lv)
        if rv != -1:
            dfs.append(rv)

    subsum = a[:]
    for idx in range(n - 1, -1, -1):
        v = order[idx]
        p = parent[v]
        if p != -1:
            subsum[p] += subsum[v]

    # A starting node can initially consume its entire Cartesian subtree except
    # when its only accessible child-side is an equal-valued right child.
    bad = bytearray(n)
    for v in range(n):
        rv = right[v]
        if left[v] == -1 and rv != -1 and a[rv] == a[v]:
            bad[v] = 1

    # up[j][v] is the ancestor after 2^j consecutive traversable tree edges.
    # Edge v -> parent[v] is traversable exactly when subsum[v] > A[parent[v]].
    levels = n.bit_length()
    up = []

    first = array('i', [-1]) * n
    for v in range(n):
        p = parent[v]
        if p != -1 and subsum[v] > a[p]:
            first[v] = p
    up.append(first)

    for _ in range(1, levels):
        prev = up[-1]
        cur = array('i', [-1]) * n
        for v in range(n):
            mid = prev[v]
            if mid != -1:
                cur[v] = prev[mid]
        up.append(cur)

    ans = [0] * n
    for v in range(n):
        if bad[v]:
            ans[v] = a[v]
            continue

        cur = v
        for j in range(levels - 1, -1, -1):
            nxt = up[j][cur]
            if nxt != -1:
                cur = nxt
        ans[v] = subsum[cur]

    print(*ans)

if __name__ == "__main__":
    solve()