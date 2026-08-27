import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    m = data[1]
    p = data[2:]

    def feasible(x):
        total = 0
        for price in p:
            k = (x // price + 1) // 2
            total += price * k * k
            if total > m:
                return False
        return True

    # Find the greatest integer threshold x such that buying every
    # marginal unit costing at most x is within the budget.
    lo = 0
    hi = m + 1  # exclusive, always enough because any useful marginal cost <= M

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    threshold = lo

    count = 0
    spent = 0
    next_cost = None

    for price in p:
        # Odd multiples of price are the marginal costs:
        # price, 3*price, 5*price, ...
        k = (threshold // price + 1) // 2
        count += k
        spent += price * k * k

        nxt = (2 * k + 1) * price
        if next_cost is None or nxt < next_cost:
            next_cost = nxt

    # All still-unselected units cost at least next_cost.  The cheapest
    # remaining units are exactly the products whose next marginal cost
    # equals next_cost, and the binary-search maximality guarantees that
    # the remaining budget cannot buy all of them.
    count += (m - spent) // next_cost

    print(count)


if __name__ == "__main__":
    main()