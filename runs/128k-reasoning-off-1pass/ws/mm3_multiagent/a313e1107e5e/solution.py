import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    queries = []
    X_vals = []
    for idx in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, idx))
        X_vals.append(X)
    
    # Coordinate compression of all A values and X values
    all_vals = A + X_vals
    uniq = sorted(set(all_vals))
    comp = {v: i+1 for i, v in enumerate(uniq)}  # 1-based index for BIT
    m = len(uniq)
    
    # Map A and X queries
    A_comp = [comp[v] for v in A]
    queries_comp = []
    for R, X, idx in queries:
        queries_comp.append((R, comp[X], idx))
    
    # Sort queries by R
    queries_comp.sort(key=lambda x: x[0])
    
    # Fenwick tree for range max query, point update
    class BIT:
        __slots__ = ('n', 'tree')
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        def update(self, idx, val):
            # set tree[idx] = max(tree[idx], val)
            n = self.n
            tree = self.tree
            while idx <= n:
                if val > tree[idx]:
                    tree[idx] = val
                else:
                    # No need to propagate if current is already >= val
                    # But we cannot break early because higher nodes may need update
                    # Actually if tree[idx] >= val, ancestors (larger idx) are also >= val?
                    # Not necessarily. We must still propagate to be safe.
                    # So we always go up.
                    pass
                idx += idx & -idx
        def query(self, idx):
            # max over [1, idx]
            res = 0
            tree = self.tree
            while idx > 0:
                if tree[idx] > res:
                    res = tree[idx]
                idx -= idx & -idx
            return res
    
    bit = BIT(m)
    ans = [0] * Q
    q_ptr = 0
    num_q = Q
    
    for i in range(N):
        v = A_comp[i]
        # query strictly smaller values: v-1
        best = bit.query(v - 1)
        new_len = best + 1
        bit.update(v, new_len)
        
        # answer all queries with R == i+1
        while q_ptr < num_q and queries_comp[q_ptr][0] == i + 1:
            _, x_idx, qid = queries_comp[q_ptr]
            ans[qid] = bit.query(x_idx)
            q_ptr += 1
    
    # In case there are queries with R > N? (should not happen per constraints)
    # but just in case, we could answer them now, but they are already processed because
    # we looped up to N. However if some R values are missing from the loop, we'd need to
    # process them. Actually we processed i from 0 to N-1, covering R = 1..N.
    # So all queries should be answered.
    
    out = '\n'.join(map(str, ans))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()