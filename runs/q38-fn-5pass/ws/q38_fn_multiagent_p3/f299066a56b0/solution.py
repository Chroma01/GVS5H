import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    def can(k: int) -> bool:
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

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid

    print(lo)

if __name__ == "__main__":
    main()