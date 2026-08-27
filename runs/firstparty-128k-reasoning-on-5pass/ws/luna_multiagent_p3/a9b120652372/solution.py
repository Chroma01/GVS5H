import sys


def solve_case(n, a, b):
    p = [i for i, c in enumerate(a) if c == "1"]
    q = [i for i, c in enumerate(b) if c == "1"]
    m = len(p)
    r = len(q)

    if m < r:
        return -1

    def feasible(k):
        lower = [0] * r
        upper = [0] * r

        lo = 0
        hi = -1

        for j, x in enumerate(q):
            left = x - k
            right = x + k

            while lo < m and p[lo] < left:
                lo += 1
            if lo == m:
                return False

            if hi < lo - 1:
                hi = lo - 1
            while hi + 1 < m and p[hi + 1] <= right:
                hi += 1

            lower[j] = lo
            upper[j] = hi

            if lo > hi:
                return False

        # The first target must receive the first piece.
        if lower[0] > 0 or upper[0] < 0:
            return False

        # reachable endpoints of the current target form an interval
        min_end = 0

        for j in range(r - 1):
            if min_end > upper[j]:
                return False

            required_gap = q[j + 1] - q[j]
            e = min_end

            # Find the first possible boundary whose source gap is
            # at least the corresponding target gap.
            while e < upper[j] and p[e + 1] - p[e] < required_gap:
                e += 1

            if e >= upper[j]:
                return False

            min_end = max(lower[j + 1], e + 1)
            if min_end > upper[j + 1]:
                return False

        return min_end <= m - 1 <= upper[-1]

    if not feasible(n):
        return -1

    low, high = -1, n
    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid
        else:
            low = mid

    return high


def main():
    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()
        ans.append(str(solve_case(n, a, b)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()