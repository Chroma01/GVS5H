import sys


def feasible(x, y, k):
    """Check reachability using at most k operations."""
    n = len(x)
    m = len(y)
    left = 0

    for j in range(m):
        if left >= n:
            return False

        low = y[j] - k
        high = y[j] + k

        # The first source assigned to this target must be reachable.
        if x[left] < low or x[left] > high:
            return False

        # The last target receives all remaining sources.
        if j == m - 1:
            return x[-1] <= high

        next_low = y[j + 1] - k
        next_high = y[j + 1] + k
        target_gap = y[j + 1] - y[j]

        right = left

        while right + 1 < n:
            nxt = x[right + 1]

            # The next group must start at a source reachable by the next
            # target. Since sources are ordered, going farther cannot help
            # once nxt is already too large.
            if nxt > next_high:
                return False

            if nxt < next_low:
                # This source cannot start the next group, so it must belong
                # to the current group.
                right += 1
                if x[right] > high:
                    return False
                continue

            # Across two consecutive groups, displacements must be
            # nonincreasing:
            # y[j] - x[right] >= y[j+1] - x[right+1].
            if nxt - x[right] >= target_gap:
                break

            # This boundary is invalid. Absorb the next source into the
            # current group and try a later boundary.
            right += 1
            if x[right] > high:
                return False

        if right + 1 >= n:
            return False

        left = right + 1

    return left == n


def solve_case(a, b):
    x = [i for i, c in enumerate(a) if c == "1"]
    y = [i for i, c in enumerate(b) if c == "1"]

    if len(x) < len(y):
        return -1

    lo, hi = -1, len(a)

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(x, y, mid):
            hi = mid
        else:
            lo = mid

    return hi


def main():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        input()  # N
        a = input().strip()
        b = input().strip()
        out.append(str(solve_case(a, b)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()