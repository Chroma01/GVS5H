import sys


def fwt_xor(a):
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


def main():
    input = sys.stdin.buffer.readline
    h, w = map(int, input().split())

    n = 1 << w
    freq = [0] * n
    for _ in range(h):
        row = int(input().strip(), 2)
        freq[row] += 1

    cost = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        cost[mask] = min(ones, w - ones)

    fwt_xor(freq)
    fwt_xor(cost)

    for i in range(n):
        freq[i] *= cost[i]

    fwt_xor(freq)

    answer = min(value // n for value in freq)
    print(answer)


if __name__ == "__main__":
    main()