import sys
import math
from bisect import bisect_right
from array import array


def make_blocks(arr, S, nb, N):
    blocks = []
    for b in range(nb):
        st = b * S
        en = st + S
        if en > N:
            en = N
        v = sorted(arr[st:en])
        m = len(v)
        pref = [0] * (m + 1)
        s = 0
        i = 1
        for x in v:
            s += x
            pref[i] = s
            i += 1
        blocks.append((v, pref, m, s))
    return blocks


def build_pref(X, y_blocks, S, nb, W, block_len):
    """
    For each block of X, build a flat array:
      row p-1, column q = sum over first p elements of this X-block
      and first q full Y-blocks of |X_i - Y_j|.
    """
    prefs = []
    br = bisect_right

    for ba in range(nb):
        st = ba * S
        L = block_len[ba]

        # Temporary Python list is faster to fill; convert once per block.
        buf = [0] * (L * W)
        cum = [0] * W

        for t in range(L):
            x = X[st + t]
            run = 0
            ci = 1
            idx = t * W + 1

            for vals, pref, m, total in y_blocks:
                pos = br(vals, x)
                # sum_{v in block} |x-v|
                # = x*(2*pos-m) + total - 2*pref[pos]
                run += x * (pos + pos - m) + total - (pref[pos] << 1)

                c = cum[ci] + run
                cum[ci] = c
                buf[idx] = c

                ci += 1
                idx += 1

        prefs.append(array('q', buf))
        del buf

    return prefs


def build_block_pref(prefA, block_len, nb, W):
    """
    2D prefix over full block sums.
    bp[i][j] = sum over A-blocks < i and B-blocks < j.
    """
    bp = [[0] * (nb + 1) for _ in range(nb + 1)]

    for ba in range(nb):
        L = block_len[ba]
        base = (L - 1) * W
        arr = prefA[ba]

        row_acc = 0
        prev = 0
        bp_prev = bp[ba]
        bp_cur = bp[ba + 1]

        for bb in range(nb):
            cur = arr[base + bb + 1]
            val = cur - prev
            prev = cur
            row_acc += val
            bp_cur[bb + 1] = bp_prev[bb + 1] + row_acc

    return bp


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(map(int, data))
    N = next(it)
    A = [next(it) for _ in range(N)]
    B = [next(it) for _ in range(N)]
    K = next(it)
    queries = [(next(it), next(it)) for _ in range(K)]

    # Number of blocks around sqrt(K/2), block size around sqrt(2)*N/sqrt(K).
    nb = math.isqrt(K // 2) + 1
    if nb < 1:
        nb = 1
    if nb > N:
        nb = N

    S = (N + nb - 1) // nb
    nb = (N + S - 1) // S
    W = nb + 1

    blocksA = make_blocks(A, S, nb, N)
    blocksB = make_blocks(B, S, nb, N)
    block_len = [blk[2] for blk in blocksA]

    prefA = build_pref(A, blocksB, S, nb, W, block_len)
    prefB = build_pref(B, blocksA, S, nb, W, block_len)

    block_pref = build_block_pref(prefA, block_len, nb, W)

    br = bisect_right

    def calc_pp(ba, p, bb, r,
                A=A, B=B, blocksA=blocksA, blocksB=blocksB,
                block_len=block_len, S=S, br=br):
        sa = ba * S
        sb = bb * S

        # Tiny rectangles are faster by direct double loop.
        if p * r <= 80:
            ans = 0
            if p <= r:
                for i in range(sa, sa + p):
                    a = A[i]
                    for j in range(sb, sb + r):
                        b = B[j]
                        d = a - b
                        ans += d if d >= 0 else -d
            else:
                for j in range(sb, sb + r):
                    b = B[j]
                    for i in range(sa, sa + p):
                        a = A[i]
                        d = a - b
                        ans += d if d >= 0 else -d
            return ans

        L = block_len[ba]
        M = block_len[bb]

        # One element on one side: scan the other side, or use full sorted block.
        if p == 1:
            a = A[sa]
            if r == M:
                vals, pref, m, total = blocksB[bb]
                pos = br(vals, a)
                return a * (pos + pos - m) + total - (pref[pos] << 1)

            ans = 0
            end = sb + r
            for j in range(sb, end):
                d = B[j] - a
                ans += d if d >= 0 else -d
            return ans

        if r == 1:
            b = B[sb]
            if p == L:
                vals, pref, m, total = blocksA[ba]
                pos = br(vals, b)
                return b * (pos + pos - m) + total - (pref[pos] << 1)

            ans = 0
            end = sa + p
            for i in range(sa, end):
                d = A[i] - b
                ans += d if d >= 0 else -d
            return ans

        # Sort the smaller prefix, binary-search it for every element of the larger prefix.
        if p <= r:
            if p == L:
                vals, pref, m, total = blocksA[ba]
            else:
                vals = A[sa:sa + p]
                vals.sort()
                m = p
                pref = [0] * (m + 1)
                s = 0
                i = 1
                for v in vals:
                    s += v
                    pref[i] = s
                    i += 1
                total = s

            ans = 0
            end = sb + r
            for j in range(sb, end):
                x = B[j]
                pos = br(vals, x)
                ans += x * (pos + pos - m) + total - (pref[pos] << 1)
            return ans

        else:
            if r == M:
                vals, pref, m, total = blocksB[bb]
            else:
                vals = B[sb:sb + r]
                vals.sort()
                m = r
                pref = [0] * (m + 1)
                s = 0
                i = 1
                for v in vals:
                    s += v
                    pref[i] = s
                    i += 1
                total = s

            ans = 0
            end = sa + p
            for i in range(sa, end):
                x = A[i]
                pos = br(vals, x)
                ans += x * (pos + pos - m) + total - (pref[pos] << 1)
            return ans

    out = []
    pp_cache = {}
    SP1 = S + 1

    for qx, qy in queries:
        x = qx - 1
        y = qy - 1

        ba = x // S
        p = x - ba * S + 1

        bb = y // S
        r = y - bb * S + 1

        # full-full + partialA-fullB + fullA-partialB
        ans = block_pref[ba][bb]
        ans += prefA[ba][(p - 1) * W + bb]
        ans += prefB[bb][(r - 1) * W + ba]

        # partial-partial
        if p == block_len[ba] and r == block_len[bb]:
            pp = (block_pref[ba + 1][bb + 1]
                  - block_pref[ba][bb + 1]
                  - block_pref[ba + 1][bb]
                  + block_pref[ba][bb])
        else:
            key = ((ba * SP1 + p) * nb + bb) * SP1 + r
            pp = pp_cache.get(key)
            if pp is None:
                pp = calc_pp(ba, p, bb, r)
                pp_cache[key] = pp

        ans += pp
        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()