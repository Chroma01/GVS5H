import sys
import math
from bisect import bisect_right


def make_blocks(arr, S):
    blocks = []
    n = len(arr)
    for start in range(0, n, S):
        seg = arr[start:start + S]
        L = len(seg)
        sv = sorted(seg)
        pref = [0] * (L + 1)
        s = 0
        for i, v in enumerate(sv):
            s += v
            pref[i + 1] = s
        blocks.append((seg, sv, pref, s, L))
    return blocks


def prefix_contrib(seq, osv, opref, otot, olen, C):
    """C[r] = sum over first r elements of seq vs the whole other block."""
    s = 0
    C[0] = 0
    br = bisect_right
    i = 1
    for val in seq:
        p = br(osv, val)
        op = opref[p]
        s += val * p - op + (otot - op) - val * (olen - p)
        C[i] = s
        i += 1
    return s


def full_contrib(seq, osv, opref, otot, olen):
    """Sum over all elements of seq vs the whole other block."""
    s = 0
    br = bisect_right
    for val in seq:
        p = br(osv, val)
        op = opref[p]
        s += val * p - op + (otot - op) - val * (olen - p)
    return s


def sum_abs_sorted(l1, t1, l2, t2):
    """Sum |x-y| over two sorted lists, using a two-pointer scan."""
    if len(l1) <= len(l2):
        it = l1
        other = l2
        total = t2
    else:
        it = l2
        other = l1
        total = t1

    p = 0
    sum_le = 0
    lo = len(other)
    s = 0
    for val in it:
        while p < lo and other[p] <= val:
            sum_le += other[p]
            p += 1
        s += val * p - sum_le + (total - sum_le) - val * (lo - p)
    return s


def process_light(qs, Aseg, Bseg, Alen, Blen, Asv, Atot, Bsv, Btot, ans, S):
    DIRECT = max(2000, S)
    use_cache = (S <= 3000) or (len(qs) * S <= 2_000_000)
    cacheA = {} if use_cache else None
    cacheB = {} if use_cache else None

    for q, ra, rb in qs:
        if ra * rb <= DIRECT:
            s = 0
            if ra <= rb:
                for i in range(ra):
                    av = Aseg[i]
                    for j in range(rb):
                        bv = Bseg[j]
                        if av >= bv:
                            s += av - bv
                        else:
                            s += bv - av
            else:
                for j in range(rb):
                    bv = Bseg[j]
                    for i in range(ra):
                        av = Aseg[i]
                        if av >= bv:
                            s += av - bv
                        else:
                            s += bv - av
            ans[q] += s
            continue

        if use_cache:
            item = cacheA.get(ra)
            if item is None:
                if ra == Alen:
                    item = (Asv, Atot)
                else:
                    lst = Aseg[:ra]
                    lst.sort()
                    item = (lst, sum(lst))
                cacheA[ra] = item

            item2 = cacheB.get(rb)
            if item2 is None:
                if rb == Blen:
                    item2 = (Bsv, Btot)
                else:
                    lst = Bseg[:rb]
                    lst.sort()
                    item2 = (lst, sum(lst))
                cacheB[rb] = item2
        else:
            if ra == Alen:
                l1 = Asv
                t1 = Atot
            else:
                l1 = Aseg[:ra]
                l1.sort()
                t1 = sum(l1)

            if rb == Blen:
                l2 = Bsv
                t2 = Btot
            else:
                l2 = Bseg[:rb]
                l2.sort()
                t2 = sum(l2)

            item = (l1, t1)
            item2 = (l2, t2)

        ans[q] += sum_abs_sorted(item[0], item[1], item2[0], item2[1])


