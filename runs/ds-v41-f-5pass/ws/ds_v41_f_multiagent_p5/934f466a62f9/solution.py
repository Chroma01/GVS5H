import sys
from heapq import nsmallest, nlargest


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    C = 5  # candidate count for each operation subtype

    for _ in range(T):
        N = int(data[pos]); K = int(data[pos + 1]); pos += 2
        X = [0] * N; Y = [0] * N; Z = [0] * N
        M = [0] * N; col = [0] * N
        for i in range(N):
            x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2]); pos += 3
            X[i] = x; Y[i] = y; Z[i] = z
            # baseline color = argmax (ties: prefer X, then Y, then Z)
            if x >= y and x >= z:
                M[i] = x; col[i] = 0
            elif y >= z:
                M[i] = y; col[i] = 1
            else:
                M[i] = z; col[i] = 2

        order = sorted(range(N), key=lambda i: -M[i])
        m2 = 2 * K
        Tset = order[:m2]
        outside = order[m2:]

        tlist = [[], [], []]
        cnt = [0, 0, 0]
        sumM = 0
        for i in Tset:
            sumM += M[i]
            c = col[i]
            cnt[c] += 1
            tlist[c].append(i)

        odd = [c for c in range(3) if cnt[c] & 1]
        if not odd:
            out.append(str(sumM))
            continue

        p, q = odd[0], odd[1]
        r = 3 - p - q
        val = (X, Y, Z)

        def pair_ops(a, b):
            """All cheap operations toggling parities of colors a and b.
            Each op: (cost, tidx, oidx); oidx == -1 means recolor (uses tidx only)."""
            va = val[a]; vb = val[b]
            ta = tlist[a]; tb = tlist[b]
            ops = []
            if ta:  # recolor a -> b
                for i in nsmallest(C, ta, key=lambda i: M[i] - vb[i]):
                    ops.append((M[i] - vb[i], i, -1))
            if tb:  # recolor b -> a
                for i in nsmallest(C, tb, key=lambda i: M[i] - va[i]):
                    ops.append((M[i] - va[i], i, -1))
            if ta and outside:  # swap a out, b in
                ob = nlargest(C, outside, key=lambda j: vb[j])
                for i in nsmallest(C, ta, key=lambda i: M[i]):
                    mi = M[i]
                    for j in ob:
                        ops.append((mi - vb[j], i, j))
            if tb and outside:  # swap b out, a in
                oa = nlargest(C, outside, key=lambda j: va[j])
                for i in nsmallest(C, tb, key=lambda i: M[i]):
                    mi = M[i]
                    for j in oa:
                        ops.append((mi - va[j], i, j))
            return ops

        # Option A: single op toggling the two odd colors {p,q}
        best = min(c for c, _, _ in pair_ops(p, q))

        # Option B: one op on {p,r} plus one on {q,r}, disjoint items
        ops1 = pair_ops(p, r)
        ops2 = pair_ops(q, r)
        ops1.sort()
        ops2.sort()
        for c1, i1, j1 in ops1:
            if c1 >= best:
                break
            for c2, i2, j2 in ops2:
                if c1 + c2 >= best:
                    break
                if i1 == i2:
                    continue
                if j1 != -1 and j1 == i2:
                    continue
                if j2 != -1 and j2 == i1:
                    continue
                if j1 != -1 and j2 != -1 and j1 == j2:
                    continue
                best = c1 + c2

        out.append(str(sumM - best))

    sys.stdout.write("\n".join(out) + "\n")


main()