import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    def feasible(k):
        # Pair the k smallest mochi as tops with the k largest mochi as bottoms.
        # Both groups are already in ascending order, so pair them index by index.
        bottom_start = n - k
        arr = a
        for i in range(k):
            x = arr[i]
            if x + x > arr[bottom_start + i]:
                return False
        return True

    lo = 0
    hi = n // 2 + 1  # exclusive upper bound

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)

if __name__ == "__main__":
    main()