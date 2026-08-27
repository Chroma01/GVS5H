import sys
from array import array

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    A = data[2:2 + n]
    M = 0
    # find max while converting
    vals = A  # bytes objects
    # Build freq
    # First pass to get M
    # (convert lazily)
    # To avoid double conversion cost concerns, just convert once into a list of ints.
    a = [int(x) for x in vals]
    for v in a:
        if v > M:
            M = v
    size = M + 1
    freq = array('I', bytes(4 * size))
    for v in a:
        freq[v] += 1

    # cnt[d] = number of elements divisible by d, via slice sums (C speed)
    cnt = array('I', bytes(4 * size))
    for d in range(1, size):
        cnt[d] = sum(freq[d::d])

    # best[v] = largest d dividing v with cnt[d] >= K
    best = array('I', bytes(4 * size))
    # number of distinct values present (for early termination)
    remaining = 0
    for v in a:
        pass
    # count distinct via freq
    remaining = sum(1 for v in range(size) if freq[v] > 0)

    for d in range(M, 0, -1):
        if cnt[d] >= k:
            for m in range(d, size, d):
                if best[m] == 0:
                    best[m] = d
                    if freq[m]:
                        remaining -= 1
                        if remaining == 0:
                            break
            if remaining == 0:
                break

    out = '\n'.join(str(best[v]) for v in a)
    sys.stdout.write(out + '\n')

solve()