import sys


def main():
    it = iter(sys.stdin.buffer.read().split())
    try:
        n = int(next(it))
    except StopIteration:
        return
    A = list(map(int, it))
    del it

    if n == 1:
        sys.stdout.write(str(A[0]) + "\n")
        return

    left = [-1] * n
    right = [-1] * n

    # Max Cartesian tree, tie broken by larger index (later index wins).
    st = []
    push = st.append
    pop = st.pop
    for i in range(n):
        x = A[i]
        last = -1
        while st and A[st[-1]] <= x:
            last = pop()
        if st:
            right[st[-1]] = i
        if last != -1:
            left[i] = last
        push(i)

    root = st[0]

    # Reuse stack for traversal.
    st = [root]
    push = st.append
    pop = st.pop

    # Singleton stable intervals are answers immediately.
    ans = [0] * n
    if A[1] >= A[0]:
        ans[0] = A[0]
    for i in range(1, n - 1):
        x = A[i]
        if A[i - 1] >= x and A[i + 1] >= x:
            ans[i] = x
    if A[n - 2] >= A[n - 1]:
        ans[n - 1] = A[n - 1]

    # Preorder list, then reversed gives a valid postorder.
    order = []
    order_append = order.append
    while st:
        v = pop()
        order_append(v)
        l = left[v]
        if l != -1:
            push(l)
        r = right[v]
        if r != -1:
            push(r)
    del order_append, push, pop

    sub = [0] * n
    L = [0] * n
    R = [0] * n
    stable = bytearray(n)
    n1 = n - 1

    # Bottom-up subtree intervals, sums, and stability.
    for v in reversed(order):
        l = left[v]
        r = right[v]
        s = A[v]
        lv = v
        rv = v
        if l != -1:
            s += sub[l]
            lv = L[l]
        if r != -1:
            s += sub[r]
            rv = R[r]
        sub[v] = s
        L[v] = lv
        R[v] = rv
        if (lv == 0 or A[lv - 1] >= s) and (rv == n1 or A[rv + 1] >= s):
            stable[v] = 1

    del order, L, R

    # Top-down propagation of the deepest stable ancestor sum.
    st = [root]
    cst = [0]
    push_st = st.append
    pop_st = st.pop
    push_c = cst.append
    pop_c = cst.pop

    while st:
        v = pop_st()
        c = pop_c()

        if stable[v]:
            c = sub[v]

        if ans[v] == 0:
            ans[v] = c

        l = left[v]
        if l != -1:
            push_st(l)
            push_c(c)

        r = right[v]
        if r != -1:
            push_st(r)
            push_c(c)

    del push_st, pop_st, push_c, pop_c, st, cst
    del A, left, right, sub, stable

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    main()