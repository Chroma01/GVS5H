import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    del data

    def feasible(k, a=a, n=n):
        j = n - k
        for i in range(k):
            if a[i] * 2 > a[j + i]:
                return False
        return True

    low = 0
    high = n // 2 + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)

if __name__ == "__main__":
    main()