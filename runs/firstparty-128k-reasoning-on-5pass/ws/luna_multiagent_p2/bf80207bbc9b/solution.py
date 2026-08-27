import sys


def fwht(a):
    n = len(a)
    length = 1
    while length < n:
        step = length << 1
        for start in range(0, n, step):
            end = start + length
            for i in range(start, end):
                x = a[i]
                y = a[i + length]
                a[i] = x + y
                a[i + length] = x - y
        length = step


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    h = int(data[0])
    w = int(data[1])
    n = 1 << w

    freq = [0] * n
    for s in data[2:2 + h]:
        freq[int(s, 2)] += 1

    kernel = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        kernel[mask] = min(ones, w - ones)

    fwht(freq)
    fwht(kernel)

    for i in range(n):
        freq[i] *= kernel[i]

    fwht(freq)

    answer = min(value // n for value in freq)
    print(answer)


if __name__ == "__main__":
    solve()