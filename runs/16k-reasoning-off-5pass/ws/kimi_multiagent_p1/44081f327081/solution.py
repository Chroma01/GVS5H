import sys
from array import array

def main():
    data = sys.stdin.buffer.read()
    nums = []
    num = 0
    in_num = False
    for c in data:
        if 48 <= c <= 57:
            num = num * 10 + (c - 48)
            in_num = True
        else:
            if in_num:
                nums.append(num)
                num = 0
                in_num = False
    if in_num:
        nums.append(num)

    n, k = nums[0], nums[1]
    A = nums[2:2 + n]
    M = max(A) if A else 0

    try:
        import numpy as np
        freq = np.zeros(M + 1, dtype=np.int64)
        idx = np.array(A, dtype=np.int64)
        np.add.at(freq, idx, 1)
        cnt = np.zeros(M + 1, dtype=np.int64)
        for d in range(1, M + 1):
            cnt[d] = freq[d::d].sum()
        best = np.zeros(M + 1, dtype=np.int64)
        valid = np.nonzero(cnt >= k)[0]
        for d in valid:
            best[d::d] = d
        out = '\n'.join(map(str, best[idx].tolist())) + '\n'
        sys.stdout.write(out)
    except ImportError:
        freq = array('I', [0]) * (M + 1)
        for a in A:
            freq[a] += 1
        cnt = array('I', [0]) * (M + 1)
        for d in range(1, M + 1):
            s = 0
            for j in range(d, M + 1, d):
                s += freq[j]
            cnt[d] = s
        best = array('I', [0]) * (M + 1)
        for d in range(1, M + 1):
            if cnt[d] >= k:
                for j in range(d, M + 1, d):
                    best[j] = d
        write = sys.stdout.write
        for a in A:
            write(str(best[a]) + '\n')

main()