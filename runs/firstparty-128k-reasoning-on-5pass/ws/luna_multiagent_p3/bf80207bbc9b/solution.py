import sys


def fwht(arr):
    n = len(arr)
    length = 1
    while length < n:
        step = length << 1
        for start in range(0, n, step):
            end = start + length
            for i in range(start, end):
                x = arr[i]
                y = arr[i + length]
                arr[i] = x + y
                arr[i + length] = x - y
        length <<= 1


def solve():
    input = sys.stdin.buffer.readline
    H, W = map(int, input().split())

    n = 1 << W
    frequency = [0] * n

    for _ in range(H):
        row = int(input().strip(), 2)
        frequency[row] += 1

    kernel = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        kernel[mask] = min(ones, W - ones)

    fwht(frequency)
    fwht(kernel)

    for i in range(n):
        frequency[i] *= kernel[i]

    fwht(frequency)

    answer = min(value // n for value in frequency)
    print(answer)


if __name__ == "__main__":
    solve()