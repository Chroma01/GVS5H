import sys

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    M = int(data[p]); p += 1
    A = int(data[p]); p += 1
    B = int(data[p]); p += 1
    ivs = []
    for _ in range(M):
        L = int(data[p]); p += 1
        R = int(data[p]); p += 1
        ivs.append((L, R))

    full = (1 << B) - 1

    # A bad block of length >= B can never be crossed.
    for L, R in ivs:
        if R - L + 1 >= B:
            sys.stdout.write("No\n")
            return

    # Boolean transition matrix for one GOOD position.
    # State vector v: bit k = reachability of position (cur - k), k = 0..B-1.
    base = [0] * B
    base[0] = ((1 << (B - A + 1)) - 1) << (A - 1)   # v'_0 = OR of bits A-1..B-1
    for k in range(1, B):
        base[k] = 1 << (k - 1)                      # v'_k = v_{k-1}
    base = tuple(base)

    def matmul(X, Y):
        C = [0] * B
        for i in range(B):
            a = X[i]
            r = 0
            while a:
                low = a & (-a)
                r |= Y[low.bit_length() - 1]
                a ^= low
            C[i] = r
        return tuple(C)

    LOG = N.bit_length() + 1
    pows = [base]
    for _ in range(LOG):
        pows.append(matmul(pows[-1], pows[-1]))

    BITS = [1 << j for j in range(B)]

    def apply(v, L):
        if v == 0 or v == full:
            return v
        t = 0
        while L:
            if L & 1:
                rows = pows[t]
                r = 0
                for j in range(B):
                    if rows[j] & v:
                        r |= BITS[j]
                v = r
                if v == 0 or v == full:
                    return v
            L >>= 1
            t += 1
        return v

    mask = 1          # window ending at position 1: reach[1] = 1
    prev = 2
    for L, R in ivs:
        gl = L - prev                    # good run [prev, L-1]
        if gl > 0:
            mask = apply(mask, gl)
            if mask == 0:
                sys.stdout.write("No\n")
                return
        blen = R - L + 1                 # all bad positions are unreachable
        mask = (mask << blen) & full
        if mask == 0:
            sys.stdout.write("No\n")
            return
        prev = R + 1

    gl = N - prev + 1                    # final good run [prev, N]
    if gl > 0:
        mask = apply(mask, gl)

    sys.stdout.write("Yes\n" if (mask & 1) else "No\n")

main()