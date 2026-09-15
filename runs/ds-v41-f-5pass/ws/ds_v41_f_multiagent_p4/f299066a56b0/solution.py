import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]

    def feasible(k):
        # Use the k smallest mochi as tops and the k largest as bottoms.
        # For sorted top sizes t_i and bottom sizes b_i, matching is possible
        # iff 2*t_i <= b_i for every i.
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

    print(lo)

if __name__ == "__main__":
    main()