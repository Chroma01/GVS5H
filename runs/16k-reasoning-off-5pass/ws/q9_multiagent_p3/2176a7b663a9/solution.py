import sys
import bisect

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        W = []
        for _ in range(N):
            W.append(int(next(iterator)))
            
        L = []
        R = []
        for _ in range(N):
            L.append(int(next(iterator)))
            R.append(int(next(iterator)))
            
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            s = int(next(iterator))
            t = int(next(iterator))
            queries.append((s-1, t-1)) # 0-indexed
    except StopIteration:
        return

    # Coordinate compression for L and R values
    coords = set()
    for l, r in zip(L, R):
        coords.add(l)
        coords.add(r)
        coords.add(l-1)
        coords.add(r+1)
    
    sorted_coords = sorted(list(coords))
    coord_map = {val: i for i, val in enumerate(sorted_coords)}
    M = len(sorted_coords)
    
    # Segment Tree for Range Minimum Query
    class SegmentTree:
        def __init__(self, size, init_val):
            self.n = 1
            while self.n < size:
                self.n *= 2
            self.tree = [init_val] * (2 * self.n)
            
        def update(self, idx, val):
            idx += self.n
            self.tree[idx] = min(self.tree[idx], val)
            while idx > 1:
                idx //= 2
                self.tree[idx] = min(self.tree[2*idx], self.tree[2*idx+1])
                
        def query(self, l, r):
            if l > r:
                return float('inf')
            l += self.n
            r += self.n
            res = float('inf')
            while l <= r:
                if l % 2 == 1:
                    res = min(res, self.tree[l])
                    l += 1
                if r % 2 == 0:
                    res = min(res, self.tree[r])
                    r -= 1
                l //= 2
                r //= 2
            return res

    # Initialize Segment Trees for 1D queries
    st_l = SegmentTree(M, float('inf'))
    st_r = SegmentTree(M, float('inf'))
    
    for i in range(N):
        l_idx = coord_map[L[i]]
        r_idx = coord_map[R[i]]
        w = W[i]
        st_l.update(l_idx, w)
        st_r.update(r_idx, w)
        
    ans = [float('inf')] * Q
    
    # Helper to update ans
    def update_ans(idx, val):
        if val < ans[idx]:
            ans[idx] = val

    # Process Case 3: R[t] < L[s] (Gap between t and s)
    # We need k such that L[k] > R[t] and R[k] < L[s]
    case3_queries = []
    for i, (s, t) in enumerate(queries):
        if R[t] < L[s]:
            case3_queries.append((L[s], R[t], i))
    case3_queries.sort(key=lambda x: x[0])
    
    nodes_by_R = sorted(range(N), key=lambda i: R[i])
    st_case3 = SegmentTree(M, float('inf'))
    ptr = 0
    for l_s, r_t, q_idx in case3_queries:
        while ptr < N and R[nodes_by_R[ptr]] < l_s:
            k = nodes_by_R[ptr]
            l_idx = coord_map[L[k]]
            st_case3.update(l_idx, W[k])
            ptr += 1
        
        idx_start = bisect.bisect_right(sorted_coords, r_t)
        if idx_start < M:
            val = st_case3.query(idx_start, M-1)
            if val != float('inf'):
                update_ans(q_idx, val)
    
    # Process Case 4: R[s] < L[t] (Gap between s and t)
    # We need k such that L[k] > R[s] and R[k] < L[t]
    case4_queries = []
    for i, (s, t) in enumerate(queries):
        if R[s] < L[t]:
            case4_queries.append((L[t], R[s], i))
    case4_queries.sort(key=lambda x: x[0])
    
    ptr = 0
    st_case4 = SegmentTree(M, float('inf'))
    
    for l_t, r_s, q_idx in case4_queries:
        while ptr < N and R[nodes_by_R[ptr]] < l_t:
            k = nodes_by_R[ptr]
            l_idx = coord_map[L[k]]
            st_case4.update(l_idx, W[k])
            ptr += 1
        
        idx_start = bisect.bisect_right(sorted_coords, r_s)
        if idx_start < M:
            val = st_case4.query(idx_start, M-1)
            if val != float('inf'):
                update_ans(q_idx, val)
                
    # Process 1-hop and 2-hop (Left/Right Gaps)
    for i, (s, t) in enumerate(queries):
        # Check 1-hop
        if R[s] < L[t] or R[t] < L[s]:
            if ans[i] == float('inf'):
                ans[i] = W[s] + W[t]
            continue
            
        # Check 2-hop (Left Gap: R[k] < min(Ls, Lt))
        min_L = min(L[s], L[t])
        idx_limit = bisect.bisect_left(sorted_coords, min_L) - 1
        if idx_limit >= 0:
            val = st_r.query(0, idx_limit)
            if val != float('inf'):
                if ans[i] == float('inf') or W[s] + val + W[t] < ans[i]:
                    ans[i] = W[s] + val + W[t]
                    
        # Check 2-hop (Right Gap: L[k] > max(Rs, Rt))
        max_R = max(R[s], R[t])
        idx_start = bisect.bisect_right(sorted_coords, max_R)
        if idx_start < M:
            val = st_l.query(idx_start, M-1)
            if val != float('inf'):
                if ans[i] == float('inf') or W[s] + val + W[t] < ans[i]:
                    ans[i] = W[s] + val + W[t]
                    
    for res in ans:
        if res == float('inf'):
            print(-1)
        else:
            print(res)

if __name__ == '__main__':
    solve()