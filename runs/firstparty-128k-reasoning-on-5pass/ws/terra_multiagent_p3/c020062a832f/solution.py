import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = data[2:]

    count = [0] * m
    pos_sum = [0] * m

    bit = [0] * (m + 1)

    def add(i):
        while i <= m:
            bit[i] += 1
            i += i & -i

    def prefix_sum(i):
        result = 0
        while i > 0:
            result += bit[i]
            i -= i & -i
        return result

    inversions = 0
    seen = 0

    for position, value in enumerate(a, 1):
        index = value + 1
        inversions += seen - prefix_sum(index)
        add(index)
        seen += 1

        count[value] += 1
        pos_sum[value] += position

    answer = []
    current = inversions

    for k in range(m):
        answer.append(str(current))

        if k + 1 < m:
            value = m - 1 - k
            current += 2 * pos_sum[value] - count[value] * (n + 1)

    sys.stdout.write("\n".join(answer))


if __name__ == "__main__":
    main()