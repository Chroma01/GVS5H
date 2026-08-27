import sys

def main():
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())
    p_list = list(map(int, input().split()))

    def affordable(x):
        total = 0
        for p in p_list:
            k = (x // p + 1) // 2
            total += k * k * p
            if total > m:
                return False
        return True

    # This value is always infeasible.
    lo = 0
    hi = 2 * m + max(p_list)

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if affordable(mid):
            lo = mid
        else:
            hi = mid

    bought = 0
    spent = 0
    next_cost = None
    same_next_cost = 0

    for p in p_list:
        k = (lo // p + 1) // 2
        bought += k
        spent += k * k * p

        marginal = (2 * k + 1) * p
        if next_cost is None or marginal < next_cost:
            next_cost = marginal
            same_next_cost = 1
        elif marginal == next_cost:
            same_next_cost += 1

    extra = min(same_next_cost, (m - spent) // next_cost)
    print(bought + extra)

if __name__ == "__main__":
    main()