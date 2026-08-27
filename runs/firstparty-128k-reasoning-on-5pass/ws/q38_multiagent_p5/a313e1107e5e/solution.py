import sys
from bisect import bisect_left, bisect_right


def main():
    it = map(int, sys.stdin.buffer.read().split())
    try:
        N = next(it)
    except StopIteration:
        return
    Q = next(it)

    A = [next(it) for _ in range(N)]
    queries = [(next(it), next(it), i) for i in range(Q)]
    queries.sort()

    ans = [0] * Q
    tails = []
    p = 0

    bl = bisect_left
    br = bisect_right

    for r, a in enumerate(A, 1):
        pos = bl(tails, a)
        if pos == len(tails):
            tails.append(a)
        else:
            tails[pos] = a

        while p < Q and queries[p][0] == r:
            x = queries[p][1]
            idx = queries[p][2]
            ans[idx] = br(tails, x)
            p += 1

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()