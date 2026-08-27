import sys
import bisect
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

MOD = 998244353

def solve():
    H, W = map(int, input().split())
    A = []
    for _ in range(H):
        A.append(list(map(int, input().split())))
    Q, sh, sw = map(int, input().split())
    queries = []
    for _ in range(Q):
        d, a = input().split()
        a = int(a)
        queries.append((d, a))
    
    # Flatten grid by anti-diagonal order: increasing i+j, then increasing i
    cells = []  # list of (i, j)
    idx_of = {}  # (i,j) -> idx
    for s in range(2, H+W+1):
        for i in range(1, min(H, s-1)+1):
            j = s - i
            if 1 <= j <= W:
                idx = len(cells)
                cells.append((i, j))
                idx_of[(i,j)] = idx
    
    N = len(cells)
    up_idx = [0]*N
    left_idx = [0]*N
    for idx, (i,j) in enumerate(cells):
        if i > 1:
            up_idx[idx] = idx_of[(i-1, j)]
        else:
            up_idx[idx] = -1
        if j > 1:
            left_idx[idx] = idx_of[(i, j-1)]
        else:
            left_idx[idx] = -1
    
    A_flat = [0]*N
    for idx, (i,j) in enumerate(cells):
        A_flat[idx] = A[i-1][j-1]
    
    # Compute initial dp values
    dp = [0]*N
    for idx in range(N):
        if up_idx[idx] == -1 and left_idx[idx] == -1:
            dp[idx] = A_flat[idx] % MOD
        else:
            s = 0
            if up_idx[idx] != -1:
                s += dp[up_idx[idx]]
            if left_idx[idx] != -1:
                s += dp[left_idx[idx]]
            dp[idx] = (A_flat[idx] * s) % MOD
    
    # Segment tree for range updates
    size = 1
    while size < N:
        size *= 2
    seg = [0]*(2*size)
    
    for i in range(N):
        seg[size+i] = dp[i]
    for i in range(size-1, 0, -1):
        seg[i] = seg[2*i+1]
    
    def get_dp(idx):
        return seg[size+idx]
    
    def set_dp(idx, val):
        seg[size+idx] = val
        i = (size+idx) // 2
        while i:
            seg[i] = seg[2*i+1]
            i //= 2
    
    # Update range [L,R] given prev_dp (dp value of cell at L-1)
    def update_range(L, R, prev_dp):
        def _update(node, l, r, prev):
            if r < L or l > R:
                return prev
            if L <= l and r <= R:
                # Recompute dp for index r
                up = up_idx[r]
                up_dp = get_dp(up) if up != -1 else 0
                left_dp = prev
                s = up_dp + left_dp
                if s >= MOD:
                    s -= MOD
                new_dp = (A_flat[r] * s) % MOD
                seg[node] = new_dp
                seg[size+r] = new_dp
                return new_dp
            else:
                mid = (l+r)//2
                if L <= mid:
                    prev = _update(2*node, l, mid, prev)
                if R > mid:
                    prev = _update(2*node+1, mid+1, r, prev)
                seg[node] = seg[2*node+1]
                return prev
        _update(1, 0, size-1, prev_dp)
    
    # Precompute anti-diagonal indices
    diag_i_idx = {}
    for s in range(2, H+W+1):
        lst = []
        for idx, (i,j) in enumerate(cells):
            if i+j == s:
                lst.append((i, idx))
        if lst:
            diag_i_idx[s] = lst
    
    cur_h, cur_w = sh, sw
    out = []
    for d, a in queries:
        if d == 'L':
            cur_w -= 1
        elif d == 'R':
            cur_w += 1
        elif d == 'U':
            cur_h -= 1
        elif d == 'D':
            cur_h += 1
        x, y = cur_h, cur_w
        A[x-1][y-1] = a
        idx = idx_of[(x,y)]
        A_flat[idx] = a
        
        # Process affected anti-diagonals
        for s in range(x+y, H+W+1):
            if s not in diag_i_idx:
                continue
            lst = diag_i_idx[s]
            i_low = max(x, s-W)
            i_high = min(H, s-y)
            if i_low > i_high:
                continue
            left = bisect.bisect_left(lst, (i_low, -1))
            right = bisect.bisect_right(lst, (i_high, float('inf')))
            if left >= right:
                continue
            L_idx = lst[left][1]
            R_idx = lst[right-1][1]
            
            # Compute dp for L_idx
            up = up_idx[L_idx]
            left_n = left_idx[L_idx]
            up_dp = get_dp(up) if up != -1 else 0
            left_dp = get_dp(left_n) if left_n != -1 else 0
            s_val = up_dp + left_dp
            if s_val >= MOD:
                s_val -= MOD
            new_dp = (A_flat[L_idx] * s_val) % MOD
            set_dp(L_idx, new_dp)
            
            if L_idx < R_idx:
                update_range(L_idx+1, R_idx, new_dp)
        
        ans_idx = idx_of[(H,W)]
        ans = get_dp(ans_idx)
        out.append(ans)
    
    print('\n'.join(map(str, out)))

solve()