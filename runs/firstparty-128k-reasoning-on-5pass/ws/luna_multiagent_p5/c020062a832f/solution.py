import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = data[2:]

    freq = [0] * m
    for x in a:
        freq[x] += 1

    bit = [0] * (m + 1)

    def add(index, value):
        index += 1
        while index <= m:
            bit[index] += value
            index += index & -index

    def prefix(index):
        total = 0
        index += 1
        while index > 0:
            total += bit[index]
            index -= index & -index
        return total

    inversions = 0
    seen = 0
    for x in a:
        inversions += seen - prefix(x)
        add(x, 1)
        seen += 1

    delta = [0] * m
    occurrence_rank = [0] * m

    for i, x in enumerate(a):
        rank = occurrence_rank[x]
        delta[x] += 2 * i - n + freq[x] - 2 * rank
        occurrence_rank[x] += 1

    answers = []
    current = inversions

    for k in range(m):
        answers.append(str(current))
        if k < m - 1:
            wrapping_value = m - 1 - k
            current += delta[wrapping_value]

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()