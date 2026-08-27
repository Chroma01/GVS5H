import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    A = list(map(int, data[1:1 + N]))
    del data

    left = [-1] * N
    right = [-1] * N
    st = []

    # Build max Cartesian tree with leftmost maximum as the higher tie-break.
    for i, a in enumerate(A):
        last = -1
        while st and A[st[-1]] < a:
            last = st.pop()
        if st:
            right[st[-1]] = i
        if last != -1:
            left[i] = last
        st.append(i)

    root = st[0]

    # Iterative preorder.
    order = []
    st = [root]
    while st:
        v = st.pop()
        order.append(v)
        l = left[v]
        r = right[v]
        if l != -1:
            st.append(l)
        if r != -1:
            st.append(r)

    sum_sub = [0] * N
    L = [0] * N
    R = [0] * N
    stable = bytearray(N)
    INF = 10**18

    # Postorder: subtree sums and intervals; mark stable non-singleton subtrees.
    for v in reversed(order):
        l = left[v]
        r = right[v]
        s = A[v]
        lv = v
        rv = v

        if l != -1:
            s += sum_sub[l]
            lv = L[l]
        if r != -1:
            s += sum_sub[r]
            rv = R[r]

        sum_sub[v] = s
        L[v] = lv
        R[v] = rv

        if l != -1 or r != -1:
            lo = A[lv - 1] if lv > 0 else INF
            ro = A[rv + 1] if rv < N - 1 else INF
            if s <= lo and s <= ro:
                stable[v] = 1

    # Reuse L as best-stable-ancestor sum, R as final answers.
    best = L
    ans = R
    best[root] = 0

    # Top-down: deepest stable ancestor, with singleton-stable override.
    for v in order:
        cur = best[v]
        if stable[v]:
            cur = sum_sub[v]

        av = A[v]
        if (v == 0 or av <= A[v - 1]) and (v == N - 1 or av <= A[v + 1]):
            ans[v] = av
        else:
            ans[v] = cur

        l = left[v]
        r = right[v]
        if l != -1:
            best[l] = cur
        if r != -1:
            best[r] = cur

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

if __name__ == "__main__":
    main()