import sys
from bisect import bisect_left, bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    q = next(it)

    a = [next(it) for _ in range(n)]

    queries = []
    for idx in range(q):
        r = next(it)
        x = next(it)
        queries.append((r, x, idx))

    queries.sort()

    tails = []
    answers = [0] * q
    pos = 0

    for r, x, idx in queries:
        while pos < r:
            value = a[pos]
            insert_pos = bisect_left(tails, value)
            if insert_pos == len(tails):
                tails.append(value)
            else:
                tails[insert_pos] = value
            pos += 1

        answers[idx] = bisect_right(tails, x)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()