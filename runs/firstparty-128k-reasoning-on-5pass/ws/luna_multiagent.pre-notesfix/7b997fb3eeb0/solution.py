import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    # c[i] = first index j >= i such that A[j] >= 2*A[i], adjusted
    # so that c[i] is the required distance from i to a valid bottom.
    c = [bisect_left(a, 2 * a[i]) - i for i in range(n)]

    # Sparse table for range maximum queries on c.
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i // 2] + 1

    st = [c]
    level = 1
    while (1 << level) <= n:
        prev = st[-1]
        length = n - (1 << level) + 1
        half = 1 << (level - 1)
        curr = [
            max(prev[i], prev[i + half])
            for i in range(length)
        ]
        st.append(curr)
        level += 1

    def range_max(left, right):
        """Maximum on c[left:right], with right exclusive."""
        length = right - left
        k = log[length]
        span = 1 << k
        return max(st[k][left], st[k][right - span])

    q = int(input())
    answers = []

    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1

        m = r - l + 1
        low, high = 0, m // 2

        while low < high:
            k = (low + high + 1) // 2
            # The k smallest mochi are tops, and the k largest are bottoms.
            # Every top must reach the corresponding bottom.
            required = m - k
            if range_max(l, l + k) <= required:
                low = k
            else:
                high = k - 1

        answers.append(str(low))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()