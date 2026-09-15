import sys
import math
from bisect import bisect_right


def merge_sum(outer, inner, total_inner):
    j = 0
    sum_le = 0
    total = 0
    len_inner = len(inner)
    inn = inner
    for v in outer:
        while j < len_inner and inn[j] <= v:
            sum_le += inn[j]
            j += 1
        total += v * (j + j - len_inner) + total_inner - (sum_le << 1)
    return total


def sum_abs_sorted(X, Y, totalX, totalY):
    if len(X) <= len(Y):
        return merge_sum(X, Y, totalY)
    else:
        return merge_sum(Y, X, totalX)


def add_contrib_total(A_vals, A_idx, B_vals, B_total, arr):
    j = 0
    sum_le = 0
    total = 0
    lenB = len(B_vals)
    Bv = B_vals
    ar = arr
    Ai = A_idx
    bt = B_total
    for idx, v in enumerate(A_vals):
        while j < lenB and Bv[j] <= v:
            sum_le += Bv[j]
            j += 1
        c = v * (j + j - lenB) + bt - (sum_le << 1)
        total += c
        ar[Ai[idx]] += c
    return total


def add_contrib(A_vals, A_idx, B_vals, B_total, arr):
    j = 0
    sum_le = 0
    lenB = len(B_vals)
    Bv = B_vals
    ar = arr
    Ai = A_idx
    bt = B_total
    for idx, v in enumerate(A_vals):
        while j < lenB and Bv[j] <= v:
            sum_le += Bv[j]
            j += 1
        c = v * (j + j - lenB) + bt - (sum_le << 1)
        ar[Ai[idx]] += c


def direct_sum(A_block, pa, B_block, pb):
    Ap = A_block[:pa]
    Bp = B_block[:pb]
    total = 0
    if pa <= pb:
        for a in Ap:
            for b in Bp:
                if a >= b:
                    total += a - b
                else:
                    total += b - a
    else:
        for b in Bp:
            for a in Ap:
                if a >= b:
                    total += a - b
                else:
                    total += b - a
    return total


