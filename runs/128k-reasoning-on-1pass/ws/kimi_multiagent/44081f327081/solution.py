import sys
from array import array

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    A = array('i', map(int, data[2:2 + n]))
    del data

    M = max(A)

    # freq[x] = number of occurrences of value x
    cnt = [0] * (M + 1)
    for a in A:
        cnt[a] += 1

    # In-place ascending sieve: after processing d, cnt[d] = number of
    # array elements divisible by d. Safe because multiples of d are >= d,
    # and only indices < d have been overwritten so far.
    for d in range(1, M + 1):
        cnt[d] = sum(cnt[d::d])

    # best[x] = largest d with d | x and cnt[d] >= K.
    # Ascending d means larger feasible d overwrites smaller ones.
    best = [0] * (M + 1)
    for d in range(1, M + 1):
        if cnt[d] >= k:
            best[d::d] = [d] * (M // d)

    out = sys.stdout.write
    buf = []
    ap = buf.append
    for a in A:
        ap(str(best[a]))
        if len(buf) >= 65536:
            out('\n'.join(buf) + '\n')
            buf.clear()
    if buf:
        out('\n'.join(buf) + '\n')

main()