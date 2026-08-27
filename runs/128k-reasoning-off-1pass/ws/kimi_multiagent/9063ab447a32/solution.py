import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = int(data[1])
    P = [int(x) for x in data[2:2 + n]]
    twoP = [2 * p for p in P]

    # For a marginal-cost threshold lam, product i can supply
    # k_i = floor((lam + P_i) / (2 P_i)) units whose marginal cost (2j-1)*P_i <= lam.
    # Returns (count, cost); cost is capped early once it exceeds M.
    def feasible(lam):
        s = 0
        for p, tp in zip(P, twoP):
            k = (lam + p) // tp
            if k:
                s += k * k * p
                if s > M:
                    return False
        return True

    # Binary search: largest lam such that total cost of all units
    # with marginal cost <= lam is <= M.
    lo = 0
    hi = 2 * 10**21  # safely above any needed marginal cost
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    lam = lo
    ks = [(lam + p) // tp for p, tp in zip(P, twoP)]
    count = 0
    spent = 0
    for k, p in zip(ks, P):
        count += k
        spent += k * k * p
    R = M - spent

    # Cheapest next unit among all products
    mu = min((2 * k + 1) * p for k, p in zip(ks, P))
    cnt_mu = 0
    for k, p in zip(ks, P):
        if (2 * k + 1) * p == mu:
            cnt_mu += 1

    ans = count + min(cnt_mu, R // mu)
    sys.stdout.write(str(ans) + "\n")

main()