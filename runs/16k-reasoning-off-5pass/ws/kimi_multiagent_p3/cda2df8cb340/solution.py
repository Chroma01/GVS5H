import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = np.fromiter((int(x) for x in data[1:1 + n]), dtype=np.int64, count=n)
    maxA = int(A.max())
    maxSum = 2 * maxA
    kmax = maxSum.bit_length() - 1  # largest k with 2^k <= maxSum

    ans = 0
    KRES = 20  # residue-array method for k <= 20 (modulus <= 2^21)

    # distinct-value counts for the large-k candidate method (built lazily)
    cnt0 = None
    vals = None
    vc = None

    for k in range(kmax + 1):
        t = 1 << k
        if k <= KRES:
            m = t << 1
            res = A % m
            cnt = np.bincount(res, minlength=m)                       # int64
            sval = np.bincount(res, weights=A, minlength=m).astype(np.int64)
            r2 = (t - np.arange(m)) & (m - 1)
            # ordered sum of (a+b) over pairs with a+b ≡ 2^k (mod 2^{k+1})
            O = int((cnt * sval[r2]).sum() + (sval * cnt[r2]).sum())
            if k == 0:
                D = 0
            else:
                # residues with 2r ≡ 2^k (mod 2^{k+1}): r = 2^{k-1}, 2^{k-1}+2^k
                D = 2 * (int(sval[t >> 1]) + int(sval[(t >> 1) + t]))
            pair_sum = (O + D) // 2  # convert ordered -> i<=j
            ans += pair_sum >> k
        else:
            if cnt0 is None:
                cnt0 = np.bincount(A, minlength=maxA + 1).astype(np.int32)
                vals = np.nonzero(cnt0)[0]
                vc = cnt0[vals].astype(np.int64)
            step = t << 1
            s = t
            while s <= maxSum:
                b = s - vals
                mask = (b >= 1) & (b <= maxA)
                # ordered pairs (i,j) with A_i + A_j = s
                oc = int((vc[mask] * cnt0[b[mask]]).sum())
                d = int(cnt0[s >> 1]) if (s & 1) == 0 else 0  # diagonal i=j count
                pairs = (oc + d) // 2
                ans += (s >> k) * pairs  # f(s) = s / 2^k since v2(s) = k
                s += step

    print(ans)

main()