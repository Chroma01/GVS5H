import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]

    pref = [0] * (n + 1)
    for i, x in enumerate(a):
        pref[i + 1] = pref[i] + x
    total = pref[n]

    # Nearest position on the left with value >= a[i].
    left_ge = [-1] * n
    st = []
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            st.pop()
        if st:
            left_ge[i] = st[-1]
        st.append(i)

    # Nearest position on the right with value >= a[i].
    right_ge = [n] * n
    st = []
    for i in range(n - 1, -1, -1):
        x = a[i]
        while st and a[st[-1]] < x:
            st.pop()
        if st:
            right_ge[i] = st[-1]
        st.append(i)

    # Max Cartesian tree. Equal values are kept in ancestor-descendant
    # order; therefore every parent has value >= every child's value.
    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n
    st = []

    for i, x in enumerate(a):
        last = -1
        while st and a[st[-1]] < x:
            last = st.pop()

        if st:
            right[st[-1]] = i
            parent[i] = st[-1]

        if last != -1:
            left[i] = last
            parent[last] = i

        st.append(i)

    root = st[0]

    # Cartesian-tree preorder and subtree sums.
    order = []
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        if left[u] != -1:
            stack.append(left[u])
        if right[u] != -1:
            stack.append(right[u])

    sub_sum = a[:]
    for u in reversed(order):
        if left[u] != -1:
            sub_sum[u] += sub_sum[left[u]]
        if right[u] != -1:
            sub_sum[u] += sub_sum[right[u]]

    # Binary lifting table for weighted ancestor queries.
    log = n.bit_length()
    up = [parent]
    for k in range(1, log):
        prev = up[-1]
        cur = [-1] * n
        for i in range(n):
            p = prev[i]
            cur[i] = -1 if p == -1 else prev[p]
        up.append(cur)

    # Starting from u, climb while ancestor values are strictly below
    # threshold. The returned node is the highest reachable node.
    def highest_below(u, threshold):
        cur = u
        for k in range(log - 1, -1, -1):
            v = up[k][cur]
            if v != -1 and a[v] < threshold:
                cur = v
        return cur

    # F[u] is the terminal size when the current absorbed interval is
    # exactly the Cartesian subtree rooted at u.
    terminal = [0] * n
    terminal[root] = total

    # Ancestors occur before descendants in order, so terminal[ancestor]
    # is available when processing a descendant.
    for u in order[1:]:
        s = sub_sum[u]
        p = parent[u]

        if p == -1 or a[p] >= s:
            terminal[u] = s
        else:
            v = highest_below(u, s)
            if v == u:
                terminal[u] = s
            else:
                terminal[u] = terminal[v]

    ans = [0] * n

    for i in range(n):
        # Initial closure uses the strict threshold a[i].
        l = left_ge[i] + 1
        r = right_ge[i] - 1
        current = pref[r + 1] - pref[l]

        # No blocker can be absorbed unless the current size is already
        # strictly larger than a[i]. In that case, the initial interval is
        # already terminal.
        if current == a[i]:
            ans[i] = current
            continue

        # At threshold current > a[i], the component containing i is the
        # subtree of the highest ancestor whose value is still < current.
        u = highest_below(i, current)
        ans[i] = terminal[u]

    sys.stdout.write(" ".join(map(str, ans)))


if __name__ == "__main__":
    solve()