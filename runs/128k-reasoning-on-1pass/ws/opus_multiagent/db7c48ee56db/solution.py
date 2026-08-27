import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    vals = list(map(int, data[2:2 + n]))
    A = np.array(vals, dtype=np.int64)

    tot = 0
    for v in vals:
        tot ^= v

    m = min(k, n - k)
    use_comp = (m != k)

    if m == 0:
        # K == N (choose everything) -> XOR of all
        sys.stdout.write(str(tot) + "\n")
        return

    if m == 1:
        if use_comp:
            ans = int((A ^ np.int64(tot)).max())
        else:
            ans = int(A.max())
        sys.stdout.write(str(ans) + "\n")
        return

    # m >= 2  => C(n,m) <= 1e6 forces n to be small (<= ~1414)
    # Layer 1: subsets of size 1, flat array ordered by last index
    F = A.copy()
    # off[t] = number of subsets in current layer whose last index < t
    off = np.arange(n, dtype=np.int64)

    for _ in range(m - 1):
        parts = []
        for t in range(n):
            o = int(off[t])
            if o:
                parts.append(F[:o] ^ A[t])
        cnt = off.copy()  # new count for last index t equals old off[t]
        if parts:
            F = np.concatenate(parts)
        else:
            F = np.empty(0, dtype=np.int64)
        # exclusive prefix sums of cnt
        c = np.cumsum(cnt)
        off = np.empty(n, dtype=np.int64)
        off[0] = 0
        if n > 1:
            off[1:] = c[:-1]

    if use_comp:
        ans = int((F ^ np.int64(tot)).max())
    else:
        ans = int(F.max())
    sys.stdout.write(str(ans) + "\n")


main()