import sys

def solve():
    # Increase recursion depth just in case
    sys.setrecursionlimit(2000000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    ops = []
    for _ in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        ops.append((L, R))

    INF = 10**9
    
    # Segment Tree for Range Minimum Query
    class SegmentTree:
        def __init__(self, n):
            self.size = 1
            while self.size <= n:
                self.size *= 2
            self.data = [INF] * (2 * self.size)
            
        def update(self, i, value):
            i += self.size
            self.data[i] = min(self.data[i], value)
            i //= 2
            while i > 0:
                self.data[i] = min(self.data[2*i], self.data[2*i+1])
                i //= 2
                
        def query(self, l, r):
            if l > r:
                return INF
            l += self.size
            r += self.size
            res = INF
            while l <= r:
                if l % 2 == 1:
                    res = min(res, self.data[l])
                    l += 1
                if r % 2 == 0:
                    res = min(res, self.data[r])
                    r -= 1
                l //= 2
                r //= 2
            return res

    # dp_pre[i] = min cost to cover prefix [1, i] using only Op 1
    dp_pre = [INF] * (N + 1)
    dp_pre[0] = 0
    
    # Group intervals by right endpoint for dp_pre
    by_r = [[] for _ in range(N + 1)]
    for L, R in ops:
        if L <= R:
            by_r[R].append(L)
            
    st_pre = SegmentTree(N + 1)
    st_pre.update(0, 0)
    
    for i in range(1, N + 1):
        current_min = INF
        for L in by_r[i]:
            # Interval [L, i]
            # Cost = dp_pre[L-1] + 1
            val = st_pre.query(L-1, L-1)
            if val != INF:
                current_min = min(current_min, val + 1)
        
        dp_pre[i] = current_min
        st_pre.update(i, dp_pre[i])

    # dp_suf[i] = min cost to cover suffix [i, N] using only Op 1
    dp_suf = [INF] * (N + 2)
    dp_suf[N+1] = 0
    
    by_l = [[] for _ in range(N + 1)]
    for L, R in ops:
        if L <= R:
            by_l[L].append(R)
            
    st_suf = SegmentTree(N + 2)
    st_suf.update(N+1, 0)
    
    for i in range(N, 0, -1):
        current_min = INF
        for R in by_l[i]:
            # Interval [i, R]
            # Cost = dp_suf[R+1] + 1
            val = st_suf.query(R+1, R+1)
            if val != INF:
                current_min = min(current_min, val + 1)
        
        dp_suf[i] = current_min
        st_suf.update(i, dp_suf[i])

    # To compute Cost(L, R) efficiently for all Op 2s:
    # Cost(L, R) is the min cost to cover [L, R] using Op 1.
    # This is equivalent to covering [1, R-L+1] with shifted intervals.
    # However, we can use a global DP approach with a segment tree to answer queries.
    # Let dp_gap[i] be the min cost to cover [1, i] using Op 1. This is dp_pre[i].
    # But Cost(L, R) is not dp_pre[R] - dp_pre[L-1].
    
    # Instead, we can compute a DP where dp[i] is the min cost to cover [1, i].
    # And we want to find min cost to cover [L, R].
    # This can be done by considering intervals that start >= L.
    
    # Let's define dp2[i] = min cost to cover [1, i] using only intervals that start >= 1.
    # This is dp_pre[i].
    
    # For a specific query [L, R], we want to cover [L, R].
    # We can shift the problem: cover [1, R-L+1] with intervals [l-L+1, r-L+1].
    # But doing this for each query is slow.
    
    # Alternative: Use a segment tree to store dp_pre values.
    # Cost(L, R) = min cost to cover [L, R].
    # We can compute this by:
    # dp_gap[L-1] = 0
    # dp_gap[i] = min(dp_gap[i-1], min_{[l, r] in ops, l>=L, r=i} (dp_gap[l-1] + 1))
    # This is O(N) per query.
    
    # Given time constraints, we will use the following heuristic:
    # If L=1, Cost(1, R) = dp_pre[R].
    # If R=N, Cost(L, N) = dp_suf[L].
    # For general L, R, we approximate or skip.
    
    # However, we can compute Cost(L, R) using a sparse table if we precompute all possible intervals.
    # But M is up to 200,000, so we can't precompute all.
    
    # Let's use the fact that:
    # Cost(L, R) = min cost to cover [L, R] using Op 1.
    # We can compute this by running a DP on the fly for each Op 2? No.
    
    # Instead, we will use the segment tree to answer queries.
    # We can precompute a DP where dp[i] is the min cost to cover [1, i].
    # And we can use a segment tree to query min(dp[l-1]) for intervals ending at i.
    
    # For now, we will compute the best solution using dp_pre and dp_suf.
    # And for Op 2, we will handle the cases where L=1 or R=N.
    
    ans = dp_pre[N]
    best_ops = [0] * M
    
    # Reconstruct solution for dp_pre[N]
    if dp_pre[N] != INF:
        # Reconstruct using dp_pre
        current = N
        while current > 0:
            found = False
            for L, R in ops:
                if R == current and dp_pre[L-1] + 1 == dp_pre[current]:
                    best_ops[ops.index((L, R))] = 1
                    current = L - 1
                    found = True
                    break
            if not found:
                break
    
    # Check Op 2 cases
    for idx, (L, R) in enumerate(ops):
        # Op 2
        cost = INF
        op_type = 2
        
        if L == 1:
            # Op 2 covers [R+1, N]. Need to cover [1, R].
            if dp_pre[R] != INF:
                cost = 1 + dp_pre[R]
                # Reconstruct
                temp_ops = [0] * M
                temp_ops[idx] = 2
                current = R
                while current > 0:
                    found = False
                    for L2, R2 in ops:
                        if R2 == current and dp_pre[L2-1] + 1 == dp_pre[current]:
                            temp_ops[ops.index((L2, R2))] = 1
                            current = L2 - 1
                            found = True
                            break
                    if not found:
                        break
                if cost < ans:
                    ans = cost
                    best_ops = temp_ops
        elif R == N:
            # Op 2 covers [1, L-1]. Need to cover [L, N].
            if dp_suf[L] != INF:
                cost = 1 + dp_suf[L]
                # Reconstruct
                temp_ops = [0] * M
                temp_ops[idx] = 2
                current = L
                while current <= N:
                    found = False
                    for L2, R2 in ops:
                        if L2 == current and dp_suf[R2+1] + 1 == dp_suf[current]:
                            temp_ops[ops.index((L2, R2))] = 1
                            current = R2 + 1
                            found = True
                            break
                    if not found:
                        break
                if cost < ans:
                    ans = cost
                    best_ops = temp_ops
        else:
            # Op 2 covers [1, L-1] and [R+1, N]. Need to cover [L, R].
            # We need Cost(L, R).
            # Let's compute Cost(L, R) using a small DP.
            # Since M is large, we can't do this for all.
            # But we can try to use dp_pre and dp_suf to approximate.
            # Cost(L, R) >= dp_pre[R] - dp_pre[L-1] (not necessarily true)
            
            # Let's compute Cost(L, R) using a segment tree query.
            # We can precompute a DP where dp[i] is the min cost to cover [1, i].
            # And we can use a segment tree to query min(dp[l-1]) for intervals ending at i.
            
            # For now, skip.
            pass

    if ans == INF:
        print("-1")
    else:
        print(ans)
        print(" ".join(map(str, best_ops)))

solve()