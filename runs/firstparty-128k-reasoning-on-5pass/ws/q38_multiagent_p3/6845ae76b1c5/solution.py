import sys
from bisect import bisect_right
from itertools import accumulate


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    p += 1
    A = data[p:p + N]
    p += N
    B = data[p:p + N]
    p += N
    K = data[p]
    p += 1

    # If every A and B value is the same single value, all answers are zero.
    amin = min(A)
    amax = max(A)
    bmin = min(B)
    bmax = max(B)
    if amin == amax and bmin == bmax and amin == bmin:
        sys.stdout.write("\n".join(["0"] * K))
        return

    Xs = [0] * K
    Ys = [0] * K
    for i in range(K):
        Xs[i] = data[p]
        Ys[i] = data[p + 1]
        p += 2

    del data

    # Prefix sums of B in original index order.
    prefB = [0] * (N + 1)
    s = 0
    for i, b in enumerate(B, 1):
        s += b
        prefB[i] = s

    totalB_sum = [prefB[y] for y in Ys]

    ans = [0] * K
    less_cnt = [0] * K
    less_sum = [0] * K

    E = 2 * N

    # Chunk size for value partitioning.
    T = int(4 * (K ** 0.5))
    if T < 64:
        T = 64
    if T > 700:
        T = 700
    if T > E:
        T = E
    if T < 1:
        T = 1

    # Combined elements: (value, signed_index).
    # Positive index => A element, negative index => B element.
    combined = [(a, i) for i, a in enumerate(A, 1)]
    combined.extend((b, -j) for j, b in enumerate(B, 1))
    del A, B
    combined.sort()

    br = bisect_right

    Xs_l = Xs
    Ys_l = Ys
    totalB_sum_l = totalB_sum
    ans_l = ans
    less_cnt_l = less_cnt
    less_sum_l = less_sum
    K_l = K

    pos = 0
    while pos < E:
        end = pos + T
        if end > E:
            end = E

        A_list = []
        B_list = []

        for t in range(pos, end):
            val, code = combined[t]
            if code > 0:
                A_list.append((code, val))
            else:
                B_list.append((-code, val))

        na = len(A_list)
        nb = len(B_list)

        if na:
            A_list.sort()
            A_idx = [0] * na
            A_vals = [0] * na
            for i, (idx, val) in enumerate(A_list):
                A_idx[i] = idx
                A_vals[i] = val
            A_pref = [0] + list(accumulate(A_vals))
        else:
            A_idx = []
            A_vals = []
            A_pref = [0]

        if nb:
            B_list.sort()
            B_idx = [0] * nb
            B_vals = [0] * nb
            for i, (idx, val) in enumerate(B_list):
                B_idx[i] = idx
                B_vals[i] = val
            B_pref = [0] + list(accumulate(B_vals))
        else:
            B_idx = []
            B_vals = []
            B_pref = [0]

        # Same-chunk 2D prefix, if needed.
        P = None
        if na and nb and combined[pos][0] != combined[end - 1][0]:
            P = [[0] * (nb + 1)]
            Bv = B_vals
            nb_l = nb
            abs_ = abs
            for a in A_vals:
                prev = P[-1]
                row = [0] * (nb_l + 1)
                cum = 0
                for j in range(nb_l):
                    cum += abs_(a - Bv[j])
                    row[j + 1] = prev[j + 1] + cum
                P.append(row)

        if na == 0:
            # Only B elements: just update the "less B" accumulators.
            if nb:
                B_idx_l = B_idx
                B_pref_l = B_pref
                for k in range(K_l):
                    ib = br(B_idx_l, Ys_l[k])
                    if ib:
                        less_cnt_l[k] += ib
                        less_sum_l[k] += B_pref_l[ib]

        elif nb == 0:
            # Only A elements: add contributions against already-seen B and future B.
            A_idx_l = A_idx
            A_pref_l = A_pref
            for k in range(K_l):
                ia = br(A_idx_l, Xs_l[k])
                if ia:
                    sumA = A_pref_l[ia]
                    lc = less_cnt_l[k]
                    ls = less_sum_l[k]
                    ans_l[k] += (
                        sumA * lc
                        - ia * ls
                        + ia * (totalB_sum_l[k] - ls)
                        - sumA * (Ys_l[k] - lc)
                    )

        else:
            A_idx_l = A_idx
            B_idx_l = B_idx
            A_pref_l = A_pref
            B_pref_l = B_pref

            if P is None:
                # Same-chunk contribution is zero (all values in this chunk equal).
                for k in range(K_l):
                    ia = br(A_idx_l, Xs_l[k])
                    ib = br(B_idx_l, Ys_l[k])
                    if ia or ib:
                        sumA = A_pref_l[ia] if ia else 0
                        sumB = B_pref_l[ib] if ib else 0
                        lc = less_cnt_l[k]
                        ls = less_sum_l[k]
                        ans_l[k] += (
                            sumA * lc
                            - ia * ls
                            + ia * (totalB_sum_l[k] - ls - sumB)
                            - sumA * (Ys_l[k] - lc - ib)
                        )
                        if ib:
                            less_cnt_l[k] = lc + ib
                            less_sum_l[k] = ls + sumB
            else:
                P_l = P
                for k in range(K_l):
                    x = Xs_l[k]
                    y = Ys_l[k]
                    ia = br(A_idx_l, x)
                    ib = br(B_idx_l, y)
                    sumA = A_pref_l[ia]
                    sumB = B_pref_l[ib]
                    lc = less_cnt_l[k]
                    ls = less_sum_l[k]
                    ans_l[k] += (
                        P_l[ia][ib]
                        + sumA * lc
                        - ia * ls
                        + ia * (totalB_sum_l[k] - ls - sumB)
                        - sumA * (y - lc - ib)
                    )
                    less_cnt_l[k] = lc + ib
                    less_sum_l[k] = ls + sumB

        pos = end

    sys.stdout.write("\n".join(map(str, ans_l)))


if __name__ == "__main__":
    main()