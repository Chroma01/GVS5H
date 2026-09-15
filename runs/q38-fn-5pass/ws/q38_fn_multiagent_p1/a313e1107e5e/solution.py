import sys
from bisect import bisect_left, bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    N = next(it)
    Q = next(it)

    A = [next(it) for _ in range(N)]

    queries = []
    for idx in range(Q):
        R = next(it)
        X = next(it)
        queries.append((R, X, idx))

    queries.sort(key=lambda t: t[0])

    ans = [0] * Q
    tails = []
    processed = 0

    for R, X, idx in queries:
        while processed < R:
            v = A[processed]
            pos = bisect_left(tails, v)
            if pos == len(tails):
                tails.append(v)
            else:
                tails[pos] = v
            processed += 1

        ans[idx] = bisect_right(tails, X)

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()