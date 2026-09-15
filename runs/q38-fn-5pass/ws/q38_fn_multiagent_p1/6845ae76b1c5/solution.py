import sys
import math
from itertools import accumulate


def main():
    if sys.implementation.name == "cpython":
        import gc
        gc.disable()

    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    pos = 0
    N = data[pos]
    pos += 1

    A = [0] + data[pos:pos + N]
    pos += N

    B = [0] + data[pos:pos + N]
    pos += N

    K = data[pos]
    pos += 1

    if K == 0:
        return

    xs = [0] * K
    ys = [0] * K
    max_x = 0
    max_y = 0

    for q in range(K):
        x = data[pos]
        y = data[pos + 1]
        pos += 2
        xs[q] = x
        ys[q] = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    del data

    uniq_y = sorted(set(ys))
    D = len(uniq_y)

    y_to_idx = [-1] * (max_y + 1)
    for i, y in enumerate(uniq_y):
        y_to_idx[y] = i

    # Dynamic block size.
    # Precomputation is about max_y * N / S, partial work is about K * S.
    S = int(math.sqrt(max_y * N / K))
    max_sub = 3_000_000
    cap = (2 * max_sub) // K
    if cap < 1:
        cap = 1
    if S > cap:
        S = cap
    if S < 1:
        S = 1
    if S > N:
        S = N

    num_blocks = (max_x - 1) // S + 1
    queries_by_block = [[] for _ in range(num_blocks)]
    for qid, x in enumerate(xs):
        queries_by_block[(x - 1) // S].append(qid)

    # Bit widths for packing subqueries.
    ID_BITS = max(1, K.bit_length())
    Y_BITS = max(1, max_y.bit_length())
    Y_SHIFT = ID_BITS + 1
    A_SHIFT = Y_SHIFT + Y_BITS
    Y_MASK = (1 << Y_BITS) - 1
    ID_MASK = (1 << ID_BITS) - 1

    A_pack = [0] * (N + 1)
    for i in range(1, N + 1):
        A_pack[i] = A[i] << A_SHIFT

    y_pack = [y << Y_SHIFT for y in ys]
    qid_pack = [i << 1 for i in range(K)]

    M = max_y

    # Sort only B[1..max_y], because larger indices are never queried.
    order = list(range(1, M + 1))
    order.sort(key=B.__getitem__)
    sorted_B_idx = order
    sorted_B_vals = [B[i] for i in order]

    prefB = [0] * (M + 1)
    acc = 0
    for i in range(1, M + 1):
        acc += B[i]
        prefB[i] = acc

    del B

    d = [0] * (M + 1)
    base = [0] * D
    ans = [0] * K
    subqs = []

    BATCH = 500_000
    range_M = range(M)
    range_1_M = range(1, M + 1)
    range_D = range(D)

    # On CPython, itertools.accumulate is usually faster than a Python prefix loop.
    # On PyPy, an in-place loop avoids many temporary list allocations.
    USE_ACCUMULATE = (sys.implementation.name == "cpython")

    def solve_chunk(subqs, n=M, sv=sorted_B_vals, si=sorted_B_idx, pref=prefB, ans=ans,
                    A_SHIFT=A_SHIFT, Y_SHIFT=Y_SHIFT, Y_MASK=Y_MASK, ID_MASK=ID_MASK):
        if not subqs:
            return

        subqs.sort()
        bitc = [0] * (n + 1)
        bits = [0] * (n + 1)
        ptr = 0

        for p in subqs:
            a = p >> A_SHIFT

            while ptr < n and sv[ptr] <= a:
                v = sv[ptr]
                i = si[ptr]
                while i <= n:
                    bitc[i] += 1
                    bits[i] += v
                    i += i & -i
                ptr += 1

            y = (p >> Y_SHIFT) & Y_MASK
            qid = (p >> 1) & ID_MASK

            c = 0
            s = 0
            i = y
            while i:
                c += bitc[i]
                s += bits[i]
                i &= i - 1

            # sum_{j<=y} |a - B_j|
            val = a * (c + c - y) + pref[y] - (s << 1)

            if p & 1:
                ans[qid] -= val
            else:
                ans[qid] += val

    uy = uniq_y

    for b in range(num_blocks):
        start = b * S + 1
        end = (b + 1) * S
        if end > N:
            end = N

        vals = A[start:end + 1]
        vals.sort()
        blen = len(vals)
        total = sum(vals)

        # For each B_j, compute sum_{a in block} |a - B_j|.
        # If p = #block_values <= B_j and sum_le = sum of those values:
        # contribution = B_j * (2p - blen) + total - 2*sum_le.
        coef = -blen
        const = total
        p = 0

        sv = sorted_B_vals
        si = sorted_B_idx
        dloc = d
        valsloc = vals
        blenloc = blen

        for t in range_M:
            v = sv[t]
            while p < blenloc and valsloc[p] <= v:
                const -= valsloc[p] * 2
                coef += 2
                p += 1
            dloc[si[t]] = v * coef + const

        if USE_ACCUMULATE:
            prefix = list(accumulate(dloc))
        else:
            acc2 = 0
            for i in range_1_M:
                acc2 += dloc[i]
                dloc[i] = acc2
            prefix = dloc

        if queries_by_block[b]:
            base_loc = base
            ans_loc = ans
            xs_loc = xs
            ys_loc = ys
            yidx_loc = y_to_idx
            apack = A_pack
            yp = y_pack
            qp = qid_pack
            append = subqs.append

            for qid in queries_by_block[b]:
                x = xs_loc[qid]
                y = ys_loc[qid]
                yidx = yidx_loc[y]

                prefix_len = x - start + 1
                suffix_len = end - x

                if prefix_len <= suffix_len:
                    # Use full previous blocks, add the short A-prefix.
                    ans_loc[qid] += base_loc[yidx]
                    bp = yp[qid] | qp[qid]
                    for i in range(start, x + 1):
                        append(apack[i] | bp)
                else:
                    # Use full previous blocks plus the whole current block,
                    # subtract the short A-suffix.
                    ans_loc[qid] += base_loc[yidx] + prefix[y]
                    bp = yp[qid] | qp[qid] | 1
                    for i in range(x + 1, end + 1):
                        append(apack[i] | bp)

                if len(subqs) >= BATCH:
                    solve_chunk(subqs)
                    subqs.clear()

        if b + 1 < num_blocks:
            base_loc = base
            pref_loc = prefix
            uy_loc = uy
            for idx in range_D:
                base_loc[idx] += pref_loc[uy_loc[idx]]
            del pref_loc

        del prefix

    if subqs:
        solve_chunk(subqs)
        subqs.clear()

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()