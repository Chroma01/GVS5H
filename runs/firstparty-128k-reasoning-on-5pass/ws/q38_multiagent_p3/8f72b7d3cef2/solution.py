import sys
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = list(map(int, it))
    if len(A) > N:
        A = A[:N]
    del data, it

    # Prefix sums, later reused as the subtree-sum array.
    P = [0] * (N + 1)
    s = 0
    for i in range(N):
        s += A[i]
        P[i + 1] = s

    # S0[i] = sum of the first absorbable segment around i.
    # First store previous greater-or-equal boundary, then replace by the sum.
    S0 = [0] * N
    st = [0] * N

    top = -1
    for i in range(N):
        a = A[i]
        while top >= 0 and A[st[top]] < a:
            top -= 1
        S0[i] = st[top] if top >= 0 else -1
        top += 1
        st[top] = i

    top = -1
    for i in range(N - 1, -1, -1):
        a = A[i]
        while top >= 0 and A[st[top]] < a:
            top -= 1
        nxt = st[top] if top >= 0 else N
        prev = S0[i]
        S0[i] = P[nxt] - P[prev + 1]
        top += 1
        st[top] = i

    # Strict max Cartesian tree: pop while strictly smaller.
    left = [-1] * N
    right = [-1] * N
    parent = [-1] * N
    top = -1
    for i in range(N):
        a = A[i]
        last = -1
        while top >= 0 and A[st[top]] < a:
            last = st[top]
            top -= 1
        if top >= 0:
            p = st[top]
            right[p] = i
            parent[i] = p
        if last != -1:
            left[i] = last
            parent[last] = i
        top += 1
        st[top] = i
    root = st[0]

    # Reuse prefix-sum list for subtree sums.
    subsum = P
    del P
    subsum[:N] = A

    # DFS preorder of the Cartesian tree.
    order = [0] * N
    ord_len = 0
    top = 0
    st[0] = root
    while top >= 0:
        u = st[top]
        top -= 1
        order[ord_len] = u
        ord_len += 1
        r = right[u]
        l = left[u]
        if r != -1:
            top += 1
            st[top] = r
        if l != -1:
            top += 1
            st[top] = l

    del left, right

    # Subtree sums by adding each node to its parent in reverse preorder.
    for u in reversed(order):
        p = parent[u]
        if p != -1:
            subsum[p] += subsum[u]

    total = subsum[root]
    max_root_val = A[root]

    # Reuse the stack list as the current root-to-node path.
    path = st
    path_neg = [0] * N
    depth = 0
    br = bisect_right

    for u in order:
        p = parent[u]

        # Maintain the current path in the DFS preorder.
        while depth and path[depth - 1] != p:
            depth -= 1
        au = A[u]
        path[depth] = u
        path_neg[depth] = -au
        depth += 1

        # Compute nearest stable ancestor sum for u.
        # After this, subsum[u] stores that nearest stable sum.
        su = subsum[u]
        if p == -1:
            cur = su
            ap = 0
        else:
            ap = A[p]
            cur = subsum[p]
            if su <= ap:
                cur = su
        subsum[u] = cur

        s0 = S0[u]
        if s0 > au:
            if s0 > max_root_val:
                S0[u] = total
            elif p == -1 or s0 <= ap:
                # The highest ancestor with value < s0 is u itself.
                S0[u] = subsum[u]
            else:
                # First ancestor with A[ancestor] < s0.
                pos = br(path_neg, -s0, 0, depth)
                anc = path[pos]
                S0[u] = subsum[anc]
        else:
            S0[u] = au

    del A, parent, subsum, order, path, path_neg, st
    sys.stdout.write(' '.join(map(str, S0)))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()