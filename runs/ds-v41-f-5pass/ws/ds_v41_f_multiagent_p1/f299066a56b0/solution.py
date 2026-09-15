import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    def feasible(k):
        # tops = k smallest, bottoms = k largest; pair in sorted order
        for i in range(k):
            if a[i] * 2 > a[n - k + i]:
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