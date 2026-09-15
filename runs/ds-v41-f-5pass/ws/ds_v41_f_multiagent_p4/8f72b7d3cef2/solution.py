import sys
from array import array


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    A = [0] * N
    for i in range(N):
        A[i] = int(data[i + 1])
    del data

    # Max Cartesian tree, leftmost-maximum is root of each interval.
    # Tie handling: while stack top value < current value -> pop.
    left = array('i', [-1]) * N
    right = array('i', [-1]) * N
    stack = []
    for i in range(N):
        ai = A[i]
        last = -1
        while stack and A[stack[-1]] < ai:
            last = stack.pop()
        if last != -1:
            left[i] = last
        if stack:
            right[stack[-1]] = i
        stack.append(i)
    root = stack[0]
    del stack

    # Preorder (parent before children).
    order = []
    st = [root]
    while st:
        u = st.pop()
        order.append(u)
        l = left[u]
        r = right[u]
        if l != -1:
            st.append(l)
        if r != -1:
            st.append(r)

    # T[i] = sum of subtree interval of i.
    T = array('q', [0]) * N
    for u in reversed(order):
        s = A[u]
        l = left[u]
        r = right[u]
        if l != -1:
            s += T[l]
        if r != -1:
            s += T[r]
        T[u] = s
    del order

    # reach[i] = topmost ancestor whose whole subtree i can absorb.
    # Climb from child c to parent u iff size after absorbing subtree, T[c], > A[u].
    reach = array('i', [0]) * N
    reach[root] = root
    st = [root]
    while st:
        u = st.pop()
        ru = reach[u]
        au = A[u]
        l = left[u]
        r = right[u]
        if l != -1:
            reach[l] = ru if T[l] > au else l
            st.append(l)
        if r != -1:
            reach[r] = ru if T[r] > au else r
            st.append(r)

    out = []
    for i in range(N):
        # If neither neighbour is strictly smaller, Takahashi cannot move at all.
        if (i > 0 and A[i - 1] < A[i]) or (i < N - 1 and A[i + 1] < A[i]):
            out.append(T[reach[i]])
        else:
            out.append(A[i])

    sys.stdout.write(' '.join(map(str, out)))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()