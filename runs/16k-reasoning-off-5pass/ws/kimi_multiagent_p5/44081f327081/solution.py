import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); K = int(data[1])
    A = list(map(int, data[2:2 + n]))
    M = max(A)

    try:
        import numpy as np
        freq = np.bincount(A, minlength=M + 1)
        cnt = np.zeros(M + 1, dtype=np.int64)
        # cnt[d] = number of elements divisible by d
        for d in range(1, M + 1):
            cnt[d] = freq[d::d].sum()
        good = cnt >= K
        best = np.zeros(M + 1, dtype=np.int64)
        # best[v] = largest divisor d of v with cnt[d] >= K
        # ascending d with maximum works since larger d overwrites smaller
        idx = np.nonzero(good)[0]
        for d in idx:
            if d:
                best[d::d] = np.maximum(best[d::d], d)
        out = '\n'.join(map(str, best[np.array(A)].tolist()))
        sys.stdout.write(out + '\n')
    except ImportError:
        # Pure Python fallback
        freq = [0] * (M + 1)
        for a in A:
            freq[a] += 1
        cnt = [0] * (M + 1)
        for d in range(1, M + 1):
            s = 0
            for m in range(d, M + 1, d):
                s += freq[m]
            cnt[d] = s
        best = [0] * (M + 1)
        for d in range(1, M + 1):
            if cnt[d] >= K:
                for m in range(d, M + 1, d):
                    if best[m] < d:
                        best[m] = d
        sys.stdout.write('\n'.join(map(str, (best[a] for a in A))) + '\n')

solve()