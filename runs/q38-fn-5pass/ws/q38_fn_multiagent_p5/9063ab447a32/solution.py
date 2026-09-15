import sys
from bisect import bisect_right
from math import isqrt


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    P = data[2:2 + N]
    del data

    P.sort()

    # Products with P_i > M can never be bought.
    vals = []
    cnts = []
    for p in P:
        if p > M:
            break
        if vals and vals[-1] == p:
            cnts[-1] += 1
        else:
            vals.append(p)
            cnts.append(1)

    if not vals:
        print(0)
        return

    m = len(vals)

    # Prefix sums of P*count and count, for quotient-block aggregation.
    prefW = [0] * (m + 1)
    prefC = [0] * (m + 1)
    sw = sc = 0
    for i in range(m):
        sw += vals[i] * cnts[i]
        sc += cnts[i]
        prefW[i + 1] = sw
        prefC[i + 1] = sc

    del P, cnts

    minP = vals[0]
    last = vals[-1]

    # Safe exclusive upper bound: at hi, the cheapest product alone costs > M.
    k = isqrt(M // minP)
    hi = minP * (2 * k + 1) + 1

    br = bisect_right

    def cost_leq(t, V=vals, PW=prefW, budget=M, br=br, last=last, m=m):
        end = m if t >= last else br(V, t)
        cost = 0
        i = 0
        while i < end:
            p = V[i]
            q = t // p
            c = (q + 1) >> 1
            limit = t // q
            if limit >= last:
                j = end
            else:
                j = br(V, limit, i, end)

            cost += c * c * (PW[j] - PW[i])
            if cost > budget:
                return False
            i = j
        return True

    # Largest t such that the total cost of all marginal costs <= t is <= M.
    lo = 0
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if cost_leq(mid):
            lo = mid
        else:
            hi = mid

    t = lo

    # Compute units and cost exactly at threshold t.
    end = m if t >= last else br(vals, t)
    units = 0
    cost = 0
    i = 0
    V = vals
    PW = prefW
    PC = prefC

    while i < end:
        p = V[i]
        q = t // p
        c = (q + 1) >> 1
        limit = t // q
        if limit >= last:
            j = end
        else:
            j = br(V, limit, i, end)

        units += c * (PC[j] - PC[i])
        cost += c * c * (PW[j] - PW[i])
        i = j

    # The next marginal cost is t+1; remaining budget buys that many units.
    ans = units + (M - cost) // (t + 1)
    print(ans)


if __name__ == "__main__":
    solve()