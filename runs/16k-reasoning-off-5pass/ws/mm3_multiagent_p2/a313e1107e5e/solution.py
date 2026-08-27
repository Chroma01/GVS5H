import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    queries = []
    for idx in range(Q):
        R = int(next(it)) - 1  # zero-based
        X = int(next(it))
        queries.append((R, X, idx))

    # Coordinate compression
    # We need to compress A values and also map query X to largest compressed <= X
    # Get all values that appear in A and all X from queries
    vals = sorted(set(A))
    # Map each value to its index (0-based)
    comp = {v: i for i, v in enumerate(vals)}
    M = len(vals)

    # Precompute dp[i] using a temporary BIT (point max, prefix max)
    # BIT uses 1-based indexing internally
    class BITMax:
        __slots__ = ('n', 'tree')
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        def update(self, idx, val):
            # idx is 0-based; convert to 1-based
            i = idx + 1
            n = self.n
            tree = self.tree
            while i <= n:
                if val > tree[i]:
                    tree[i] = val
                i += i & -i
        def query(self, idx):
            # return max over [0, idx]; if idx < 0 return 0
            if idx < 0:
                return 0
            i = idx + 1
            res = 0
            tree = self.tree
            while i > 0:
                if tree[i] > res:
                    res = tree[i]
                i -= i & -i
            return res

    temp_bit = BITMax(M)
    dp = [0] * N
    for i, a in enumerate(A):
        c = comp[a]
        # query max for values < c
        best = temp_bit.query(c - 1)
        dp[i] = best + 1
        temp_bit.update(c, dp[i])

    # Process queries offline
    # Sort queries by R ascending
    queries_sorted = sorted(queries, key=lambda x: x[0])
    ans = [0] * Q

    main_bit = BITMax(M)
    cur_r = -1
    # We'll iterate over queries; for each, add positions up to its R
    for R, X, qid in queries_sorted:
        # Add positions from cur_r+1 to R inclusive
        while cur_r < R:
            cur_r += 1
            c = comp[A[cur_r]]
            main_bit.update(c, dp[cur_r])
        # Map X to compressed index
        # find largest value <= X
        idx = bisect.bisect_right(vals, X) - 1
        if idx < 0:
            ans[qid] = 0
        else:
            ans[qid] = main_bit.query(idx)

    # Output
    out_lines = '\n'.join(map(str, ans))
    sys.stdout.write(out_lines)

if __name__ == "__main__":
    solve()