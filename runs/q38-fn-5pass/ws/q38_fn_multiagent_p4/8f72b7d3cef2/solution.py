import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    A = list(map(int, it))
    del data, it

    if n == 0:
        sys.stdout.write("\n")
        return

    # Max Cartesian tree.
    # Tie-breaking: pop only while strictly smaller, so earlier equal values
    # become ancestors of later equal values.
    left = [-1] * n
    right = [-1] * n
    st = []

    for i in range(n):
        a = A[i]
        last = -1
        while st and A[st[-1]] < a:
            last = st.pop()
        if st:
            right[st[-1]] = i
        if last != -1:
            left[i] = last
        st.append(i)

    root = st[0]

    # Iterative DFS order: parent appears before children.
    order = []
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        l = left[u]
        r = right[u]
        if l != -1:
            stack.append(l)
        if r != -1:
            stack.append(r)

    # Subtree sums.
    S = A[:]
    for u in reversed(order):
        l = left[u]
        if l != -1:
            S[u] += S[l]
        r = right[u]
        if r != -1:
            S[u] += S[r]

    # top[u] = highest ancestor reachable from u by passable edges.
    # Edge child -> parent is passable iff S[child] > A[parent].
    top = [0] * n
    top[root] = root

    for u in order:
        tu = top[u]
        au = A[u]

        l = left[u]
        if l != -1:
            if S[l] > au:
                top[l] = tu
            else:
                top[l] = l

        r = right[u]
        if r != -1:
            if S[r] > au:
                top[r] = tu
            else:
                top[r] = r

    del left, right, order, stack, st

    # Output in chunks to avoid building one huge list of strings.
    write = sys.stdout.write
    buf = []
    first = True

    A_local = A
    S_local = S
    top_local = top

    for i in range(n):
        ai = A_local[i]
        if (i > 0 and A_local[i - 1] < ai) or (i + 1 < n and A_local[i + 1] < ai):
            buf.append(str(S_local[top_local[i]]))
        else:
            buf.append(str(ai))

        if len(buf) >= 10000:
            if first:
                write(" ".join(buf))
                first = False
            else:
                write(" " + " ".join(buf))
            buf.clear()

    if buf:
        if first:
            write(" ".join(buf))
        else:
            write(" " + " ".join(buf))

    write("\n")


if __name__ == "__main__":
    main()