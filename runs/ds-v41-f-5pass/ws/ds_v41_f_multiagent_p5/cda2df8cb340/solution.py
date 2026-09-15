import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    if n == 0:
        sys.stdout.write("0\n")
        return

    # f(x) = odd part of x.  Answer = sum over i<=j of oddpart(A_i + A_j).
    # Group pairs by k = v2(A_i + A_j); each contributes (A_i + A_j) / 2^k.
    # v2(x) == k  <=>  x == 2^k  (mod 2^{k+1}).
    maxsum = max(A) * 2
    kmax = maxsum.bit_length()          # possible k are 0 .. kmax-1

    SHIFT = 42                          # per-residue sum <= N*maxA = 2e12 < 2^42
    LOW = (1 << SHIFT) - 1
    ONE = 1 << SHIFT

    total = 0
    for k in range(kmax):
        mask = (1 << (k + 1)) - 1
        target = 1 << k
        pair_sum = 0
        diag_c = 0

        if mask < (1 << 20):
            d = [0] * (mask + 1)
            for a in A:
                r = a & mask
                comp = (target - r) & mask
                w = d[comp]
                if w:
                    pair_sum += a * (w >> SHIFT) + (w & LOW)
                if r == comp:
                    diag_c += a << 1
                d[r] += ONE + a
        else:
            d = {}
            dget = d.get
            for a in A:
                r = a & mask
                comp = (target - r) & mask
                w = dget(comp)
                if w is not None:
                    pair_sum += a * (w >> SHIFT) + (w & LOW)
                if r == comp:
                    diag_c += a << 1
                w2 = dget(r)
                if w2 is None:
                    d[r] = ONE + a
                else:
                    d[r] = w2 + ONE + a

        total += (pair_sum + diag_c) >> k

    sys.stdout.write(str(total) + "\n")


main()