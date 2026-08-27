import sys
from bisect import bisect_left, bisect_right


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    to_int = int
    N = to_int(data[0])
    P = [0] * (N + 1)
    s = 0
    for i in range(1, N + 1):
        s += to_int(data[i])
        P[i] = s
    del data

    SHIFT = 20
    MASK = (1 << SHIFT) - 1
    PACK_SHIFT = 40

    exp_head = [0] * (N + 2)
    exp_next = [0] * (N + 2)
    prev = [0] * (N + 2)
    nxt = [0] * (N + 2)

    # Two-level bitset for successor queries among active left endpoints.
    BSHIFT = 10
    B = 1 << BSHIFT
    BMASK = B - 1
    M = (N + BMASK) >> BSHIFT
    masks = [0] * M
    bits = [1 << i for i in range(B)]
    block_bit = [1 << i for i in range(M)]
    bstart = [i << BSHIFT for i in range(M)]
    block_bits = 0

    head = 0
    tail = 0
    intervals = []
    append = intervals.append
    br = bisect_right
    bl = bisect_left
    N1 = N + 1

    for r in range(1, N1):
        # Remove left endpoints whose left inequality no longer holds.
        e = exp_head[r]
        while e:
            p = prev[e]
            q = nxt[e]
            if p:
                nxt[p] = q
            else:
                head = q
            if q:
                prev[q] = p
            else:
                tail = p

            pos = e - 1
            b = pos >> BSHIFT
            off = pos & BMASK
            mb = masks[b] ^ bits[off]
            masks[b] = mb
            if not mb:
                block_bits &= ~block_bit[b]

            e = exp_next[e]

        Pr = P[r]

        # Add l = r if the left inequality can hold for at least r.
        if r == 1:
            R = N
        else:
            pr1 = P[r - 1]
            th = pr1 + pr1 - P[r - 2]
            R = br(P, th, r - 1, N1) - 1

        if R >= r:
            prev[r] = tail
            nxt[r] = 0
            if tail:
                nxt[tail] = r
            else:
                head = r
            tail = r

            pos = r - 1
            b = pos >> BSHIFT
            off = pos & BMASK
            mb = masks[b]
            if not mb:
                block_bits |= block_bit[b]
            masks[b] = mb | bits[off]

            t = R + 1
            if t <= N:
                exp_next[r] = exp_head[t]
                exp_head[t] = r

        # Smallest l for which the right inequality holds.
        if r == N:
            L = 1
        else:
            th = Pr + Pr - P[r + 1]
            i = bl(P, th, 0, r)
            if i < r:
                L = i + 1
            else:
                L = r + 1

        # All active l >= L are stable intervals ending at r.
        if L <= tail:
            if L <= head:
                first = head
            else:
                x = L
                b = (x - 1) >> BSHIFT
                off = (x - 1) & BMASK
                m = masks[b] >> off
                if m:
                    first = bstart[b] + off + (m & -m).bit_length()
                else:
                    bm = block_bits >> (b + 1)
                    if bm:
                        blk = b + (bm & -bm).bit_length()
                        m2 = masks[blk]
                        first = bstart[blk] + (m2 & -m2).bit_length()
                    else:
                        first = 0

            if first:
                cur = first
                while cur:
                    ssum = Pr - P[cur - 1]
                    append((ssum << PACK_SHIFT) | (cur << SHIFT) | r)
                    cur = nxt[cur]

    del P, exp_head, exp_next, prev, nxt, masks, bits, block_bit, bstart

    intervals.sort()

    par = list(range(N + 2))
    ans = [0] * (N + 1)

    def find(x, par=par):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for val in intervals:
        rr = val & MASK
        ll = (val >> SHIFT) & MASK
        ss = val >> PACK_SHIFT
        i = find(ll)
        while i <= rr:
            ans[i] = ss
            par[i] = find(i + 1)
            i = par[i]

    del intervals, append

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')


if __name__ == '__main__':
    solve()