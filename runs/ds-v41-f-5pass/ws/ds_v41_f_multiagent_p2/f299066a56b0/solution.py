import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    def ok(k):
        # K smallest mochi are used as tops, K largest as bottoms.
        off = n - k
        for i in range(k):
            if a[i] * 2 > a[off + i]:
                return False
        return True

    lo, hi = 0, n // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)

if __name__ == "__main__":
    main()