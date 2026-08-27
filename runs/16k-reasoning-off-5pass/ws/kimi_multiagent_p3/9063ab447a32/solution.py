import sys
from math import isqrt

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = list(map(int, data[2:2 + n]))

    pmin = min(P)

    # For marginal threshold X, product i contributes k_i = (X // p + 1) // 2 units
    # (all k >= 1 with (2k-1)*p <= X). Sum of those marginals = k_i^2 * p.
    # Early break once cost exceeds M to keep big-int arithmetic cheap.
    def evaluate(X):
        total_cost = 0
        total_cnt = 0
        for p in P:
            k = (X // p + 1) // 2
            if k:
                total_cnt += k
                total_cost += k * k * p
                if total_cost > M:
                    return total_cnt, total_cost
        return total_cnt, total_cost

    # Binary search the maximal integer X with cost(X) <= M.
    # lo = 0 is always feasible (cost 0 <= M since M >= 1).
    # hi is infeasible: cheapest product alone costs >= hi^2/(4*pmin) > M.
    lo = 0
    hi = 2 * isqrt(M * pmin) + 10
    while lo < hi:
        mid = (lo + hi + 1) // 2
        _, c = evaluate(mid)
        if c <= M:
            lo = mid
        else:
            hi = mid - 1

    X = lo
    cnt, cost = evaluate(X)
    R = M - cost

    # Cheapest next marginal across all products.
    v = 1 << 62  # large sentinel; will be overwritten
    for p in P:
        k = (X // p + 1) // 2
        nxt = (2 * k + 1) * p
        if nxt < v:
            v = nxt

    # R // v < number of products offering marginal v (else X wasn't maximal),
    # so exactly R // v extra units can be bought.
    ans = cnt + R // v
    sys.stdout.write(str(ans) + "\n")

main()