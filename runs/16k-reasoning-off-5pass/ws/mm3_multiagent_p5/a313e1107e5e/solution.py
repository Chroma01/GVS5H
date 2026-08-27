import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    Q = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    queries = []
    for idx in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((X, R, idx))
    # coordinate compression of A values
    vals = sorted(set(A[1:]))
    comp = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed
    M = len(vals)
    # positions sorted by A[i]
    sorted_pos = sorted(range(1, N + 1), key=lambda i: A[i])
    # sort queries by X ascending
    queries.sort()
    class BIT:
        __slots__ = ('n', 'tree')
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        def update(self, idx, val):
            n = self.n
            tree = self.tree
            while idx <= n:
                if val > tree[idx]:
                    tree[idx] = val
                else:
                    # early break if current node already has larger value
                    # but we must still go up to cover larger ranges? Actually if current node already has val > new val,
                    # its ancestors may also have larger values, but we still need to propagate because they might have smaller.
                    # Standard BIT update for max doesn't need to propagate if no change.
                    # So we can break early to save time.
                    return
                idx += idx & -idx
        def query(self, idx):
            res = 0
            tree = self.tree
            while idx > 0:
                if tree[idx] > res:
                    res = tree[idx]
                idx -= idx & -idx
            return res
    bit_val = BIT(M)   # over values
    bit_pos = BIT(N)   # over positions
    ans = [0] * Q
    p = 0  # pointer in sorted_pos
    for X, R, qid in queries:
        # activate all positions with A[i] <= X
        while p < N and A[sorted_pos[p]] <= X:
            i = sorted_pos[p]
            v = comp[A[i]]
            best = bit_val.query(v - 1)
            dp = best + 1
            bit_val.update(v, dp)
            bit_pos.update(i, dp)
            p += 1
        ans[qid] = bit_pos.query(R)
    out = '\n'.join(map(str, ans))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()