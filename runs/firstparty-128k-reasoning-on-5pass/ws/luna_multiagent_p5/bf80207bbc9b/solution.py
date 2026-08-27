import sys


def fwht(a):
    n = len(a)
    length = 1
    while length < n:
        step = length << 1
        for i in range(0, n, step):
            end = i + length
            for j in range(i, end):
                x = a[j]
                y = a[j + length]
                a[j] = x + y
                a[j + length] = x - y
        length <<= 1


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    h = int(data[0])
    w = int(data[1])
    n = 1 << w

    freq = [0] * n
    for i in range(h):
        mask = int(data[2 + i], 2)
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

    answer = min(value // n for value in freq)
    print(answer)


if __name__ == "__main__":
    main()