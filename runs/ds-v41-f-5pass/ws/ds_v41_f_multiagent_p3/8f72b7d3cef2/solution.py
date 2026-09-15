import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 2)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # Build max Cartesian tree with strict pop (ties: earlier index stays higher).
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    stack = []
    for i in range(1, n + 1):
        ai = A[i]
        last = 0
        while stack and A[stack[-1]] < ai:
            last = stack.pop()
        if stack:
            right[stack[-1]] = i
        if last:
            left[i] = last
        stack.append(i)
    root = stack[0]

    # Iterative pre-order (parent appears before its children).
    order = []
    st = [root]
    while st:
        u = st.pop()
        order.append(u)
        l = left[u]
        if l:
            st.append(l)
        r = right[u]
        if r:
            st.append(r)

    # Subtree sums: reverse pre-order => children before parent.
    S = [0] * (n + 1)
    for u in reversed(order):
        s = A[u]
        l = left[u]
        if l:
            s += S[l]
        r = right[u]
        if r:
            s += S[r]
        S[u] = s

    # top[u] = highest ancestor whose whole subtree can be absorbed.
    # Crossing child c -> parent u possible iff S[c] > A[u] (strict).
    top = [0] * (n + 1)
    top[root] = root
    for u in order:
        tu = top[u]
        au = A[u]
        l = left[u]
        if l:
            top[l] = tu if S[l] > au else l
        r = right[u]
        if r:
            top[r] = tu if S[r] > au else r

    out = []
    append = out.append
    for u in range(1, n + 1):
        l = left[u]
        r = right[u]
        # g[u]: can start u absorb at least one neighbour (strictly smaller)?
        if (l and A[u - 1] < A[u]) or (r and A[u + 1] < A[u]):
            append(str(S[top[u]]))
        else:
            append(str(A[u]))

    sys.stdout.write(' '.join(out) + '\n')

main()