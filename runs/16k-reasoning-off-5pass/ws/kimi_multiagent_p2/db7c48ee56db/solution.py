import sys
from itertools import combinations
from functools import reduce
from operator import xor

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2 + n]))

    # Complement trick: choosing K elements = all elements XOR the (N-K) unchosen.
    T = 0
    if k > n - k:
        for v in A:
            T ^= v
        k = n - k

    if k == 0:
        print(T)
        return

    mid = n // 2
    L = A[:mid]
    R = A[mid:]
    lenL, lenR = mid, n - mid

    ans = -1
    j_lo = max(0, k - lenR)
    j_hi = min(k, lenL)
    for j in range(j_lo, j_hi + 1):
        # XORs of all ways to pick j elements from the left half
        LA = [reduce(xor, c, 0) for c in combinations(L, j)]
        # XORs of all ways to pick k-j elements from the right half
        RB = [reduce(xor, c, 0) for c in combinations(R, k - j)]
        # |LA| * |RB| = C(mid, j) * C(n-mid, k-j) <= C(n, k) <= 1e6 total over all j
        for a in LA:
            ta = T ^ a
            for b in RB:
                v = ta ^ b
                if v > ans:
                    ans = v
    print(ans)

main()