import sys


def solve_array(A):
    n = len(A)
    last = [0] * (n + 2)  # sentinels at 0 and n+1

    sum_last = 0   # sum_v last[v]
    sum_min = 0    # sum_v min(last[v], last[v+1])
    ans = 0

    for r, x in enumerate(A, 1):
        p = last[x]

        # last[x] changes from p to r.
        sum_last += r - p

        # Pair (x-1, x): new min is last[x-1], because r is larger than it.
        left = last[x - 1]
        if left >= p:
            sum_min += left - p

        # Pair (x, x+1): new min is last[x+1], because r is larger than it.
        right = last[x + 1]
        if right >= p:
            sum_min += right - p

        last[x] = r

        # For this right endpoint:
        # sum_L f(L, r) = sum_L distinct_count - sum_L adjacent_pair_count
        ans += sum_last - sum_min

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    A = data[1:1 + n]
    print(solve_array(A))


def brute(A):
    """Small O(N^2) validator."""
    total = 0
    n = len(A)

    for L in range(n):
        present = set()
        blocks = 0

        for R in range(L, n):
            x = A[R]
            if x not in present:
                delta = 1
                if x - 1 in present:
                    delta -= 1
                if x + 1 in present:
                    delta -= 1
                blocks += delta
                present.add(x)

            total += blocks

    return total


def validate():
    import random

    random.seed(123456789)

    for _ in range(500):
        n = random.randint(1, 8)
        A = [random.randint(1, n) for _ in range(n)]
        got = solve_array(A)
        exp = brute(A)
        if got != exp:
            print("FAIL", A, got, exp)
            return

    edge_cases = [
        [1],
        [1, 1, 1],
        [1, 2, 3],
        [3, 2, 1],
        [1, 3, 2, 4],
        [2, 4, 3, 1],
    ]

    for A in edge_cases:
        got = solve_array(A)
        exp = brute(A)
        if got != exp:
            print("FAIL", A, got, exp)
            return

    print("OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--validate":
        validate()
    else:
        main()