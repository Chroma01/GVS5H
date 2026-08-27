import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    A = [int(data[pos + i]) for i in range(N)]
    pos += N
    queries = []
    xs = []
    for qi in range(Q):
        R = int(data[pos]); X = int(data[pos + 1]); pos += 2
        queries.append((R, X, qi))
        xs.append(X)

    # Coordinate compress A values only; map X via bisect_right.
    comp = sorted(set(A))
    a_idx = [bisect_right(comp, v) for v in A]  # 1-based positions

    # BIT for prefix maximum
    bit = [0] * (len(comp) + 2)

    def bit_update(i, val):
        while i < len(bit):
            if val > bit[i]:
                bit[i] = val
            i += i & (-i)

    def bit_query(i):
        res = 0
        while i > 0:
            if bit[i] > res:
                res = bit[i]
            i -= i & (-i)
        return res

    # Sort queries by R
    order = sorted(queries, key=lambda t: t[0])
    ans = [0] * Q
    i = 0  # how many elements inserted (prefix length)
    for R, X, qi in order:
        while i < R:
            v = a_idx[i]
            # dp = 1 + max dp over strictly smaller values among earlier indices
            dp = bit_query(v - 1) + 1
            bit_update(v, dp)
            i += 1
        # answer: max dp over values <= X
        xi = bisect_right(comp, X)
        ans[qi] = bit_query(xi)

    out = "\n".join(map(str, ans))
    sys.stdout.write(out + "\n")

main()