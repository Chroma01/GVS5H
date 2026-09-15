import sys
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = data[pos:pos + N]; pos += N
    B = data[pos:pos + N]; pos += N
    C = list(map(int, data[pos:pos + N])); pos += N

    Moff = []   # A=1,B=0 : must be turned off once
    Mon = []    # A=0,B=1 : must be turned on once
    Opt = []    # A=1,B=1 : leave, or turn off then on
    for i in range(N):
        ai = A[i]
        bi = B[i]
        ci = C[i]
        if ai == b'1':
            if bi == b'1':
                Opt.append(ci)
            else:
                Moff.append(ci)
        else:
            if bi == b'1':
                Mon.append(ci)
            # A=0,B=0 : never flip

    def pair_min(lst):
        # sum over all unordered pairs of the smaller value
        lst.sort()
        L = len(lst)
        s = 0
        for i in range(L):
            s += lst[i] * (L - 1 - i)
        return s

    m = len(Moff)
    n = len(Mon)
    a = m + n
    SO = sum(Opt)

    C0 = pair_min(Moff) + pair_min(Mon) + sum(Mon)
    K0 = C0 + SO * a          # cost with no Opt flipped

    mandatory = sorted(Moff + Mon)
    pref = [0] * (a + 1)
    for i in range(a):
        pref[i + 1] = pref[i] + mandatory[i]

    opts = []
    for v in Opt:
        k = bisect_right(mandatory, v)           # number of mandatory <= v
        g = pref[k] + v * (a - k)                # = sum_mandatory min(mand, v)
        beta = g + 2 * SO - (a + 1) * v
        opts.append((v, beta))

    opts.sort()                                   # ascending by value
    best = K0
    cur = K0
    chosen_sum = 0
    for v, beta in reversed(opts):                # add optional of largest cost first
        cur += beta - 2 * chosen_sum
        chosen_sum += v
        if cur < best:
            best = cur

    print(best)


main()