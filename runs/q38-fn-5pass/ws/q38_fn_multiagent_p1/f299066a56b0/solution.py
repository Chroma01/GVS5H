import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    def feasible(k):
        if k == 0:
            return True
        offset = n - k
        arr = a
        for i in range(k):
            if arr[i] * 2 > arr[offset + i]:
                return False
        return True

    lo = 0
    hi = n // 2 + 1

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)

if __name__ == "__main__":
    main()