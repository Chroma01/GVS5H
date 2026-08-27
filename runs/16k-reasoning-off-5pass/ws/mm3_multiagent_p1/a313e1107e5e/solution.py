import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    queries = []
    xs = []
    for i in range(Q):
        R = int(next(it))
        X = int(next(it))
        queries.append((R, X, i))
        xs.append(X)
    
    # Coordinate compression
    all_vals = A + xs
    uniq = sorted(set(all_vals))
    M = len(uniq)
    
    def comp(v):
        return bisect.bisect_left(uniq, v) + 1  # 1-indexed
    
    # Fenwick tree for max
    bit = [0] * (M + 2)
    
    def update(idx, val):
        while idx <= M:
            if val > bit[idx]:
                bit[idx] = val
            else:
                # If current node already has >= val, no need to propagate further? 
                # Actually we still need to continue to update parents, but they might already have larger.
                # However, we can break early if bit[idx] >= val and we know parents are already >= bit[idx]?
                # Not safe without extra info. Just continue.
                pass
            idx += idx & -idx
    
    def query(idx):
        res = 0
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & -idx
        return res
    
    # Sort queries by R
    queries.sort()
    answers = [0] * Q
    qptr = 0
    nq = len(queries)
    
    for i in range(1, N + 1):
        a = A[i - 1]
        idx = comp(a)
        # strictly increasing: values < a
        best = query(idx - 1) + 1
        update(idx, best)
        
        # Answer queries with R == i
        while qptr < nq and queries[qptr][0] == i:
            R, X, qid = queries[qptr]
            # Find position of largest value <= X
            pos = bisect.bisect_right(uniq, X)
            if pos == 0:
                ans = 0
            else:
                ans = query(pos)
            answers[qid] = ans
            qptr += 1
    
    # Handle any queries with R == 0? Not possible since R >= 1.
    # But if some queries had R == 0 (not in constraints), they'd not be answered.
    # For safety, process remaining queries (should not happen)
    while qptr < nq:
        R, X, qid = queries[qptr]
        pos = bisect.bisect_right(uniq, X)
        if pos == 0:
            ans = 0
        else:
            ans = query(pos)
        answers[qid] = ans
        qptr += 1
    
    out = '\n'.join(map(str, answers))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()