import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    A = list(map(int, it))
    del data, it

    # Official input is valid; this only makes the code robust.
    if len(A) > n:
        A = A[:n]
    elif len(A) < n:
        n = len(A)

    if n == 0:
        return

    # Build a max Cartesian tree.
    # Heap property: parent value >= child value.
    # Tie-breaking: pop only strictly smaller values, so equal values form
    # a right chain and the leftmost maximum becomes the root.
    left = [-1] * n
    right = [-1] * n
    st = []

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
    del st

    # Preorder list: every parent appears before its children.
    order = [root]
    idx = 0
    while idx < len(order):
        v = order[idx]
        idx += 1

        lc = left[v]
        if lc != -1:
            order.append(lc)

        rc = right[v]
        if rc != -1:
            order.append(rc)

    # Subtree sums.
    sumv = [0] * n
    for v in reversed(order):
        s = A[v]

        lc = left[v]
        if lc != -1:
            s += sumv[lc]

        rc = right[v]
        if rc != -1:
            s += sumv[rc]

        sumv[v] = s

    # Reuse sumv:
    #   before processing v, sumv[v] stores the sum of the topmost reachable
    #   ancestor subtree for v;
    #   after processing v, sumv[v] stores the final answer for v.
    #
    # For a child c of v:
    #   if sumv[c] > A[v], c can climb to v and inherits v's top_sum;
    #   otherwise c's top_sum remains its own subtree sum.
    for v in order:
        top_sum = sumv[v]
        av = A[v]

        lc = left[v]
        if lc != -1 and sumv[lc] > av:
            sumv[lc] = top_sum

        rc = right[v]
        if rc != -1 and sumv[rc] > av:
            sumv[rc] = top_sum

        # A node can absorb its whole Cartesian subtree iff it is a leaf,
        # or it has an adjacent original slime strictly smaller than itself.
        # A smaller adjacent slime cannot be an ancestor because of the heap
        # property, hence it lies inside the subtree.
        if (
            (lc == -1 and rc == -1)
            or (v > 0 and A[v - 1] < av)
            or (v + 1 < n and A[v + 1] < av)
        ):
            sumv[v] = top_sum
        else:
            sumv[v] = av

    del left, right, order, A

    write = sys.stdout.write
    out = []
    first = True

    for x in sumv:
        out.append(str(x))
        if len(out) >= 10000:
            if first:
                write(" ".join(out))
                first = False
            else:
                write(" ")
                write(" ".join(out))
            out.clear()

    if out:
        if first:
            write(" ".join(out))
        else:
            write(" ")
            write(" ".join(out))

    write("\n")


if __name__ == "__main__":
    solve()