import sys
import math
from bisect import bisect_right
from itertools import accumulate
from operator import itemgetter


def main():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    try:
        N = next(it)
    except StopIteration:
        return

    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]
    K = next(it)

    Xs = [0] * K
    Ys = [0] * K
    for i in range(K):
        Xs[i] = next(it)
        Ys[i] = next(it)
    del it

    prefA = [0]
    prefA.extend(accumulate(A))
    prefB = [0]
    prefB.extend(accumulate(B))

    # Exact integer version of int(N * sqrt(2 / K)) + 1.
    S = math.isqrt((2 * N * N) // K) + 1
    if S > N:
        S = N
    if S < 1:
        S = 1

    nb = (N + S - 1) // S

    block_orig = []
    block_vals = []
    block_pref = []
    for b in range(nb):
        start = b * S
        end = min(N, start + S)
        seg = A[start:end]
        block_orig.append(seg)

        vals = sorted(seg)
        block_vals.append(vals)

        pref = [0]
        pref.extend(accumulate(vals))
        block_pref.append(pref)

    full_count = [0] * K
    max_y_for_c = [0] * (nb + 1)
    qbyY = [[] for _ in range(N + 1)]
    partial = [[] for _ in range(nb)]

    for i in range(K):
        X = Xs[i]
        Y = Ys[i]
        c = X // S
        L = X % S

        full_count[i] = c
        if Y > max_y_for_c[c]:
            max_y_for_c[c] = Y

        qbyY[Y].append(i)

        if L:
            partial[c].append((Y, L, i))

    # max_y_full[b] = max Y among queries for which block b is a full block.
    max_y_full = [0] * nb
    suf = 0
    for b in range(nb - 1, -1, -1):
        if max_y_for_c[b + 1] > suf:
            suf = max_y_for_c[b + 1]
        max_y_full[b] = suf

    G = [0] * K
    br = bisect_right
    B_list = B
    qby = qbyY
    fc = full_count

    # Full A-blocks: sweep B for each block up to its maximum needed Y.
    for b in range(nb):
        maxy = max_y_full[b]
        if maxy == 0:
            continue

        vals = block_vals[b]
        m = len(vals)
        total = 0

        if m == 1:
            a0 = vals[0]
            for y in range(maxy):
                bv = B_list[y]
                if a0 <= bv:
                    total += a0
                else:
                    total += bv

                lst = qby[y + 1]
                if lst:
                    for idx in lst:
                        if fc[idx] > b:
                            G[idx] += total
        else:
            pref = block_pref[b]
            for y in range(maxy):
                bv = B_list[y]
                p = br(vals, bv)
                total += pref[p] + (m - p) * bv

                lst = qby[y + 1]
                if lst:
                    for idx in lst:
                        if fc[idx] > b:
                            G[idx] += total

    # Partial A-blocks: lazy flush of pending B intervals per block.
    for b in range(nb):
        lst = partial[b]
        if not lst:
            continue

        lst.sort(key=itemgetter(0))
        orig = block_orig[b]
        len_b = len(orig)

        g = [0] * len_b
        prefix_g = [0] * (len_b + 1)
        prefix_valid = False
        last_y = 0

        i = 0
        nq = len(lst)
        while i < nq:
            Y = lst[i][0]
            j = i + 1
            need_prefix = lst[i][1] > 1

            while j < nq and lst[j][0] == Y:
                if lst[j][1] > 1:
                    need_prefix = True
                j += 1

            if Y > last_y:
                mP = Y - last_y

                if mP == 1:
                    pv = B_list[last_y]

                    if need_prefix:
                        s = 0
                        prefix_g[0] = 0
                        for pos, val in enumerate(orig):
                            if val < pv:
                                g[pos] += val
                            else:
                                g[pos] += pv
                            s += g[pos]
                            prefix_g[pos + 1] = s
                        prefix_valid = True
                    else:
                        for pos, val in enumerate(orig):
                            if val < pv:
                                g[pos] += val
                            else:
                                g[pos] += pv
                        prefix_valid = False

                else:
                    P = B_list[last_y:Y]
                    P.sort()
                    mP = len(P)

                    prefP = [0]
                    prefP.extend(accumulate(P))

                    if need_prefix:
                        s = 0
                        prefix_g[0] = 0
                        for pos, val in enumerate(orig):
                            p = br(P, val)
                            g[pos] += prefP[p] + (mP - p) * val
                            s += g[pos]
                            prefix_g[pos + 1] = s
                        prefix_valid = True
                    else:
                        for pos, val in enumerate(orig):
                            p = br(P, val)
                            g[pos] += prefP[p] + (mP - p) * val
                        prefix_valid = False

                last_y = Y

            if need_prefix and not prefix_valid:
                s = 0
                prefix_g[0] = 0
                for pos, gv in enumerate(g):
                    s += gv
                    prefix_g[pos + 1] = s
                prefix_valid = True

            for t in range(i, j):
                _, L, idx = lst[t]
                if L == 1:
                    G[idx] += g[0]
                else:
                    G[idx] += prefix_g[L]

            i = j

    out = []
    for X, Y, g in zip(Xs, Ys, G):
        out.append(str(X * prefB[Y] + Y * prefA[X] - 2 * g))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()