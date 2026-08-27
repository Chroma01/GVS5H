import sys
from bisect import bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    Q = data[1]

    A = data[2:2 + N]

    vals = sorted(set(A))
    comp = {v: i + 1 for i, v in enumerate(vals)}
    ranks = [comp[x] for x in A]
    m = len(vals)

    pos = 2 + N
    queries = []
    for idx in range(Q):
        R = data[pos]
        X = data[pos + 1]
        pos += 2
        k = bisect_right(vals, X)
        queries.append((R, k, idx))

    queries.sort()

    bit = [0] * (m + 1)
    ans = [0] * Q
    p = 0

    for R, k, idx in queries:
        while p < R:
            r = ranks[p]

            i = r - 1
            best = 0
            while i:
                bv = bit[i]
                if bv > best:
                    best = bv
                i -= i & -i
            best += 1

            i = r
            while i <= m:
                if best > bit[i]:
                    bit[i] = best
                i += i & -i

            p += 1

        i = k
        res = 0
        while i:
            bv = bit[i]
            if bv > res:
                res = bv
            i -= i & -i

        ans[idx] = res

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    main()