def process_heavy(qs, Aseg, Bseg, Alen, Blen, ans):
    max_ra = 0
    max_rb = 0
    for _, ra, rb in qs:
        if ra > max_ra:
            max_ra = ra
        if rb > max_rb:
            max_rb = rb

    if max_ra * Blen <= max_rb * Alen:
        by_ra = {}
        for q, ra, rb in qs:
            lst = by_ra.get(ra)
            if lst is None:
                by_ra[ra] = [(q, rb)]
            else:
                lst.append((q, rb))

        prev = [0] * (Blen + 1)
        new = [0] * (Blen + 1)
        cur = 0

        for target in sorted(by_ra):
            while cur < target:
                x = Aseg[cur]
                s = 0
                new[0] = 0
                for j in range(Blen):
                    y = Bseg[j]
                    if x >= y:
                        s += x - y
                    else:
                        s += y - x
                    new[j + 1] = prev[j + 1] + s
                prev, new = new, prev
                cur += 1

            for q, rb in by_ra[target]:
                ans[q] += prev[rb]
    else:
        by_rb = {}
        for q, ra, rb in qs:
            lst = by_rb.get(rb)
            if lst is None:
                by_rb[rb] = [(q, ra)]
            else:
                lst.append((q, ra))

        prev = [0] * (Alen + 1)
        new = [0] * (Alen + 1)
        cur = 0

        for target in sorted(by_rb):
            while cur < target:
                y = Bseg[cur]
                s = 0
                new[0] = 0
                for i in range(Alen):
                    x = Aseg[i]
                    if x >= y:
                        s += x - y
                    else:
                        s += y - x
                    new[i + 1] = prev[i + 1] + s
                prev, new = new, prev
                cur += 1

            for q, ra in by_rb[target]:
                ans[q] += prev[ra]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    pos = 0
    N = data[pos]
    pos += 1

    A = data[pos:pos + N]
    pos += N

    B = data[pos:pos + N]
    pos += N

    K = data[pos]
    pos += 1

    # Tuned block size for Python: same sqrt idea, slightly larger than 1.2*N/sqrt(K).
    S = int(1.8 * N / math.sqrt(K))
    if S < 1:
        S = 1
    if S > N:
        S = N

    NA = (N + S - 1) // S
    NB = (N + S - 1) // S

    groupsA = [[] for _ in range(NA)]
    groupsB = [[] for _ in range(NB)]
    res_groups = {}
    fa_arr = [0] * K
    fb_arr = [0] * K

    max_fa_full = 0
    max_fb_full = 0

    for q in range(K):
        x = data[pos]
        y = data[pos + 1]
        pos += 2

        fa = x // S
        ra = x - fa * S
        fb = y // S
        rb = y - fb * S

        fa_arr[q] = fa
        fb_arr[q] = fb

        if fa > max_fa_full:
            max_fa_full = fa
        if fb > max_fb_full:
            max_fb_full = fb

        if ra:
            groupsA[fa].append((q, ra, fb))
        if rb:
            groupsB[fb].append((q, rb, fa))
        if ra and rb:
            key = (fa, fb)
            if key in res_groups:
                res_groups[key].append((q, ra, rb))
            else:
                res_groups[key] = [(q, ra, rb)]

    del data

    A_blocks = make_blocks(A, S)
    B_blocks = make_blocks(B, S)
    del A, B

    ans = [0] * K

    # Sweep A blocks:
    # - compute full block-pair sums F[a][b]
    # - add partial-A-prefix vs full-B-block contributions
    F = [[0] * max_fb_full for _ in range(max_fa_full)]

    for a in range(max_fa_full):
        Aseg, Asv, Apref, Atot, Alen = A_blocks[a]
        rowF = F[a]
        qs = groupsA[a]

        if qs:
            max_fb_q = 0
            for _, _, fb in qs:
                if fb > max_fb_q:
                    max_fb_q = fb

            if max_fb_q:
                C = [0] * (Alen + 1)
                for b in range(max_fb_q):
                    _, Bsv, Bpref, Btot, Blen = B_blocks[b]
                    s = prefix_contrib(Aseg, Bsv, Bpref, Btot, Blen, C)
                    rowF[b] = s
                    for q, ra, fb in qs:
                        if fb > b:
                            ans[q] += C[ra]

            for b in range(max_fb_q, max_fb_full):
                _, Bsv, Bpref, Btot, Blen = B_blocks[b]
                rowF[b] = full_contrib(Aseg, Bsv, Bpref, Btot, Blen)
        else:
            for b in range(max_fb_full):
                _, Bsv, Bpref, Btot, Blen = B_blocks[b]
                rowF[b] = full_contrib(Aseg, Bsv, Bpref, Btot, Blen)

    # If the maximum full-A count is not the last block, a query may still have
    # a partial prefix in that last full-count block.
    if max_fa_full < NA:
        qs = groupsA[max_fa_full]
        if qs:
            Aseg, Asv, Apref, Atot, Alen = A_blocks[max_fa_full]
            max_fb_q = 0
            for _, _, fb in qs:
                if fb > max_fb_q:
                    max_fb_q = fb

            if max_fb_q:
                C = [0] * (Alen + 1)
                for b in range(max_fb_q):
                    _, Bsv, Bpref, Btot, Blen = B_blocks[b]
                    prefix_contrib(Aseg, Bsv, Bpref, Btot, Blen, C)
                    for q, ra, fb in qs:
                        if fb > b:
                            ans[q] += C[ra]

    # 2D prefix over full block-pair sums.
    prefFF = [[0] * (max_fb_full + 1) for _ in range(max_fa_full + 1)]
    for a in range(max_fa_full):
        row = F[a]
        acc = 0
        prev = prefFF[a]
        cur = prefFF[a + 1]
        for b in range(max_fb_full):
            acc += row[b]
            cur[b + 1] = prev[b + 1] + acc

    for q in range(K):
        ans[q] += prefFF[fa_arr[q]][fb_arr[q]]

    # Sweep B blocks:
    # - add full-A-blocks vs partial-B-prefix contributions
    for b in range(max_fb_full):
        qs = groupsB[b]
        if not qs:
            continue

        Bseg, Bsv, Bpref, Btot, Blen = B_blocks[b]
        max_fa_q = 0
        for _, _, fa in qs:
            if fa > max_fa_q:
                max_fa_q = fa

        if max_fa_q:
            C = [0] * (Blen + 1)
            for a in range(max_fa_q):
                Aseg, Asv, Apref, Atot, Alen = A_blocks[a]
                prefix_contrib(Bseg, Asv, Apref, Atot, Alen, C)
                for q, rb, fa in qs:
                    if fa > a:
                        ans[q] += C[rb]

    if max_fb_full < NB:
        qs = groupsB[max_fb_full]
        if qs:
            Bseg, Bsv, Bpref, Btot, Blen = B_blocks[max_fb_full]
            max_fa_q = 0
            for _, _, fa in qs:
                if fa > max_fa_q:
                    max_fa_q = fa

            if max_fa_q:
                C = [0] * (Blen + 1)
                for a in range(max_fa_q):
                    Aseg, Asv, Apref, Atot, Alen = A_blocks[a]
                    prefix_contrib(Bseg, Asv, Apref, Atot, Alen, C)
                    for q, rb, fa in qs:
                        if fa > a:
                            ans[q] += C[rb]

    # Partial-partial residuals, grouped by block pair.
    for (a, b), qs in res_groups.items():
        Aseg, Asv, Apref, Atot, Alen = A_blocks[a]
        Bseg, Bsv, Bpref, Btot, Blen = B_blocks[b]

        max_ra = 0
        max_rb = 0
        light_cost = 0
        for _, ra, rb in qs:
            if ra > max_ra:
                max_ra = ra
            if rb > max_rb:
                max_rb = rb
            light_cost += ra + rb

        heavy_cost = max_ra * Blen
        alt_cost = max_rb * Alen
        if alt_cost < heavy_cost:
            heavy_cost = alt_cost

        if len(qs) >= 300 and heavy_cost <= 4_000_000 and heavy_cost * 2 < light_cost:
            process_heavy(qs, Aseg, Bseg, Alen, Blen, ans)
        else:
            process_light(qs, Aseg, Bseg, Alen, Blen, Asv, Atot, Bsv, Btot, ans, S)

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()