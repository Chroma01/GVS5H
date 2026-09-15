import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]

    # Safe upper bound for the marginal-cost cutoff X.
    # The next unselected marginal cost of product i is at most
    # P_i * (2 * floor(sqrt(M / P_i)) + 1).
    upper = max(P)
    for p in P:
        r = math.isqrt(M // p)
        v = p * (2 * r + 1)
        if v > upper:
            upper = v

    budget = M
    P_list = P

    def affordable(x):
        total = 0
        for p in P_list:
            k = (x // p + 1) >> 1
            if k:
                total += p * k * k
                if total > budget:
                    return False
        return True

    lo = 0
    hi = upper
    while lo < hi:
        mid = (lo + hi + 1) >> 1
        if affordable(mid):
            lo = mid
        else:
            hi = mid - 1

    x = lo
    total = 0
    units = 0
    for p in P_list:
        k = (x // p + 1) >> 1
        if k:
            units += k
            total += p * k * k

    ans = units + (budget - total) // (x + 1)
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()