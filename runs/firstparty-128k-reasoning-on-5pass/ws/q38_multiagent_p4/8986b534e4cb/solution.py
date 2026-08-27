import sys
import gc
from bisect import bisect_left, bisect_right


class Block:
    __slots__ = (
        'idxs', 'l_vals', 'r_vals', 'l_pref', 'r_pref',
        'cl_order', 'cr_order', 'all_mask', 'K',
        'min_l', 'max_l', 'min_r', 'max_r'
    )


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, Q = data[0], data[1], data[2]
    l = [0] * (M + 1)
    r = [0] * (M + 1)
    pos = []
    neg = []

    ptr = 3
    for i in range(1, M + 1):
        S = data[ptr]
        T = data[ptr + 1]
        ptr += 2
        if S < T:
            l[i] = S
            r[i] = T
            pos.append(i)
        else:
            l[i] = T
            r[i] = S
            neg.append(i)

    queries = data[ptr:]
    del data

    bad = [0] * (M + 1)

    # Same left endpoint or same right endpoint is always a conflict.
    last_l = [0] * (N + 1)
    last_r = [0] * (N + 1)
    for i in range(1, M + 1):
        li = l[i]
        ri = r[i]
        b = last_l[li]
        if b > bad[i]:
            bad[i] = b
        b = last_r[ri]
        if b > bad[i]:
            bad[i] = b
        last_l[li] = i
        last_r[ri] = i
    del last_l, last_r

    # Block size: larger blocks reduce Python-level overhead.
    B = 8192 if M > 100000 else 4096

    def make_block(chunk):
        K = len(chunk)
        idxs = chunk
        ls = [0] * K
        rs = [0] * K

        min_l = 10 ** 9
        max_l = 0
        min_r = 10 ** 9
        max_r = 0
        for t, i in enumerate(chunk):
            li = l[i]
            ri = r[i]
            ls[t] = li
            rs[t] = ri
            if li < min_l:
                min_l = li
            if li > max_l:
                max_l = li
            if ri < min_r:
                min_r = ri
            if ri > max_r:
                max_r = ri

        cl_order = list(range(K))
        cl_order.sort(key=ls.__getitem__)
        l_vals = [ls[p] for p in cl_order]
        l_pref = [0] * (K + 1)
        mask = 0
        for t in range(K):
            p = cl_order[t]
            mask |= 1 << p
            l_pref[t + 1] = mask

        cr_order = list(range(K))
        cr_order.sort(key=rs.__getitem__)
        r_vals = [rs[p] for p in cr_order]
        r_pref = [0] * (K + 1)
        mask = 0
        for t in range(K):
            p = cr_order[t]
            mask |= 1 << p
            r_pref[t + 1] = mask

        blk = Block()
        blk.idxs = idxs
        blk.l_vals = l_vals
        blk.r_vals = r_vals
        blk.l_pref = l_pref
        blk.r_pref = r_pref
        blk.cl_order = cl_order
        blk.cr_order = cr_order
        blk.all_mask = (1 << K) - 1
        blk.K = K
        blk.min_l = min_l
        blk.max_l = max_l
        blk.min_r = min_r
        blk.max_r = max_r
        return blk

    def fill(P, C, A, A0, Bm, B0, Cm, D):
        """
        For every current interval p in C, fill:
          A[p]  = mask of P with l_i <= l_p
          A0[p] = mask of P with l_i <  l_p
          Bm[p] = mask of P with r_i <= r_p
          B0[p] = mask of P with r_i <  r_p
          Cm[p] = mask of P with r_i <= l_p
          D[p]  = mask of P with l_i <  r_p
        """
        Kp = P.K
        Kc = C.K

        k_lt = 0
        k_le = 0
        pv = P.l_vals
        pref = P.l_pref
        lvals = C.l_vals
        order = C.cl_order
        for t in range(Kc):
            x = lvals[t]
            p = order[t]
            while k_lt < Kp and pv[k_lt] < x:
                k_lt += 1
            while k_le < Kp and pv[k_le] <= x:
                k_le += 1
            A[p] = pref[k_le]
            A0[p] = pref[k_lt]

        k_lt = 0
        k_le = 0
        pv = P.r_vals
        pref = P.r_pref
        rvals = C.r_vals
        order = C.cr_order
        for t in range(Kc):
            x = rvals[t]
            p = order[t]
            while k_lt < Kp and pv[k_lt] < x:
                k_lt += 1
            while k_le < Kp and pv[k_le] <= x:
                k_le += 1
            Bm[p] = pref[k_le]
            B0[p] = pref[k_lt]

        k = 0
        pv = P.r_vals
        pref = P.r_pref
        lvals = C.l_vals
        order = C.cl_order
        for t in range(Kc):
            x = lvals[t]
            p = order[t]
            while k < Kp and pv[k] <= x:
                k += 1
            Cm[p] = pref[k]

        k = 0
        pv = P.l_vals
        pref = P.l_pref
        rvals = C.r_vals
        order = C.cr_order
        for t in range(Kc):
            x = rvals[t] - 1
            p = order[t]
            while k < Kp and pv[k] <= x:
                k += 1
            D[p] = pref[k]

    def process_sign(idxs):
        if len(idxs) < 2:
            return

        blocks = []
        for start in range(0, len(idxs), B):
            blocks.append(make_block(idxs[start:start + B]))

        nb = len(blocks)
        bad_arr = bad
        l_arr = l
        r_arr = r
        br = bisect_right
        bl = bisect_left

        for b in range(nb):
            C = blocks[b]
            Kc = C.K
            done = [False] * Kc
            remaining = Kc
            prev_max = blocks[b - 1].idxs[-1] if b > 0 else 0

            A = [0] * Kc
            A0 = [0] * Kc
            Bm = [0] * Kc
            B0 = [0] * Kc
            Cm = [0] * Kc
            D = [0] * Kc

            # Intra-block conflicts.
            fill(C, C, A, A0, Bm, B0, Cm, D)
            C_idxs = C.idxs
            C_all = C.all_mask

            for p in range(Kc):
                if remaining == 0:
                    break
                idx = C_idxs[p]
                if not done[p]:
                    max_intra = C_idxs[p - 1] if p > 0 else 0
                    if bad_arr[idx] < max_intra:
                        m1 = A[p] & Bm[p]
                        if m1:
                            m1 &= C_all ^ Cm[p]
                        m2 = D[p]
                        if m2:
                            m2 &= C_all ^ (A0[p] | B0[p])
                        m = (m1 | m2) & ((1 << p) - 1)
                        if m:
                            i = C_idxs[m.bit_length() - 1]
                            if i > bad_arr[idx]:
                                bad_arr[idx] = i
                            done[p] = True
                            remaining -= 1

                    if not done[p] and bad_arr[idx] >= prev_max:
                        done[p] = True
                        remaining -= 1

            if remaining == 0:
                C.cl_order = None
                C.cr_order = None
                continue

            # Previous blocks, newest first.
            for pb in range(b - 1, -1, -1):
                if remaining == 0:
                    break

                P = blocks[pb]

                # If all intervals in P are completely left/right of C,
                # or one block contains the other, no strict crossing exists.
                if (P.max_r <= C.min_l or P.min_l >= C.max_r or
                        (P.max_l <= C.min_l and P.min_r >= C.max_r) or
                        (C.max_l <= P.min_l and C.min_r >= P.max_r)):
                    continue

                Pmax = P.idxs[-1]

                # If only a few intervals remain unresolved, direct bisect is cheaper.
                if remaining * 8 < Kc:
                    P_l_vals = P.l_vals
                    P_l_pref = P.l_pref
                    P_r_vals = P.r_vals
                    P_r_pref = P.r_pref
                    allP = P.all_mask
                    P_idxs = P.idxs

                    for p in range(Kc):
                        if remaining == 0:
                            break
                        idx = C_idxs[p]
                        if not done[p]:
                            if bad_arr[idx] >= Pmax:
                                done[p] = True
                                remaining -= 1
                            else:
                                x = l_arr[idx]
                                y = r_arr[idx]

                                A_p = P_l_pref[br(P_l_vals, x)]
                                A0_p = P_l_pref[bl(P_l_vals, x)]
                                B_p = P_r_pref[br(P_r_vals, y)]
                                B0_p = P_r_pref[bl(P_r_vals, y)]
                                Cm_p = P_r_pref[br(P_r_vals, x)]
                                D_p = P_l_pref[br(P_l_vals, y - 1)]

                                m1 = A_p & B_p
                                if m1:
                                    m1 &= allP ^ Cm_p
                                m2 = D_p
                                if m2:
                                    m2 &= allP ^ (A0_p | B0_p)
                                m = m1 | m2

                                if m:
                                    i = P_idxs[m.bit_length() - 1]
                                    if i > bad_arr[idx]:
                                        bad_arr[idx] = i
                                    done[p] = True
                                    remaining -= 1
                else:
                    fill(P, C, A, A0, Bm, B0, Cm, D)
                    allP = P.all_mask
                    P_idxs = P.idxs

                    for p in range(Kc):
                        if remaining == 0:
                            break
                        idx = C_idxs[p]
                        if not done[p]:
                            if bad_arr[idx] >= Pmax:
                                done[p] = True
                                remaining -= 1
                            else:
                                m1 = A[p] & Bm[p]
                                if m1:
                                    m1 &= allP ^ Cm[p]
                                m2 = D[p]
                                if m2:
                                    m2 &= allP ^ (A0[p] | B0[p])
                                m = m1 | m2

                                if m:
                                    i = P_idxs[m.bit_length() - 1]
                                    if i > bad_arr[idx]:
                                        bad_arr[idx] = i
                                    done[p] = True
                                    remaining -= 1

            # Orders are only needed while this block is the current block.
            C.cl_order = None
            C.cr_order = None

    process_sign(pos)
    gc.collect()
    process_sign(neg)

    # Prefix maximum of bad[].
    mx = 0
    for i in range(1, M + 1):
        if bad[i] > mx:
            mx = bad[i]
        bad[i] = mx

    out = []
    for qi in range(0, 2 * Q, 2):
        L = queries[qi]
        R = queries[qi + 1]
        out.append('Yes' if bad[R] < L else 'No')

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()