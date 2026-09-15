import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    if n == 1:
        sys.stdout.write(str(A[0]) + "\n")
        return

    # Build Kruskal reconstruction tree on edges (i,i+1) with weight max(A_i,A_{i+1}).
    mx = [A[i] if A[i] > A[i + 1] else A[i + 1] for i in range(n - 1)]
    order = sorted(range(n - 1), key=mx.__getitem__)

    total = 2 * n  # n leaves + (n-1) internal nodes
    par = list(range(total))
    val = [0] * total
    sm = [0] * total
    lc = [-1] * total
    rc = [-1] * total
    for i in range(n):
        v = A[i]
        val[i] = v
        sm[i] = v

    def find(x, par=par):
        r = x
        while par[r] != r:
            r = par[r]
        while par[x] != r:
            par[x], x = r, par[x]
        return r

    nxt = n
    for i in order:
        w = mx[i]
        a = find(i)
        b = find(i + 1)
        if a != b:
            u = nxt
            nxt += 1
            val[u] = w
            sm[u] = sm[a] + sm[b]
            lc[u] = a
            rc[u] = b
            par[a] = u
            par[b] = u
    root = nxt - 1
    del par, order, mx

    # nearest index to the left / right with A >= A[k] (equal values block)
    leftB = [-1] * n
    st = []
    for k in range(n):
        ak = A[k]
        while st and A[st[-1]] < ak:
            st.pop()
        if st:
            leftB[k] = st[-1]
        st.append(k)
    rightB = [n] * n
    st = []
    for k in range(n - 1, -1, -1):
        ak = A[k]
        while st and A[st[-1]] < ak:
            st.pop()
        if st:
            rightB[k] = st[-1]
        st.append(k)
    del st

    pref = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += A[i]
        pref[i + 1] = s

    f = [0] * total
    res = [0] * n
    pn = []       # current root->node path (node ids)
    nv = []       # negatives of path values (non-decreasing for bisect)
    stack = [root]
    br = bisect_right
    while stack:
        x = stack.pop()
        if x >= 0:
            pn.append(x)
            nv.append(-val[x])
            c = lc[x]
            if c == -1:
                # leaf == original index x
                f[x] = A[x]
                k = x
                L = leftB[k]
                R = rightB[k]
                T0 = A[k] + (pref[k] - pref[L + 1]) + (pref[R] - pref[k + 1])
                if T0 == A[k]:
                    res[k] = T0
                else:
                    j = br(nv, -T0)          # first path node with value < T0
                    res[k] = f[pn[j]]
                pn.pop()
                nv.pop()
            else:
                S = sm[x]
                i = br(nv, -S)               # first path node with value < S
                if i >= len(pn) - 1:
                    f[x] = S
                else:
                    f[x] = f[pn[i]]
                stack.append(-x - 1)         # exit marker
                stack.append(rc[x])
                stack.append(c)
        else:
            pn.pop()
            nv.pop()

    sys.stdout.write(' '.join(map(str, res)))
    sys.stdout.write("\n")

main()