import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    def feasible(k):
        # Pair the k smallest (tops) with the k largest (bottoms), aligned.
        # Feasible iff every smallest top fits on the corresponding largest bottom.
        base = n - k
        for i in range(k):
            if a[i] * 2 > a[base + i]:
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