import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    P = list(map(int, input().split()))

    def calc(x):
        total_cost = 0
        total_count = 0

        for p in P:
            q = x // p
            k = (q + 1) // 2  # Number of odd multiples of p not exceeding x.
            total_count += k
            total_cost += k * k * p
            if total_cost > M:
                return total_cost, total_count

        return total_cost, total_count

    lo, hi = 0, M
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cost, _ = calc(mid)
        if cost <= M:
            lo = mid
        else:
            hi = mid - 1

    x = lo
    used_cost, answer = calc(x)
    remaining = M - used_cost

    if x < M:
        boundary_count = 0
        y = x + 1
        for p in P:
            q = y // p
            k_now = (q + 1) // 2

            q_prev = x // p
            k_prev = (q_prev + 1) // 2

            if k_now > k_prev:
                boundary_count += 1

        answer += min(boundary_count, remaining // y)

    print(answer)

if __name__ == "__main__":
    solve()