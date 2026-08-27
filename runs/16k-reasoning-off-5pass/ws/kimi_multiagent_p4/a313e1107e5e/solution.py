import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    q = int(next(it))
    A = [int(next(it)) for _ in range(n)]

    # Coordinate compress A values
    vals = sorted(set(A))
    comp = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed
    m = len(vals)

    # Fenwick tree for prefix maximum
    bit = [0] * (m + 1)

    def bit_query(i):
        r = 0
        while i > 0:
            if bit[i] > r:
                r = bit[i]
            i -= i & (-i)
        return r

    def bit_update(i, v):
        while i <= m:
            if v > bit[i]:
                bit[i] = v
            i += i & (-i)

    queries = []
    for qi in range(q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, qi))

    # Sort queries by R
    queries.sort(key=lambda t: t[0])

    ans = [0] * q
    pos = 0  # number of elements inserted (positions 1..pos)
    for R, X, qi in queries:
        while pos < R:
            v = A[pos]
            idx = comp[v]
            dp = bit_query(idx - 1) + 1  # strictly smaller values only
            bit_update(idx, dp)
            pos += 1
        # number of compressed values <= X
        k = bisect_right(vals, X)
        ans[qi] = bit_query(k)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()