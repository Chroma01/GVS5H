import sys


def solve() -> None:
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    last = [0] * (n + 2)
    distinct_sum = 0
    adjacent_sum = 0
    answer = 0

    for r, v in enumerate(a, 1):
        old = last[v]

        # The contribution of value v to the sum over all left endpoints
        # changes from old to r.
        distinct_sum += r - old

        # Update adjacency pairs (v-1, v) and (v, v+1).
        if v > 1:
            adjacent_sum -= min(last[v - 1], old)
            adjacent_sum += min(last[v - 1], r)

        if v < n:
            adjacent_sum -= min(old, last[v + 1])
            adjacent_sum += min(r, last[v + 1])

        last[v] = r

        # Sum of f(L, r) over all 1 <= L <= r.
        answer += distinct_sum - adjacent_sum

    print(answer)


if __name__ == "__main__":
    solve()