import sys


def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for start in range(0, n, step):
            mid = start + h
            for i in range(start, mid):
                x = a[i]
                y = a[i + h]
                a[i] = x + y
                a[i + h] = x - y
        h = step


def main():
    data = sys.stdin.buffer.read().split()
    h = int(data[0])
    w = int(data[1])

    n = 1 << w
    freq = [0] * n

    for s in data[2:2 + h]:
        freq[int(s, 2)] += 1

    cost = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        cost[mask] = min(ones, w - ones)

    fwht(freq)
    fwht(cost)

    for i in range(n):
        freq[i] *= cost[i]

    fwht(freq)

    answer = min(value // n for value in freq)
    print(answer)


if __name__ == "__main__":
    main()