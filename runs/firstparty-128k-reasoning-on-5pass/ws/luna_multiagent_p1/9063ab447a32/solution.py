import sys
from math import isqrt


def solve() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    p = list(map(int, input().split()))

    min_p = min(p)

    # Choose an infeasible threshold. If k units of the cheapest product
    # already cost more than M, its k-th marginal cost is infeasible.
    k = isqrt(m // min_p) + 1
    hi = min_p * (2 * k - 1)
    lo = 0  # C(0) = 0 is feasible

    def feasible(x: int) -> bool:
        total = 0
        for cost_per_square in p:
            q = ((x // cost_per_square) + 1) // 2
            total += cost_per_square * q * q
            if total > m:
                return False
        return True

    # Find the largest integer threshold X whose selected marginal costs
    # have total cost at most M.
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    x = lo
    total_cost = 0
    answer = 0
    next_cost = None

    for cost_per_square in p:
        q = ((x // cost_per_square) + 1) // 2
        answer += q
        total_cost += cost_per_square * q * q
        marginal = cost_per_square * (2 * q + 1)
        if next_cost is None or marginal < next_cost:
            next_cost = marginal

    # Any additionally affordable units have the minimum next marginal cost.
    # The maximality of X guarantees that the number added this way does not
    # pass the available products whose next marginal has that same cost.
    answer += (m - total_cost) // next_cost

    print(answer)


if __name__ == "__main__":
    solve()