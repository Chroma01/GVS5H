import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[0], data[1], data[2], data[3]
    C = B - A

    full = (1 << B) - 1
    # Bits A-1 .. B-1 are the previous squares that can reach the next square.
    high_mask = ((1 << (C + 1)) - 1) << (A - 1)

    # Safe-step transition matrix.
    # Bit k of the state means square p-k is reachable, with k=0 being current p.
    # New bit 0 depends on high_mask; new bit j (j>=1) is old bit j-1.
    S = [0] * B
    S[0] = high_mask
    for j in range(1, B):
        S[j] = 1 << (j - 1)

    def compose(nmat, mmat):
        # Return matrix for applying mmat first, then nmat.
        pmat = [0] * B
        for j in range(B):
            row = 0
            m = nmat[j]
            while m:
                lsb = m & -m
                i = lsb.bit_length() - 1
                row |= mmat[i]
                m ^= lsb
            pmat[j] = row
        return pmat

    max_bits = N.bit_length() + 1
    powers = [S]
    for _ in range(1, max_bits):
        powers.append(compose(powers[-1], powers[-1]))
    powers = [tuple(p) for p in powers]

    # B <= 20, so split a mask into two 10-bit halves for O(1) application.
    HALF = 10
    LOW_MASK = (1 << HALF) - 1
    bits = [1 << j for j in range(B)]
    rB = range(B)

    tables = []
    for mat in powers:
        low = [0] * 1024
        high_tab = [0] * 1024
        for x in range(1024):
            res = 0
            for j in rB:
                if x & mat[j]:
                    res |= bits[j]
            low[x] = res

            xh = x << HALF
            res = 0
            for j in rB:
                if xh & mat[j]:
                    res |= bits[j]
            high_tab[x] = res
        tables.append((low, high_tab))

    def apply_safe(mask, g, tables=tables, LOW_MASK=LOW_MASK, HALF=HALF):
        k = 0
        while g:
            if g & 1:
                low_tab, high_tab = tables[k]
                mask = low_tab[mask & LOW_MASK] | high_tab[mask >> HALF]
                if mask == 0:
                    return 0
            g >>= 1
            k += 1
        return mask

    mask = 1  # square 1 is reachable
    p = 1
    idx = 4

    for _ in range(M):
        L = data[idx]
        R = data[idx + 1]
        idx += 2

        if mask:
            g = L - p - 1
            if g > 0:
                mask = apply_safe(mask, g)
            p = L - 1

            h = R - L + 1
            if h >= B:
                mask = 0
            else:
                mask = (mask << h) & full

        p = R

    if mask:
        g = N - p
        if g > 0:
            mask = apply_safe(mask, g)

    sys.stdout.write("Yes\n" if (mask & 1) else "No\n")


if __name__ == "__main__":
    solve()