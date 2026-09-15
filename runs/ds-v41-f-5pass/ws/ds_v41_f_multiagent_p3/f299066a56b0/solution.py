import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    # Feasibility is monotone in K: if K pairs are possible, so are K-1.
    # Proof: for K-1, the required bottoms A[(N-(K-1)) + i] = A[N-K+1+i]
    # are >= those for K, A[N-K+i], so the K-condition implies the K-1 one.
    lo, hi = 0, n // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        base = n - mid
        ok = True
        for i in range(mid):
            if a[i] * 2 > a[base + i]:
                ok = False
                break
        if ok:
            lo = mid
        else:
            hi = mid - 1

    sys.stdout.write(str(lo) + "\n")

main()