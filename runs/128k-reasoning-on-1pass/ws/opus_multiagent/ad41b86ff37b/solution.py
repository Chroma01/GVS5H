import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    if n < 3:
        # Not possible under constraints, but guard anyway.
        print(0)
        return
    arr = np.array(data[1:2 * (n - 1) + 1], dtype=np.int64)
    u = arr[0::2]
    v = arr[1::2]

    deg = np.bincount(np.concatenate([u, v]), minlength=n + 1).astype(np.int64)

    src = np.concatenate([u, v])
    dst = np.concatenate([v, u])
    val = deg[dst] - 1  # number of leaves middle vertex dst can supply

    order = np.lexsort((-val, src))
    s = src[order]
    w = val[order]

    start = np.searchsorted(s, s, side='left')
    idx = np.arange(s.shape[0], dtype=np.int64)
    rank = idx - start + 1  # 1-based rank within group (sorted desc by val)

    mask = w >= 1
    if not mask.any():
        best = 3
    else:
        cand = 1 + rank[mask] * (w[mask] + 1)
        best = int(cand.max())
        if best < 3:
            best = 3

    print(n - best)


main()