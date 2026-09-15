import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    L = [0] * M
    R = [0] * M

    full_idx = -1

    maxL_val = 0
    maxL_idx = -1

    minR_val = N + 1
    minR_idx = -1

    p = 2
    for i in range(M):
        l = int(data[p])
        r = int(data[p + 1])
        p += 2

        L[i] = l
        R[i] = r

        if full_idx == -1 and l == 1 and r == N:
            full_idx = i

        if l > maxL_val:
            maxL_val = l
            maxL_idx = i

        if r < minR_val:
            minR_val = r
            minR_idx = i

    del data

    def output(k, ops):
        sys.stdout.write(str(k) + "\n")
        sys.stdout.write(" ".join(map(str, ops)) + "\n")

    # Cost 1: type 1 on a full interval.
    if full_idx != -1:
        ops = [0] * M
        ops[full_idx] = 1
        output(1, ops)
        return

    # Suffix information for the earliest disjoint pair and union-cover pair.
    suffix_max_L = [0] * (M + 1)
    suffix_min_R = [N + 1] * (M + 1)
    suffix_max_R_L1 = [-1] * (M + 1)
    suffix_min_L_RN = [N + 1] * (M + 1)

    for i in range(M - 1, -1, -1):
        l = L[i]
        r = R[i]

        prev = suffix_max_L[i + 1]
        suffix_max_L[i] = l if l > prev else prev

        prev = suffix_min_R[i + 1]
        suffix_min_R[i] = r if r < prev else prev

        prev = suffix_max_R_L1[i + 1]
        if l == 1 and r > prev:
            suffix_max_R_L1[i] = r
        else:
            suffix_max_R_L1[i] = prev

        prev = suffix_min_L_RN[i + 1]
        if r == N and l < prev:
            suffix_min_L_RN[i] = l
        else:
            suffix_min_L_RN[i] = prev

    candidates = []

    # Earliest disjoint pair: use type 2 on both intervals.
    for i in range(M - 1):
        li = L[i]
        ri = R[i]
        if suffix_max_L[i + 1] > ri or suffix_min_R[i + 1] < li:
            found = False
            for j in range(i + 1, M):
                if ri < L[j] or R[j] < li:
                    candidates.append((i, j, 2, 2))
                    found = True
                    break
            if found:
                break

    # Earliest union-cover pair: use type 1 on both intervals.
    for i in range(M - 1):
        li = L[i]
        ri = R[i]
        exists = False

        if li == 1 and suffix_min_L_RN[i + 1] <= ri + 1:
            exists = True
        if ri == N and suffix_max_R_L1[i + 1] >= li - 1:
            exists = True

        if exists:
            found = False
            for j in range(i + 1, M):
                lj = L[j]
                rj = R[j]

                if li == 1 and rj == N and ri >= lj - 1:
                    candidates.append((i, j, 1, 1))
                    found = True
                    break

                if ri == N and lj == 1 and rj >= li - 1:
                    candidates.append((i, j, 1, 1))
                    found = True
                    break

            if found:
                break

    del suffix_max_L, suffix_min_R, suffix_max_R_L1, suffix_min_L_RN

    # Earliest containment pair:
    # type 1 on the container, type 2 on the contained interval.
    # For equal intervals, put type 2 on the smaller index.
    if M >= 2:
        uniq = sorted(set(L))
        K = len(uniq)
        comp_map = {v: i for i, v in enumerate(uniq)}
        comp = [0] * M
        for i, l in enumerate(L):
            comp[i] = comp_map[l]
        del uniq, comp_map

        # Fenwick tree for prefix maximum R over compressed L.
        bit_max = [-1] * (K + 1)

        # Fenwick tree over reversed L for suffix minimum R.
        bit_min = [N + 1] * (K + 1)

        best_i = -1
        INF = N + 1
        bm = bit_max
        bn = bit_min
        kk = K

        # Process from right to left. The trees contain intervals j > i.
        for i in range(M - 1, -1, -1):
            c = comp[i]
            ri = R[i]
            idx = c + 1

            # Query max R among active intervals with L <= L_i.
            x = idx
            resmax = -1
            while x > 0:
                v = bm[x]
                if v > resmax:
                    resmax = v
                x -= x & -x

            if resmax >= ri:
                best_i = i
            else:
                # Query min R among active intervals with L >= L_i.
                # In reversed coordinates this is a prefix query.
                x = kk - c
                resmin = INF
                while x > 0:
                    v = bn[x]
                    if v < resmin:
                        resmin = v
                    x -= x & -x

                if resmin <= ri:
                    best_i = i

            # Insert current interval into the max Fenwick tree.
            x = idx
            while x <= kk:
                if ri > bm[x]:
                    bm[x] = ri
                    x += x & -x
                else:
                    break

            # Insert current interval into the min Fenwick tree (reversed L).
            x = kk - c
            while x <= kk:
                if ri < bn[x]:
                    bn[x] = ri
                    x += x & -x
                else:
                    break

        if best_i != -1:
            i = best_i
            li = L[i]
            ri = R[i]
            found = False

            for j in range(i + 1, M):
                lj = L[j]
                rj = R[j]

                if (li <= lj and ri >= rj) or (lj <= li and rj >= ri):
                    if li == lj and ri == rj:
                        candidates.append((i, j, 2, 1))
                    elif li <= lj and ri >= rj:
                        candidates.append((i, j, 1, 2))
                    else:
                        candidates.append((i, j, 2, 1))
                    found = True
                    break

    # Choose the globally lexicographically smallest valid cost-2 pair.
    best = None
    for cand in candidates:
        if best is None or (cand[0], cand[1]) < (best[0], best[1]):
            best = cand

    if best is not None:
        ops = [0] * M
        i, j, oi, oj = best
        ops[i] = oi
        ops[j] = oj
        output(2, ops)
        return

    # Cost 3: possible whenever M >= 3 and no cost-1/cost-2 solution exists.
    if M >= 3:
        A = maxL_idx
        B = minR_idx

        # Normally A != B when no cost-2 solution exists, but keep a fallback.
        if A == B:
            alt = -1
            for i in range(M):
                if i != A and L[i] == maxL_val:
                    alt = i
                    break
            if alt != -1:
                A = alt
            else:
                for i in range(M):
                    if i != B and R[i] == minR_val:
                        alt = i
                        break
                if alt != -1:
                    B = alt

        if A != B:
            C = -1
            for i in range(M):
                if i != A and i != B:
                    C = i
                    break

            if C != -1:
                ops = [0] * M
                ops[A] = 2
                ops[B] = 2
                ops[C] = 1
                output(3, ops)
                return

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    solve()