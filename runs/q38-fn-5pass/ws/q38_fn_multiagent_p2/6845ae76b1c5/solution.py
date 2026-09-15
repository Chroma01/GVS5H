import sys
from bisect import bisect_right
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]
    K = next(it)
    X = [0] * K
    Y = [0] * K
    for i in range(K):
        X[i] = next(it)
        Y[i] = next(it)
    del data, it

    # Tuned constants. 300 keeps the number of value buckets small while
    # keeping the total same-bucket matrix memory acceptable.
    VAL_BS = 300
    IDX_BS = 300
    M = (2 * N + VAL_BS - 1) // VAL_BS

    # Encode (value, occurrence-code) into one integer for fast sorting.
    CODE_BITS = (2 * N).bit_length()
    CODE_MASK = (1 << CODE_BITS) - 1

    # Encode (1-based index, value) into one integer for per-bucket sorting.
    SHIFT_IDX = 32
    MASK_IDX = (1 << SHIFT_IDX) - 1

    occ = [(v << CODE_BITS) | i for i, v in enumerate(A)]
    occ.extend((v << CODE_BITS) | (i + N) for i, v in enumerate(B))
    occ.sort()

    bucketA_by_idx = [0] * N
    bucketB_by_idx = [0] * N
    A_pairs = [[] for _ in range(M)]
    B_pairs = [[] for _ in range(M)]

    for pos, enc in enumerate(occ):
        v = enc >> CODE_BITS
        code = enc & CODE_MASK
        p = pos // VAL_BS
        if code < N:
            i = code
            bucketA_by_idx[i] = p
            A_pairs[p].append(((i + 1) << SHIFT_IDX) | v)
        else:
            i = code - N
            bucketB_by_idx[i] = p
            B_pairs[p].append(((i + 1) << SHIFT_IDX) | v)
    del occ

    # For buckets containing both A and B, keep index-sorted values.
    Aidx = [[] for _ in range(M)]
    Bidx = [[] for _ in range(M)]
    Aval = [None] * M
    Bval = [None] * M

    for p in range(M):
        ap = A_pairs[p]
        bp = B_pairs[p]
        if ap and bp:
            ap.sort()
            bp.sort()

            ai = []
            av = []
            for code in ap:
                ai.append(code >> SHIFT_IDX)
                av.append(code & MASK_IDX)

            bi = []
            bv = []
            for code in bp:
                bi.append(code >> SHIFT_IDX)
                bv.append(code & MASK_IDX)

            Aidx[p] = ai
            Aval[p] = av
            Bidx[p] = bi
            Bval[p] = bv

    del A_pairs, B_pairs

    # Prefix sums of B in original order.
    B_pref = [0] * (N + 1)
    s = 0
    for i, v in enumerate(B):
        s += v
        B_pref[i + 1] = s

    # Precompute B bucket count/sum tables at index-block boundaries.
    max_block = N // IDX_BS
    cnt_table = [[0] * M]
    sum_table = [[0] * M]
    cur_cnt = [0] * M
    cur_sum = [0] * M
    pos = 0

    ba = bucketA_by_idx
    bb = bucketB_by_idx
    bv_orig = B

    for _ in range(max_block):
        end = pos + IDX_BS
        cc = cur_cnt
        cs = cur_sum
        for i in range(pos, end):
            p = bb[i]
            cc[p] += 1
            cs[p] += bv_orig[i]
        pos = end
        cnt_table.append(cur_cnt.copy())
        sum_table.append(cur_sum.copy())

    # Precompute Y decomposition.
    Y_block = [0] * K
    Y_start = [0] * K
    Y_rem = [0] * K
    Y_total = [0] * K
    for i, ty in enumerate(Y):
        bl = ty // IDX_BS
        st = bl * IDX_BS
        Y_block[i] = bl
        Y_start[i] = st
        Y_rem[i] = ty - st
        Y_total[i] = B_pref[ty]

    order = list(range(K))
    order.sort(key=X.__getitem__)

    ans = [0] * K
    acnt = [0] * M
    asum = [0] * M
    cur_x = 0
    rangeM = range(M)

    ac = acnt
    as_ = asum
    av_orig = A
    bc = bs = base_c = base_s = None

    # Cross-bucket contributions.
    for qi in order:
        tx = X[qi]
        while cur_x < tx:
            p = ba[cur_x]
            ac[p] += 1
            as_[p] += av_orig[cur_x]
            cur_x += 1

        ty = Y[qi]
        block = Y_block[qi]
        rem = Y_rem[qi]
        start = Y_start[qi]

        base_c = cnt_table[block]
        base_s = sum_table[block]

        if rem:
            bc = base_c.copy()
            bs = base_s.copy()
            end = start + rem
            for i in range(start, end):
                p = bb[i]
                bc[p] += 1
                bs[p] += bv_orig[i]
        else:
            bc = base_c
            bs = base_s

        total_s = Y_total[qi]
        lower_c = 0
        lower_s = 0
        cross = 0

        for p in rangeM:
            bp = bc[p]
            bs_p = bs[p]
            ap = ac[p]
            if ap:
                as_p = as_[p]
                cross += (
                    as_p * lower_c
                    - ap * lower_s
                    + ap * (total_s - lower_s - bs_p)
                    - as_p * (ty - lower_c - bp)
                )
            if bp:
                lower_c += bp
                lower_s += bs_p

        ans[qi] = cross

    del (
        cnt_table, sum_table, bucketA_by_idx, bucketB_by_idx,
        ba, bb, A, B, av_orig, bv_orig, B_pref,
        acnt, asum, ac, as_, bc, bs, base_c, base_s,
        Y_block, Y_start, Y_rem, Y_total
    )

    # Build exact same-value-bucket 2D prefix matrices.
    mats = [None] * M
    strides = [0] * M

    for p in range(M):
        av = Aval[p]
        if av is None:
            continue
        bv = Bval[p]
        a = len(av)
        b = len(bv)
        stride = b + 1
        strides[p] = stride
        size = (a + 1) * stride
        flat = [0] * size

        fl = flat
        bvl = bv
        st = stride

        for x in range(1, a + 1):
            a_val = av[x - 1]
            prev = (x - 1) * st
            cur = x * st
            s = 0
            idx = cur + 1
            pidx = prev + 1
            for b_val in bvl:
                if a_val >= b_val:
                    s += a_val - b_val
                else:
                    s += b_val - a_val
                fl[idx] = fl[pidx] + s
                idx += 1
                pidx += 1

        mats[p] = array('q', flat)
        del flat, fl

    del Aval, Bval

    # Add same-bucket contributions.
    br = bisect_right
    X_list = X
    Y_list = Y
    ans_list = ans
    order_list = order

    for p in range(M):
        mat = mats[p]
        if mat is None:
            continue

        aidx = Aidx[p]
        bidx = Bidx[p]
        stride = strides[p]
        a = len(aidx)

        x = 0
        xoff = 0

        for qi in order_list:
            xq = X_list[qi]
            while x < a and aidx[x] <= xq:
                x += 1
                xoff += stride

            if x:
                y = br(bidx, Y_list[qi])
                if y:
                    ans_list[qi] += mat[xoff + y]

    sys.stdout.write('\n'.join(map(str, ans_list)))


if __name__ == '__main__':
    solve()