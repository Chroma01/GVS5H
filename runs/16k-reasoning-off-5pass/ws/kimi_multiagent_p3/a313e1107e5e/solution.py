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
    for i in range(Q):
        R = int(data[pos]); X = int(data[pos + 1]); pos += 2
        queries.append((R, X, i))
        xs.append(X)

    # Coordinate compress all A values and X thresholds
    all_vals = sorted(set(A) | set(xs))
    comp = {v: i + 1 for i, v in enumerate(all_vals)}  # 1-indexed
    size = len(all_vals)

    # Fenwick tree for prefix maximum
    bit = [0] * (size + 2)

    def bit_query(i):
        res = 0
        while i > 0:
            if bit[i] > res:
                res = bit[i]
            i -= i & (-i)
        return res

    def bit_update(i, val):
        while i <= size:
            if val > bit[i]:
                bit[i] = val
            i += i & (-i)

    # Sort queries by R
    queries.sort(key=lambda t: t[0])
    answers = [0] * Q

    qi = 0
    # Process positions 1..N, answering queries as their R is reached
    for p in range(1, N + 1):
        idx = comp[A[p - 1]]
        best = bit_query(idx - 1) + 1  # strictly increasing: values < A_p
        bit_update(idx, best)
        while qi < Q and queries[qi][0] == p:
            R, X, orig = queries[qi]
            k = bisect_right(all_vals, X)  # number of compressed values <= X
            answers[orig] = bit_query(k)
            qi += 1

    # Any remaining queries (R > N shouldn't happen, but handle gracefully)
    while qi < Q:
        R, X, orig = queries[qi]
        k = bisect_right(all_vals, X)
        answers[orig] = bit_query(k)
        qi += 1

    sys.stdout.write("\n".join(map(str, answers)) + "\n")

main()