import sys
from bisect import bisect_left, bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; M = data[p+1]; Q = data[p+2]; p += 3
    a = [0]*(M+1); b = [0]*(M+1); ori = [0]*(M+1)  # ori: 0 = up (S<T), 1 = down (S>T)
    for i in range(1, M+1):
        s = data[p]; t = data[p+1]; p += 2
        if s < t:
            a[i] = s; b[i] = t; ori[i] = 0
        else:
            a[i] = t; b[i] = s; ori[i] = 1
    queries = [(data[p+2*k], data[p+2*k+1]) for k in range(Q)]

    # Feasibility characterization (verified by brute force): a set of people is
    # feasible iff no two SAME-orientation intervals cross, where crossing means
    # a_i < a_j < b_i < b_j (or symmetric). Each crossing pair (i,j), i<j, kills
    # exactly the queries with L<=i and R>=j. So with
    #   bad[j] = max{ i<j : persons i,j same orientation and cross },
    # query (L,R) is Yes iff max(bad[L..R]) < L.

    # ---- Type 1: partners with a' < x and b' in (x, y).
    # BIT over coordinate a (prefix queries); each node holds sorted (b,idx) pairs
    # plus an iterative segment tree for range-max over b. Persons are inserted in
    # increasing index order so every stored partner has index < current.
    def solve_type1(idxs):
        bit_pairs = [None]*(N+2)
        for i in idxs:
            node = a[i]
            while node <= N:
                if bit_pairs[node] is None:
                    bit_pairs[node] = [(b[i], i)]
                else:
                    bit_pairs[node].append((b[i], i))
                node += node & (-node)
        seg = [None]*(N+2)
        sz = [0]*(N+2)
        bvals = [None]*(N+2)
        for node in range(1, N+1):
            if bit_pairs[node] is not None:
                lst = bit_pairs[node]
                lst.sort()
                bit_pairs[node] = lst
                bvals[node] = [bb for (bb, _) in lst]
                n = len(lst)
                sz[node] = n
                seg[node] = [0]*(2*n)

        def upd(node, pos, val):
            t = seg[node]; n = sz[node]
            pos += n
            if t[pos] >= val:
                return
            t[pos] = val
            pos >>= 1
            while pos:
                left = t[2*pos]; right = t[2*pos+1]
                t[pos] = left if left >= right else right
                pos >>= 1

        def qry(node, l, r):
            t = seg[node]; n = sz[node]
            l += n; r += n
            res = 0
            while l <= r:
                if l & 1:
                    if t[l] > res: res = t[l]
                    l += 1
                if not (r & 1):
                    if t[r] > res: res = t[r]
                    r -= 1
                l >>= 1; r >>= 1
            return res

        bad_local = [0]*(M+1)
        for i in sorted(idxs):
            x = a[i]; y = b[i]
            best = 0
            node = x - 1
            while node > 0:
                bv = bvals[node]
                if bv:
                    l = bisect_right(bv, x)      # first slot with b > x
                    r = bisect_left(bv, y) - 1   # last slot with b < y
                    if l <= r:
                        v = qry(node, l, r)
                        if v > best: best = v
                node -= node & (-node)
            bad_local[i] = best
            node = x
            while node <= N:
                if bit_pairs[node] is not None:
                    pos = bisect_left(bit_pairs[node], (y, i))
                    upd(node, pos, i)
                node += node & (-node)
        return bad_local

    # ---- Type 2: partners with a' in (x, y) and b' > y.
    # Segment tree over coordinate a (range queries), same inner structure.
    def solve_type2(idxs):
        size = 1
        while size < N+2:
            size <<= 1
        tree_pairs = [None]*(2*size)
        for i in idxs:
            node = a[i] + size
            while node >= 1:
                if tree_pairs[node] is None:
                    tree_pairs[node] = [(b[i], i)]
                else:
                    tree_pairs[node].append((b[i], i))
                node >>= 1
        segv = [None]*(2*size)
        szn = [0]*(2*size)
        bvals = [None]*(2*size)
        for node in range(1, 2*size):
            if tree_pairs[node] is not None:
                lst = tree_pairs[node]
                lst.sort()
                tree_pairs[node] = lst
                bvals[node] = [bb for (bb, _) in lst]
                n = len(lst)
                szn[node] = n
                segv[node] = [0]*(2*n)

        def upd(node, pos, val):
            t = segv[node]; n = szn[node]
            pos += n
            if t[pos] >= val:
                return
            t[pos] = val
            pos >>= 1
            while pos:
                left = t[2*pos]; right = t[2*pos+1]
                t[pos] = left if left >= right else right
                pos >>= 1

        def qry_node(node, l, r):
            t = segv[node]; n = szn[node]
            l += n; r += n
            res = 0
            while l <= r:
                if l & 1:
                    if t[l] > res: res = t[l]
                    l += 1
                if not (r & 1):
                    if t[r] > res: res = t[r]
                    r -= 1
                l >>= 1; r >>= 1
            return res

        def range_query(al, ar, bmin):
            res = 0
            l = al + size; r = ar + size
            while l <= r:
                if l & 1:
                    bv = bvals[l]
                    if bv:
                        pos = bisect_left(bv, bmin)
                        if pos < szn[l]:
                            v = qry_node(l, pos, szn[l]-1)
                            if v > res: res = v
                    l += 1
                if not (r & 1):
                    bv = bvals[r]
                    if bv:
                        pos = bisect_left(bv, bmin)
                        if pos < szn[r]:
                            v = qry_node(r, pos, szn[r]-1)
                            if v > res: res = v
                    r -= 1
                l >>= 1; r >>= 1
            return res

        bad_local = [0]*(M+1)
        for i in sorted(idxs):
            x = a[i]; y = b[i]
            if x + 1 <= y - 1:
                bad_local[i] = range_query(x+1, y-1, y+1)
            node = x + size
            while node >= 1:
                if tree_pairs[node] is not None:
                    pos = bisect_left(tree_pairs[node], (y, i))
                    upd(node, pos, i)
                node >>= 1
        return bad_local

    ups = [i for i in range(1, M+1) if ori[i] == 0]
    downs = [i for i in range(1, M+1) if ori[i] == 1]

    bad = [0]*(M+1)
    for idxs in (ups, downs):
        if not idxs:
            continue
        r1 = solve_type1(idxs)
        r2 = solve_type2(idxs)
        for i in idxs:
            m = r1[i] if r1[i] >= r2[i] else r2[i]
            if m > bad[i]:
                bad[i] = m

    # Sparse table for range max of bad over [L..R].
    arr = bad[1:]
    st = [arr]
    j = 1
    while (1 << j) <= M:
        prev = st[-1]
        length = M - (1 << j) + 1
        half = 1 << (j-1)
        cur = [0]*length
        for i in range(length):
            x = prev[i]; y = prev[i+half]
            cur[i] = x if x >= y else y
        st.append(cur)
        j += 1
    log2 = [0]*(M+2)
    for i in range(2, M+2):
        log2[i] = log2[i >> 1] + 1

    out = []
    for (L, R) in queries:
        if L == R:
            out.append("Yes")
            continue
        length = R - L + 1
        k = log2[length]
        row = st[k]
        i0 = L - 1
        x = row[i0]; y = row[R - (1 << k)]
        mx = x if x >= y else y
        out.append("Yes" if mx < L else "No")
    sys.stdout.write("\n".join(out) + "\n")


main()