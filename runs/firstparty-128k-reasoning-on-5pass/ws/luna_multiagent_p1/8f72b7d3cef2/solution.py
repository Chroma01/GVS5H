import sys

def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n

    stack = []
    for i, x in enumerate(a):
        last = -1
        while stack and a[stack[-1]] < x:
            last = stack.pop()

        if stack:
            right[stack[-1]] = i
            parent[i] = stack[-1]

        if last != -1:
            left[i] = last
            parent[last] = i

        stack.append(i)

    root = stack[0]

    sub_sum = [0] * n
    sub_l = [0] * n
    sub_r = [0] * n

    order = []
    st = [root]
    while st:
        v = st.pop()
        order.append(v)
        if left[v] != -1:
            st.append(left[v])
        if right[v] != -1:
            st.append(right[v])

    for v in reversed(order):
        total = a[v]
        l = v
        r = v

        if left[v] != -1:
            u = left[v]
            total += sub_sum[u]
            l = sub_l[u]

        if right[v] != -1:
            u = right[v]
            total += sub_sum[u]
            r = sub_r[u]

        sub_sum[v] = total
        sub_l[v] = l
        sub_r[v] = r

    inf = 10**30
    stable = [False] * n

    for v in range(n):
        l = sub_l[v]
        r = sub_r[v]

        lv = a[l - 1] if l > 0 else inf
        rv = a[r + 1] if r + 1 < n else inf

        # Non-singleton stable intervals are Cartesian-tree subtrees.
        # Singleton intervals are handled separately because equal adjacent
        # values cannot all simultaneously be represented as subtrees.
        if l != r and sub_sum[v] <= lv and sub_sum[v] <= rv:
            stable[v] = True

    ans = [0] * n

    # For singleton intervals, no absorption is possible exactly when both
    # adjacent slimes (if present) are at least as large.
    singleton_stable = [False] * n
    for i, x in enumerate(a):
        lv = a[i - 1] if i > 0 else inf
        rv = a[i + 1] if i + 1 < n else inf
        if x <= lv and x <= rv:
            singleton_stable[i] = True
            ans[i] = x

    # Traverse from the Cartesian-tree root.  The nearest stable subtree
    # ancestor supplies the answer for each position not stable as a singleton.
    st = [(root, 0)]
    while st:
        v, inherited = st.pop()

        current = inherited
        if stable[v]:
            current = sub_sum[v]

        if not singleton_stable[v]:
            ans[v] = current

        if left[v] != -1:
            st.append((left[v], current))
        if right[v] != -1:
            st.append((right[v], current))

    print(*ans)

if __name__ == "__main__":
    solve()