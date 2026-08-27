import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it)
    M = next(it)
    P = [next(it) for _ in range(N)]

    # total cost of all units whose price is strictly less than X
    def cost_lt(X: int) -> int:
        total = 0
        for p in P:
            q = (X - 1) // p
            t = (q + 1) // 2
            total += p * t * t
            if total > M:
                break
        return total

    # find the largest X such that cost_lt(X) <= M
    lo = 0          # always feasible (cost of empty set = 0)
    hi = 1
    while cost_lt(hi) <= M:
        lo = hi
        hi <<= 1

    # binary search on [lo, hi]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost_lt(mid) <= M:
            lo = mid
        else:
            hi = mid - 1
    X = lo                     # X is the maximal threshold described in the proof

    # compute the answer for this X
    cnt_lt = 0        # number of units cheaper than X
    cost_lt_val = 0   # their total price
    cnt_eq = 0        # units whose price equals exactly X

    for p in P:
        q = (X - 1) // p
        t = (q + 1) // 2
        cnt_lt += t
        cost_lt_val += p * t * t
        if X > 0 and (X % p == 0) and ((X // p) & 1):
            cnt_eq += 1

    remaining = M - cost_lt_val                 # money left after buying all cheaper units
    add = 0
    if X > 0:
        add = min(cnt_eq, remaining // X)

    print(cnt_lt + add)


if __name__ == "__main__":
    solve()