import sys


def fwht(a):
    n = len(a)
    length = 1
    while length < n:
        block = length << 1
        for start in range(0, n, block):
            mid = start + length
            end = start + block
            for i, j in zip(range(start, mid), range(mid, end)):
                x = a[i]
                y = a[j]
                a[i] = x + y
                a[j] = x - y
        length = block


def main():
    input = sys.stdin.buffer.readline
    h, w = map(int, input().split())

    n = 1 << w
    freq = [0] * n

    for _ in range(h):
        row = input().strip()
        freq[int(row, 2)] += 1

    kernel = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        kernel[mask] = min(ones, w - ones)

    fwht(freq)
    fwht(kernel)

    for i in range(n):
        freq[i] *= kernel[i]

    fwht(freq)

    ans = min(value // n for value in freq)
    print(ans)


if __name__ == "__main__":
    main()