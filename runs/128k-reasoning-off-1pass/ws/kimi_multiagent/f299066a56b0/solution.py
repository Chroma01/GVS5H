import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    def feasible(k):
        # Pair the k smallest mochi (tops) with the k largest (bottoms).
        # i-th smallest top with i-th smallest of the k largest bottoms.
        base = n - k
        for i in range(k):
            if 2 * a[i] > a[base + i]:
                return False
        return True

    lo, hi = 0, n // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)

main()