import sys
from bisect import bisect_left, bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]
    A = data[2:2 + N]

    # queries_by_r[r] stores pairs as a flat list: [X, query_index, X, query_index, ...]
    queries_by_r = [[] for _ in range(N + 1)]
    p = 2 + N
    for idx in range(Q):
        R = data[p]
        X = data[p + 1]
        p += 2
        queries_by_r[R].append(X)
        queries_by_r[R].append(idx)

    del data

    ans = [0] * Q
    tails = []

    bl = bisect_left
    br = bisect_right

    for i, a in enumerate(A, 1):
        # Standard LIS tails update for strictly increasing subsequences.
        pos = bl(tails, a)
        if pos == len(tails):
            tails.append(a)
        else:
            tails[pos] = a

        qs = queries_by_r[i]
        if qs:
            for k in range(0, len(qs), 2):
                x = qs[k]
                idx = qs[k + 1]
                ans[idx] = br(tails, x)

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()