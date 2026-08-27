import sys
from array import array

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    # read the sequence
    A = array('I', map(int, it))

    maxA = max(A) if A else 0
    M = maxA

    # frequency of each value
    freq = array('I', [0]) * (M + 1)
    for a in A:
        freq[a] += 1

    # cnt[d] = how many array elements are divisible by d
    cnt = array('I', [0]) * (M + 1)
    freq_local = freq
    cnt_local = cnt
    for d in range(1, M + 1):
        s = 0
        step = d
        for m in range(d, M + 1, step):
            s += freq_local[m]
        cnt_local[d] = s

    # ans[v] = largest divisor d of v with cnt[d] >= K
    ans = array('I', [0]) * (M + 1)
    ans_local = ans
    cnt_local2 = cnt
    K_local = K
    for d in range(M, 0, -1):
        if cnt_local2[d] >= K_local:
            step = d
            for m in range(d, M + 1, step):
                if ans_local[m] == 0:
                    ans_local[m] = d

    # output answers in original order
    out = '\n'.join(str(ans_local[a]) for a in A)
    sys.stdout.write(out)


if __name__ == "__main__":
    solve()