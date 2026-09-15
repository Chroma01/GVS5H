import sys
from itertools import accumulate

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    maxA = max(A)
    max_sum = 2 * maxA
    
    # sum of f(2*A_i) = sum of odd part of A_i
    diag = 0
    for a in A:
        diag += a // (a & -a)
    
    # bit reversal table for 8 bits
    rev8 = [0] * 256
    for i in range(1, 256):
        rev8[i] = (rev8[i >> 1] >> 1) | ((i & 1) << 7)
    
    def revkey(a):
        return (rev8[a & 255] << 24) | (rev8[(a >> 8) & 255] << 16) | (rev8[(a >> 16) & 255] << 8) | rev8[(a >> 24) & 255]
    
    # sort by bit-reversed order (low bits first)
    sA = sorted(A, key=revkey)
    pre = [0] + list(accumulate(sA))
    
    total = 0
    T_max = max_sum.bit_length() - 1
    blocks = [(0, n, 0)]  # (start, end, residue mod 2^t)
    
    for t in range(T_max + 1):
        bit = 1 << t
        if bit <= maxA:
            new_blocks = []
            for (l, r, res) in blocks:
                # binary search for first index with bit t set
                lo, hi = l, r
                while lo < hi:
                    mid = (lo + hi) >> 1
                    if sA[mid] & bit:
                        hi = mid
                    else:
                        lo = mid + 1
                if lo > l:
                    new_blocks.append((l, lo, res))
                if lo < r:
                    new_blocks.append((lo, r, res + bit))
            blocks = new_blocks
        
        half = bit
        M = bit << 1
        mask = M - 1
        
        cnt = {}
        sm = {}
        for (l, r, res) in blocks:
            cnt[res] = r - l
            sm[res] = pre[r] - pre[l]
        
        for res, c in cnt.items():
            m = (half - res) & mask
            cm = cnt.get(m)
            if cm is not None:
                total += (cm * sm[res] + c * sm[m]) // half
    
    sys.stdout.write(str((total + diag) // 2))

main()