def one_sort_sum(A_block, pa, B_block, pb, cacheA, cacheB, br=bisect_right):
    if pa <= pb:
        entry = cacheA.get(pa)
        if entry is None:
            s = sorted(A_block[:pa])
            pref = [0] * (pa + 1)
            acc = 0
            for i, v in enumerate(s):
                acc += v
                pref[i + 1] = acc
            entry = (s, pref, acc)
            cacheA[pa] = entry
        s, pref, totalA = entry
        total = 0
        pref_local = pref
        s_local = s
        totalA_local = totalA
        pa_local = pa
        for b in B_block[:pb]:
            idx = br(s_local, b)
            total += b * (idx + idx - pa_local) + totalA_local - (pref_local[idx] << 1)
        return total
    else:
        entry = cacheB.get(pb)
        if entry is None:
            s = sorted(B_block[:pb])
            pref = [0] * (pb + 1)
            acc = 0
            for i, v in enumerate(s):
                acc += v
                pref[i + 1] = acc
            entry = (s, pref, acc)
            cacheB[pb] = entry
        s, pref, totalB = entry
        total = 0
        pref_local = pref
        s_local = s
        totalB_local = totalB
        pb_local = pb
        for a in A_block[:pa]:
            idx = br(s_local, a)
            total += a * (idx + idx - pb_local) + totalB_local - (pref_local[idx] << 1)
        return total


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    dpos = 0
    N = data[dpos]
    dpos += 1
    A = data[dpos:dpos + N]
    dpos += N
    B = data[dpos:dpos + N]
    dpos += N
    K = data[dpos]
    dpos += 1

    S = min(N, int(N / math.sqrt(K)) + 1)
    if S < 1:
        S = 1
    M = (N + S - 1) // S

    A_blocks = []
    A_totals = []
    A_lens = []
    for i in range(0, N, S):
        block = A[i:i + S]
        A_blocks.append(block)
        A_lens.append(len(block))
        A_totals.append(sum(block))

    B_blocks = []
    B_totals = []
    B_lens = []
    for i in range(0, N, S):
        block = B[i:i + S]
        B_blocks.append(block)
        B_lens.append(len(block))
        B_totals.append(sum(block))

    del A, B

    A_sorted_vals = []
    A_sorted_idx = []
    for block in A_blocks:
        order = sorted(range(len(block)), key=block.__getitem__)
        A_sorted_vals.append([block[i] for i in order])
        A_sorted_idx.append(order)

    B_sorted_vals = []
    B_sorted_idx = []
    for block in B_blocks:
        order = sorted(range(len(block)), key=block.__getitem__)
        B_sorted_vals.append([block[i] for i in order])
        B_sorted_idx.append(order)

    ans = [0] * K
    q_ba = [0] * K
    q_bb = [0] * K

    partialA = [[] for _ in range(M)]
    partialB = [[] for _ in range(M)]
    partial_pairs = {}

    need_P = False

    for idx in range(K):
        x = data[dpos]
        y = data[dpos + 1]
        dpos += 2

        ba = (x - 1) // S
        pa = x - ba * S
        bb = (y - 1) // S
        pb = y - bb * S

        q_ba[idx] = ba
        q_bb[idx] = bb

        if bb > 0:
            partialA[ba].append((bb, pa, idx))
        if ba > 0:
            partialB[bb].append((ba, pb, idx))

        key = (ba, bb)
        if key in partial_pairs:
            partial_pairs[key].append((pa, pb, idx))
        else:
            partial_pairs[key] = [(pa, pb, idx)]

        if ba > 0 and bb > 0:
            need_P = True

    del data

    Asv = A_sorted_vals
    Asi = A_sorted_idx
    Atot = A_totals
    Alens = A_lens
    Bsv = B_sorted_vals
    Bsi = B_sorted_idx
    Btot = B_totals
    Blens = B_lens

    add_total = add_contrib_total
    add_no = add_contrib
    sum_abs = sum_abs_sorted

    P = None
    if need_P:
        P = [[0] * M for _ in range(M)]

    # First pass: block-pair sums P (if needed) and partial-A vs full-B fringe.
    for ba in range(M):
        queries = partialA[ba]
        if queries:
            queries.sort()
            max_t = queries[-1][0]
        else:
            max_t = 0

        if not need_P and max_t == 0:
            continue

        Av = Asv[ba]
        Ai = Asi[ba]
        lenA = Alens[ba]
        Atot_ba = Atot[ba]

        use_arr = max_t > 0
        arr = [0] * lenA if use_arr else None
        ptr = 0
        qn = len(queries)

        if need_P:
            Prow = P[ba]
            for bb in range(M):
                Bv = Bsv[bb]
                Btot_bb = Btot[bb]

                if use_arr and bb < max_t:
                    total = add_total(Av, Ai, Bv, Btot_bb, arr)
                else:
                    total = sum_abs(Av, Bv, Atot_ba, Btot_bb)
                Prow[bb] = total

                if use_arr and bb < max_t:
                    t = bb + 1
                    if ptr < qn and queries[ptr][0] == t:
                        s = 0
                        pos_arr = 0
                        while ptr < qn and queries[ptr][0] == t:
                            p = queries[ptr][1]
                            qid = queries[ptr][2]
                            while pos_arr < p:
                                s += arr[pos_arr]
                                pos_arr += 1
                            ans[qid] += s
                            ptr += 1
        else:
            for bb in range(max_t):
                Bv = Bsv[bb]
                add_no(Av, Ai, Bv, Btot[bb], arr)

                t = bb + 1
                if ptr < qn and queries[ptr][0] == t:
                    s = 0
                    pos_arr = 0
                    while ptr < qn and queries[ptr][0] == t:
                        p = queries[ptr][1]
                        qid = queries[ptr][2]
                        while pos_arr < p:
                            s += arr[pos_arr]
                            pos_arr += 1
                        ans[qid] += s
                        ptr += 1

    # Add full-block/full-block part.
    if need_P:
        prefP = [[0] * (M + 1) for _ in range(M + 1)]
        for i in range(M):
            row_acc = 0
            prev = prefP[i]
            cur = prefP[i + 1]
            prow = P[i]
            for j in range(M):
                row_acc += prow[j]
                cur[j + 1] = prev[j + 1] + row_acc

        for idx in range(K):
            ans[idx] += prefP[q_ba[idx]][q_bb[idx]]

    # Second pass: full-A vs partial-B fringe.
    for bb in range(M):
        queries = partialB[bb]
        if not queries:
            continue

        queries.sort()
        max_t = queries[-1][0]

        Bv = Bsv[bb]
        Bi = Bsi[bb]
        lenB = Blens[bb]
        arr = [0] * lenB

        ptr = 0
        qn = len(queries)

        for aa in range(max_t):
            Av = Asv[aa]
            add_no(Bv, Bi, Av, Atot[aa], arr)

            t = aa + 1
            if ptr < qn and queries[ptr][0] == t:
                s = 0
                pos_arr = 0
                while ptr < qn and queries[ptr][0] == t:
                    p = queries[ptr][1]
                    qid = queries[ptr][2]
                    while pos_arr < p:
                        s += arr[pos_arr]
                        pos_arr += 1
                    ans[qid] += s
                    ptr += 1

    # Partial-partial part, grouped by block pair.
    full_cache = {}

    for (ba, bb), qlist in partial_pairs.items():
        A_block = A_blocks[ba]
        B_block = B_blocks[bb]
        la = len(A_block)
        lb = len(B_block)

        uniq = {}

        for pa, pb, idx in qlist:
            if pa == la and pb == lb:
                if P is not None:
                    ans[idx] += P[ba][bb]
                else:
                    key = (ba, bb)
                    val = full_cache.get(key)
                    if val is None:
                        val = sum_abs(Asv[ba], Bsv[bb], Atot[ba], Btot[bb])
                        full_cache[key] = val
                    ans[idx] += val
            else:
                key = (pa, pb)
                ids = uniq.get(key)
                if ids is None:
                    uniq[key] = [idx]
                else:
                    ids.append(idx)

        if not uniq:
            continue

        u = len(uniq)

        # Heavy block pair: build a 2D prefix implicitly row by row.
        if u * (la + lb) > la * lb:
            by_pa = [[] for _ in range(la + 1)]
            for (pa, pb), ids in uniq.items():
                by_pa[pa].append((pb, ids))

            col = [0] * (lb + 1)
            col_local = col
            B_list = B_block

            for i, a in enumerate(A_block):
                row_cum = 0
                j = 1
                for b in B_list:
                    if a >= b:
                        row_cum += a - b
                    else:
                        row_cum += b - a
                    col_local[j] += row_cum
                    j += 1

                if by_pa[i + 1]:
                    for pb, ids in by_pa[i + 1]:
                        val = col_local[pb]
                        for idx in ids:
                            ans[idx] += val

        else:
            # Light block pair: answer each distinct prefix pair once.
            if u >= 64:
                cacheA = {}
                cacheB = {}

                for (pa, pb), ids in uniq.items():
                    if pa * pb <= 256 or pa == 1 or pb == 1:
                        val = direct_sum(A_block, pa, B_block, pb)
                    else:
                        entryA = cacheA.get(pa)
                        if entryA is None:
                            s = sorted(A_block[:pa])
                            entryA = (s, sum(s))
                            cacheA[pa] = entryA

                        entryB = cacheB.get(pb)
                        if entryB is None:
                            s = sorted(B_block[:pb])
                            entryB = (s, sum(s))
                            cacheB[pb] = entryB

                        As, At = entryA
                        Bs, Bt = entryB

                        if len(As) <= len(Bs):
                            val = merge_sum(As, Bs, Bt)
                        else:
                            val = merge_sum(Bs, As, At)

                    for idx in ids:
                        ans[idx] += val

            else:
                cacheA = {}
                cacheB = {}

                for (pa, pb), ids in uniq.items():
                    if pa * pb <= 256 or pa == 1 or pb == 1:
                        val = direct_sum(A_block, pa, B_block, pb)
                    else:
                        val = one_sort_sum(A_block, pa, B_block, pb, cacheA, cacheB)

                    for idx in ids:
                        ans[idx] += val

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    solve()