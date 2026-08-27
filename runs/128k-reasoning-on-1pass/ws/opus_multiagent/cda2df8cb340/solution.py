import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = np.array(data[1:1 + n], dtype=np.int64)

    total = 2 * n * int(A.sum())

    for k in range(1, 25):
        mask = (1 << k) - 1
        r = A & mask
        rs = np.sort(r)
        comp = (-A) & mask
        cnt = (np.searchsorted(rs, comp, 'right') -
               np.searchsorted(rs, comp, 'left')).astype(np.int64)
        s = int((A * cnt).sum())
        if s == 0:
            continue
        term = 2 * s
        total -= term >> k

    D = int((A // (A & -A)).sum())
    sys.stdout.write(str((total + D) // 2) + "\n")


main()