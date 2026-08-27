import sys


def fwht(a):
    n = len(a)
    length = 1
    while length < n:
        step = length << 1
        for start in range(0, n, step):
            mid = start + length
            end = start + step
            for i in range(start, mid):
                x = a[i]
                y = a[i + length]
                a[i] = x + y
                a[i + length] = x - y
        length = step


def main():
    input = sys.stdin.buffer.readline
    h, w = map(int, input().split())
    n = 1 << w

    freq = [0] * n
    for _ in range(h):
        row = input().strip()
        mask = int(row, 2)
        freq[mask] += 1

    cost = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        cost[mask] = min(ones, w - ones)

    fwht(freq)
    fwht(cost)

    for i in range(n):
        freq[i] *= cost[i]

    fwht(freq)

    ans = min(x // n for x in freq)
    print(ans)


if __name__ == "__main__":
    main()