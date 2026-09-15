import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    # Input is already in ascending order; sorting is harmless and safe.
    a.sort()

    def feasible(k):
        # Use the k smallest mochi as tops and the k largest as bottoms,
        # matched in sorted order: top i = a[i], bottom i = a[n-k+i].
        if k == 0:
            return True
        for i in range(k):
            if 2 * a[i] > a[n - k + i]:
                return False
        return True

    lo, hi = 0, n // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    sys.stdout.write(str(lo) + "\n")


main()