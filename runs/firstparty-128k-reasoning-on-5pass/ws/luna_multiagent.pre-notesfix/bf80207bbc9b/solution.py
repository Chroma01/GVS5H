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
        length <<= 1


def solve():
    input = sys.stdin.buffer.readline
    H, W = map(int, input().split())

    size = 1 << W
    freq = [0] * size

    for _ in range(H):
        mask = int(input().strip(), 2)
        freq[mask] += 1

    kernel = [0] * size
    for mask in range(size):
        ones = mask.bit_count()
        kernel[mask] = min(ones, W - ones)

    fwht(freq)
    fwht(kernel)

    for i in range(size):
        freq[i] *= kernel[i]

    fwht(freq)

    answer = min(value // size for value in freq)
    print(answer)


if __name__ == "__main__":
    solve()