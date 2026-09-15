import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    q = int(data[pos]); pos += 1

    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[pos]); pos += 1

    # Bucket queries by their R value.
    queries_by_R = [[] for _ in range(n + 1)]
    for qi in range(q):
        r = int(data[pos]); pos += 1
        x = int(data[pos]); pos += 1
        queries_by_R[r].append((x, qi))

    # Coordinate-compress the values present in A.
    vals = sorted(set(A[1:]))
    M = len(vals)

    # Max-Fenwick tree over value-ranks (1-indexed).
    tree = [0] * (M + 1)

    ans = [0] * q

    for i in range(1, n + 1):
        rank = bisect_left(vals, A[i]) + 1  # 1-indexed rank of A[i]

        # dp[i] = 1 + max dp[j] over A_j < A_i  (ranks strictly less)
        j = rank - 1
        best = 0
        while j > 0:
            v = tree[j]
            if v > best:
                best = v
            j -= j & (-j)
        dpi = best + 1

        # Insert dp[i] at its value-rank.
        j = rank
        while j <= M:
            if tree[j] < dpi:
                tree[j] = dpi
            j += j & (-j)

        # Answer all queries with this R (dp[i] now included).
        if queries_by_R[i]:
            for x, qi in queries_by_R[i]:
                # largest index k with vals[k-1] <= x
                j = bisect_right(vals, x)
                best = 0
                while j > 0:
                    v = tree[j]
                    if v > best:
                        best = v
                    j -= j & (-j)
                ans[qi] = best

    sys.stdout.write('\n'.join(map(str, ans)))
    sys.stdout.write('\n')


main()