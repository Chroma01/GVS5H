import sys


def possible(a, b, limit):
    """Check whether a contraction mapping with bottleneck limit exists."""
    targets = [i for i, c in enumerate(b) if c == "1"]
    k = len(targets)

    last = -1
    prev_delta = -10**18

    for x, c in enumerate(a):
        if c != "1":
            continue

        advanced = False

        # Prefer advancing to the next target: this gives the smallest
        # displacement delta = source - target and is never worse later.
        if last + 1 < k:
            y = targets[last + 1]
            delta = x - y
            if abs(delta) <= limit and delta >= prev_delta:
                last += 1
                prev_delta = delta
                advanced = True

        if not advanced:
            # Otherwise this source must merge into the last target.
            if last < 0:
                return False
            y = targets[last]
            delta = x - y
            if abs(delta) > limit or delta < prev_delta:
                return False
            prev_delta = delta

    return last == k - 1


def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()

        source_count = a.count("1")
        target_count = b.count("1")

        if source_count < target_count:
            out.append("-1")
            continue

        lo, hi = 0, n - 1
        if not possible(a, b, hi):
            out.append("-1")
            continue

        while lo < hi:
            mid = (lo + hi) // 2
            if possible(a, b, mid):
                hi = mid
            else:
                lo = mid + 1

        out.append(str(lo))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()