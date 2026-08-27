import sys


def fwht(a):
    n = len(a)
    step = 1
    while step < n:
        jump = step << 1
        for start in range(0, n, jump):
            end = start + step
            for i in range(start, end):
                x = a[i]
                y = a[i + step]
                a[i] = x + y
                a[i + step] = x - y
        step = jump


def main():
    input = sys.stdin.buffer.readline
    H, W = map(int, input().split())

    size = 1 << W
    frequency = [0] * size

    for _ in range(H):
        row = input().strip()
        mask = 0
        for bit in row:
            mask = (mask << 1) | (bit - 48)
        frequency[mask] += 1

    kernel = [0] * size
    for mask in range(size):
        ones = mask.bit_count()
        kernel[mask] = min(ones, W - ones)

    fwht(frequency)
    fwht(kernel)

    for i in range(size):
        frequency[i] *= kernel[i]

    fwht(frequency)

    divisor = size
    answer = min(value // divisor for value in frequency)
    print(answer)


if __name__ == "__main__":
    main()