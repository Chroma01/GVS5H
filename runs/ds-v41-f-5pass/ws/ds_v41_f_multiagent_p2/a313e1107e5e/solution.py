import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1

    A = [int(data[idx + i]) for i in range(N)]
    idx += N

    # coordinate compress A values
    sorted_vals = sorted(set(A))
    M = len(sorted_vals)
    rank_of = {v: i for i, v in enumerate(sorted_vals)}  # 0-indexed rank

    # group queries by R
    queries_by_R = [[] for _ in range(N + 1)]  # 1-indexed R
    answers = [0] * Q
    for qi in range(Q):
        R = int(data[idx]); idx += 1
        X = int(data[idx]); idx += 1
        # largest compressed rank (0-indexed) with value <= X
        qr = bisect_right(sorted_vals, X) - 1
        queries_by_R[R].append((qr, qi))

    # Fenwick tree for prefix maximum, 1-indexed
    tree = [0] * (M + 1)

    def update(i, v):
        while i <= M:
            if tree[i] < v:
                tree[i] = v
            i += i & (-i)

    def query(i):
        res = 0
        while i > 0:
            if tree[i] > res:
                res = tree[i]
            i -= i & (-i)
        return res

    for i in range(1, N + 1):
        r = rank_of[A[i - 1]]  # 0-indexed
        # prefix max over ranks strictly less than r => first r elements
        best = query(r)
        dp = best + 1
        update(r + 1, dp)

        if queries_by_R[i]:
            for qr, qi in queries_by_R[i]:
                # prefix max over ranks 0..qr => qr+1 elements
                answers[qi] = query(qr + 1)

    sys.stdout.write("\n".join(map(str, answers)) + "\n")

main()