import sys
from bisect import bisect_left, bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, q = data[0], data[1]
    a = data[2:2 + n]

    queries = []
    pos = 2 + n
    for i in range(q):
        r = data[pos]
        x = data[pos + 1]
        pos += 2
        queries.append((r, x, i))

    queries.sort()
    answers = [0] * q
    tails = []
    current_r = 0

    for r, x, index in queries:
        while current_r < r:
            value = a[current_r]
            p = bisect_left(tails, value)
            if p == len(tails):
                tails.append(value)
            else:
                tails[p] = value
            current_r += 1

        answers[index] = bisect_right(tails, x)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()