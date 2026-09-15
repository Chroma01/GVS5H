import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # Max Cartesian tree with leftmost-maximum tie-break (strict '<' pop).
    left = [-1] * n
    right = [-1] * n
    par = [-1] * n
    stk = []
    for i in range(n):
        ai = A[i]
        last = -1
        while stk and A[stk[-1]] < ai:
            last = stk.pop()
        if last != -1:
            left[i] = last
            par[last] = i
        if stk:
            right[stk[-1]] = i
            par[i] = stk[-1]
        stk.append(i)
    root = stk[0]

    # Iterative preorder: parent always before its descendants.
    order = []
    stack = [root]
    push = order.append
    while stack:
        v = stack.pop()
        push(v)
        l = left[v]
        if l != -1:
            stack.append(l)
        r = right[v]
        if r != -1:
            stack.append(r)

    # Subtree sums: reversed preorder => descendants before ancestors.
    sub = A[:]
    for idx in range(n - 1, -1, -1):
        v = order[idx]
        p = par[v]
        if p != -1:
            sub[p] += sub[v]

    # Top-down reach: up[v] = highest ancestor v can climb to.
    up = [0] * n
    for v in order:
        p = par[v]
        if p == -1:
            up[v] = v
        elif sub[v] > A[p]:
            up[v] = up[p]
        else:
            up[v] = v

    out = []
    for i in range(n):
        ai = A[i]
        if (i > 0 and A[i - 1] < ai) or (i < n - 1 and A[i + 1] < ai):
            out.append(sub[up[i]])
        else:
            out.append(ai)
    sys.stdout.write(' '.join(map(str, out)) + '\n')

main()