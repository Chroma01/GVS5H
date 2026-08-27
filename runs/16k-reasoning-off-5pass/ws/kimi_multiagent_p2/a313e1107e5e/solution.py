import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    A = [int(data[idx + i]) for i in range(N)]
    idx += N

    queries = []
    for i in range(Q):
        R = int(data[idx]); X = int(data[idx + 1]); idx += 2
        queries.append((R, X, i))

    # Coordinate compress array values
    vals = sorted(set(A))
    comp = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed
    M = len(vals)

    # Max Fenwick tree: point-max update, prefix-max query
    bit = [0] * (M + 1)

    def bit_update(i, v):
        while i <= M:
            if v > bit[i]:
                bit[i] = v
            else:
                # still need to continue? No: if v <= bit[i], ancestors may still
                # need update only if they don't already have >= v. But bit[i] >= v
                # doesn't imply ancestors >= v... actually ancestors cover i too,
                # and they were updated whenever a value at position in their range
                # was set. Since bit[i] >= v means some position in i's range has
                # value >= v, and that position is also in each ancestor's range,
                # ancestors already have >= v. So we can stop.
                return
            i += i & (-i)

    def bit_query(i):
        res = 0
        while i > 0:
            if bit[i] > res:
                res = bit[i]
            i -= i & (-i)
        return res

    # Sort queries by R
    queries.sort(key=lambda q: q[0])

    ans = [0] * Q
    p = 0  # number of elements of A processed (prefix length)
    for R, X, qi in queries:
        while p < R:
            a = A[p]
            c = comp[a]
            # best LIS ending at value a = 1 + best over values strictly < a
            best = bit_query(c - 1) + 1
            bit_update(c, best)
            p += 1
        # answer: max over values <= X
        k = bisect_right(vals, X)  # number of compressed values <= X
        ans[qi] = bit_query(k)

    out = sys.stdout
    out.write("\n".join(map(str, ans)) + "\n")

main()