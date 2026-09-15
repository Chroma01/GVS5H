import sys
from bisect import bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    Q = data[p + 1]
    p += 2

    A = data[p:p + N]
    p += N

    vals = sorted(set(A))
    comp = {v: i + 1 for i, v in enumerate(vals)}
    ranks = [comp[v] for v in A]
    del A, comp

    M = len(vals)

    # First Fenwick tree: compute dp[i] = LIS ending at i.
    bit = [0] * (M + 1)
    dp = [0] * N
    b = bit

    for idx in range(N):
        r = ranks[idx]

        # Query maximum dp among strictly smaller values.
        i = r - 1
        res = 0
        while i > 0:
            bv = b[i]
            if bv > res:
                res = bv
            i -= i & -i

        val = res + 1
        dp[idx] = val

        # Update this value rank.
        i = r
        while i <= M:
            if val > b[i]:
                b[i] = val
            i += i & -i

    # Read queries and precompute compressed upper bound for X.
    queries = [None] * Q
    br = bisect_right
    for qi in range(Q):
        R = data[p]
        X = data[p + 1]
        p += 2
        queries[qi] = (R, br(vals, X), qi)

    del data

    queries.sort()

    # Second Fenwick tree: sweep by R and answer prefix maxima by value.
    bit2 = [0] * (M + 1)
    b2 = bit2
    ans = [0] * Q
    cur = 0

    for R, rx, qi in queries:
        while cur < R:
            r = ranks[cur]
            val = dp[cur]

            i = r
            while i <= M:
                if val > b2[i]:
                    b2[i] = val
                i += i & -i

            cur += 1

        i = rx
        res = 0
        while i > 0:
            bv = b2[i]
            if bv > res:
                res = bv
            i -= i & -i

        ans[qi] = res

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()