import sys
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    import numpy as np
    a = np.array(A, dtype=np.int64)

    total = int(a.sum())
    # S_0 = sum over i<=j of (A_i + A_j) = (N+1) * sum(A)
    ans = (n + 1) * total

    # For t = 1..22 use bincount on residues mod 2^t
    for t in range(1, 23):
        M = 1 << t
        r = a % M
        c = np.bincount(r, minlength=M)                      # int64 counts
        v = np.bincount(r, weights=a.astype(np.float64), minlength=M).astype(np.int64)
        # residue 0 paired with itself: sum_{i<=j in class} (ai+aj) = (c+1)*v
        St = int((c[0] + 1) * v[0])
        half = M >> 1
        # residue M/2 paired with itself
        St += int((c[half] + 1) * v[half])
        # residues r and M-r for 1 <= r < M/2
        if half > 1:
            rr = np.arange(1, half, dtype=np.int64)
            ss = M - rr
            cross = (v[rr] * c[ss] + v[ss] * c[rr]).sum()
            St += int(cross)
        # 2^t divides St exactly
        ans -= St >> t

    # For t = 23, 24: modulus large; a+b must equal k*2^t (k*2^t <= 2*10^7)
    cnt = Counter(A)
    items = list(cnt.items())
    max_sum = 2 * 10**7
    for t in (23, 24):
        M = 1 << t
        St = 0
        k = 1
        while k * M <= max_sum:
            T = k * M
            pairs = 0
            h = T >> 1
            for x, cx in items:
                if x < h:
                    cy = cnt.get(T - x)
                    if cy:
                        pairs += cx * cy
            if T % 2 == 0:
                ch = cnt.get(h, 0)
                pairs += ch * (ch + 1) // 2
            St += T * pairs
            k += 1
        ans -= St >> t

    print(ans)

main()