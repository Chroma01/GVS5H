import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    A = [0] * N
    for i in range(N):
        A[i] = int(data[pos]); pos += 1

    # ---- Step 1: dp[j] = length of longest strictly increasing subsequence ending at j ----
    vals = sorted(set(A))
    M = len(vals)
    tree = [0] * (M + 1)          # max-Fenwick over compressed values (1-based)

    dp = [0] * N
    for j in range(N):
        r = bisect_left(vals, A[j]) + 1     # 1-based rank
        # prefix max over ranks <= r-1  (strictly smaller values)
        i = r - 1
        best = 0
        while i > 0:
            if tree[i] > best:
                best = tree[i]
            i -= i & (-i)
        d = best + 1
        dp[j] = d
        i = r
        while i <= M:
            if tree[i] < d:
                tree[i] = d
            i += i & (-i)

    # ---- Step 2: answer queries offline: max dp[j] for j <= R and A[j] <= X ----
    queries = []
    for qi in range(Q):
        R = int(data[pos]); pos += 1
        X = int(data[pos]); pos += 1
        queries.append((X, R, qi))
    queries.sort()

    order = sorted(range(N), key=lambda t: A[t])

    ftree = [0] * (N + 1)         # max-Fenwick over indices
    ans = [0] * Q
    p = 0
    for (X, R, qi) in queries:
        while p < N and A[order[p]] <= X:
            j = order[p]
            v = dp[j]
            i = j + 1
            while i <= N:
                if ftree[i] < v:
                    ftree[i] = v
                i += i & (-i)
            p += 1
        # prefix max over indices [1, R]
        i = R
        best = 0
        while i > 0:
            if ftree[i] > best:
                best = ftree[i]
            i -= i & (-i)
        ans[qi] = best

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()