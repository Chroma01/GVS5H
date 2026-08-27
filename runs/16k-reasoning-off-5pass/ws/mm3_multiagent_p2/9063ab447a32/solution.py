import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    # Helper to compute total cost of taking all items with marginal cost <= T
    def total_cost(T):
        total = 0
        m = M
        for p in P:
            q = T // p
            cnt = (q + 1) // 2
            total += p * cnt * cnt
            if total > m:
                return total  # early exit
        return total

    # Binary search for the smallest T such that total_cost(T) > M
    low = 0
    high = 2 * 10**18  # safe upper bound

    # Ensure high is sufficient (optional safety)
    # while total_cost(high) <= M:
    #     high *= 2

    while low < high:
        mid = (low + high) // 2
        if total_cost(mid) > M:
            high = mid
        else:
            low = mid + 1
    T_star = low  # smallest T with total_cost(T) > M

    # Compute cnt_less and sum_less for T = T_star - 1
    T_less = T_star - 1
    cnt_less = 0
    sum_less = 0
    for p in P:
        q = T_less // p
        cnt = (q + 1) // 2
        cnt_less += cnt
        sum_less += p * cnt * cnt

    # Compute g(T_star): number of items with marginal cost exactly T_star
    g_T = 0
    for p in P:
        if T_star % p == 0 and (T_star // p) % 2 == 1:
            g_T += 1

    remaining = M - sum_less
    take = 0
    if T_star > 0:
        take = min(g_T, remaining // T_star)
    answer = cnt_less + take

    print(answer)

if __name__ == "__main__":
    solve()