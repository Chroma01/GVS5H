import sys
from math import isqrt

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    # Safe upper bound for x:
    # For each p, let s = isqrt(M // p). Then p * (s + 1)^2 > M.
    # If x >= p * (2s + 1), product p alone contributes at least
    # p * (s + 1)^2 > M to F(x).  Taking the maximum over p gives H
    # with F(H) > M, so the answer x lies in [0, H].
    hi = 0
    for p in P:
        s = isqrt(M // p)
        th = p * (2 * s + 1)
        if th > hi:
            hi = th

    P.sort()  # ascending helps early break when F(mid) > M
    lo = 0
    high = hi
    M_val = M
    P_list = P

    # Binary search the largest x with F(x) <= M.
    while lo < high:
        mid = (lo + high + 1) >> 1
        total = 0
        for p in P_list:
            k = (mid + p) // (p << 1)
            if k:
                total += p * k * k
                if total > M_val:
                    break
        if total <= M_val:
            lo = mid
        else:
            high = mid - 1

    x = lo

    # Compute C(x) and F(x) at the found threshold.
    cost = 0
    cnt = 0
    for p in P_list:
        k = (x + p) // (p << 1)
        if k:
            cost += p * k * k
            cnt += k

    ans = cnt + (M - cost) // (x + 1)
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()