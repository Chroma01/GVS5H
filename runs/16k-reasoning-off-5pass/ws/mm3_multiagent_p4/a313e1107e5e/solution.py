import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    queries = []
    for idx in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, idx))
    
    # Coordinate compression
    vals = set(A)
    for _, X, _ in queries:
        vals.add(X)
    comp = {v: i+1 for i, v in enumerate(sorted(vals))}  # 1-indexed
    M = len(comp)
    
    # Fenwick tree for prefix max
    class Fenwick:
        __slots__ = ('n', 'bit')
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def update(self, i, val):
            # set position i to max(old, val)
            n = self.n
            bit = self.bit
            while i <= n:
                if val > bit[i]:
                    bit[i] = val
                else:
                    # Since bit[i] is already >= val, and due to monotonicity,
                    # we can break early? Not safe, because other positions in the
                    # range might need update. Continue normally.
                    pass
                i += i & -i
        def query(self, i):
            # max over [1..i]
            res = 0
            bit = self.bit
            while i > 0:
                if bit[i] > res:
                    res = bit[i]
                i -= i & -i
            return res
    
    ft = Fenwick(M)
    
    # sort queries by R
    queries.sort(key=lambda x: x[0])
    ans = [0] * Q
    
    q_ptr = 0
    for i, a in enumerate(A, start=1):
        pos = comp[a]
        # query max over values < a
        if pos > 1:
            best_prev = ft.query(pos - 1)
        else:
            best_prev = 0
        new_len = best_prev + 1
        ft.update(pos, new_len)
        
        # answer all queries with R == i
        while q_ptr < Q and queries[q_ptr][0] == i:
            _, X, idx = queries[q_ptr]
            x_pos = comp[X]
            # all values <= X correspond to positions 1..x_pos because of compression
            # but careful: compressed values are sorted, and X is one of them, so
            # all values <= X have compressed index <= x_pos.
            res = ft.query(x_pos)
            ans[idx] = res
            q_ptr += 1
    
    # In case there are queries with R > N? But constraint says R_i <= N, so not.
    
    out = '\n'.join(map(str, ans))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()