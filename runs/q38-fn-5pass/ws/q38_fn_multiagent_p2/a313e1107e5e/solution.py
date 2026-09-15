import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    Q = int(next(it))

    A = [int(next(it)) for _ in range(N)]

    queries = []
    for idx in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, idx))

    queries.sort(key=lambda x: x[0])

    ans = [0] * Q
    tails = []
    r = 0

    for R, X, idx in queries:
        while r < R:
            v = A[r]
            pos = bisect_left(tails, v)
            if pos == len(tails):
                tails.append(v)
            else:
                tails[pos] = v
            r += 1

        ans[idx] = bisect_right(tails, X)

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    main()