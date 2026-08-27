import sys
from array import array

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    a = data[2:]
    M = 0
    vals = [0] * n
    for i in range(n):
        v = int(a[i])
        vals[i] = v
        if v > M:
            M = v

    freq = array('i', [0]) * (M + 1)
    for v in vals:
        freq[v] += 1

    # cnt[d] = number of elements divisible by d
    cnt = array('i', [0]) * (M + 1)
    fr = freq
    cn = cnt
    for d in range(1, M + 1):
        s = 0
        for m in range(d, M + 1, d):
            s += fr[m]
        cn[d] = s

    # best[x] = max divisor d of x with cnt[d] >= K
    best = array('i', [0]) * (M + 1)
    bs = best
    for d in range(1, M + 1):
        if cn[d] >= k:
            for m in range(d, M + 1, d):
                bs[m] = d  # d ascending -> last write is largest valid divisor

    out = '\n'.join(str(bs[v]) for v in vals)
    sys.stdout.write(out + '\n')

main()