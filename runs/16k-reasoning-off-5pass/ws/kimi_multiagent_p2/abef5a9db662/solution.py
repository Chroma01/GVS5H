import sys
import random
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    contests = []
    for _ in range(N):
        L = data[p]; R = data[p+1]; p += 2
        contests.append((L, R))
    Q = data[p]; p += 1
    queries = data[p:p+Q]

    sys.setrecursionlimit(1 << 22)

    # Treap node arrays (node 0 = null)
    key = [0]          # breakpoint x
    off = [0]          # offset: F(x) = x + off on [key, next key)
    pri = [0]
    lazy = [0]
    lc = [0]
    rc = [0]

    def new_node(k, o):
        key.append(k)
        off.append(o)
        pri.append(random.getrandbits(30))
        lazy.append(0)
        lc.append(0)
        rc.append(0)
        return len(key) - 1

    def push(t):
        v = lazy[t]
        if v:
            off[t] += v
            l = lc[t]; r = rc[t]
            if l: lazy[l] += v
            if r: lazy[r] += v
            lazy[t] = 0

    def split(t, k):
        # returns (l, r): l has keys < k, r has keys >= k
        if not t:
            return (0, 0)
        push(t)
        if key[t] < k:
            a, b = split(rc[t], k)
            rc[t] = a
            return (t, b)
        else:
            a, b = split(lc[t], k)
            lc[t] = b
            return (a, t)

    def merge(a, b):
        if not a or not b:
            return a or b
        if pri[a] < pri[b]:
            push(a)
            rc[a] = merge(rc[a], b)
            return a
        else:
            push(b)
            lc[b] = merge(a, lc[b])
            return b

    INF = 1 << 62

    def lower_bound_val(t, v):
        # smallest key k such that k + off(k) >= v; INF if none
        # Valid because F(x) = x + off(x) is globally non-decreasing.
        res = INF
        while t:
            push(t)
            if key[t] + off[t] >= v:
                res = key[t]
                t = lc[t]
            else:
                t = rc[t]
        return res

    # initial treap: single breakpoint at x=1 with offset 0
    root = new_node(1, 0)

    for L, R in contests:
        a = lower_bound_val(root, L)
        if a == INF:
            continue  # F(x) < L for all x, no increment anywhere
        b = lower_bound_val(root, R + 1)  # first key with F >= R+1; increment range is [a, b)
        if a == b:
            continue
        t1, t3 = split(root, b)
        t1, t2 = split(t1, a)
        if t2:
            lazy[t2] += 1
        root = merge(merge(t1, t2), t3)

    # in-order traversal to sorted breakpoint arrays
    xs = []
    os_ = []
    stack = []
    t = root
    while stack or t:
        while t:
            push(t)
            stack.append(t)
            t = lc[t]
        t = stack.pop()
        xs.append(key[t])
        os_.append(off[t])
        t = rc[t]

    out = []
    for X in queries:
        i = bisect_right(xs, X) - 1
        out.append(str(X + os_[i]))
    sys.stdout.write("\n".join(out) + "\n")

main()