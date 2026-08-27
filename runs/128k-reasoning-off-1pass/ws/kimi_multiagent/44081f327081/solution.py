import sys
from array import array

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = data[2:]
    M = 0
    for tok in A:
        v = int(tok)
        if v > M:
            M = v

    # freq[x] = number of elements equal to x
    freq = array('i', bytes(4 * (M + 1)))
    for tok in A:
        freq[int(tok)] += 1

    # cnt[d] = number of elements divisible by d, via C-speed stepped-slice sums
    cnt = array('i', bytes(4 * (M + 1)))
    for d in range(1, M + 1):
        cnt[d] = sum(freq[d::d])

    # best[x] = largest divisor d of x with cnt[d] >= K
    # iterate d ascending so larger qualifying d overwrites smaller ones,
    # using C-speed stepped slice assignment.
    best = array('i', bytes(4 * (M + 1)))
    for d in range(1, M + 1):
        if cnt[d] >= K:
            best[d::d] = array('i', [d]) * (M // d)

    out = []
    for tok in A:
        out.append(str(best[int(tok)]))
    sys.stdout.write('\n'.join(out) + '\n')

solve()