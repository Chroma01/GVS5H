import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    
    if n <= 1:
        print(0)
        return
    
    # Build iterative segment tree for range argmax
    # Tree size: next power of 2
    size = 1
    while size < n:
        size <<= 1
    # Each node stores (value, index) ; index = -1 means -infinity
    tree = [(-1, -1)] * (2 * size)
    for i in range(n):
        tree[size + i] = (A[i], i)
    for i in range(size - 1, 0, -1):
        left = tree[2 * i]
        right = tree[2 * i + 1]
        tree[i] = left if left[0] >= right[0] else right
    
    def query_max(l, r):
        """Return (value, index) of max in A[l..r] inclusive (0-indexed)."""
        l += size
        r += size
        best_val = -1
        best_idx = -1
        while l <= r:
            if l % 2 == 1:
                if tree[l][0] > best_val:
                    best_val = tree[l][0]
                    best_idx = tree[l][1]
                l += 1
            if r % 2 == 0:
                if tree[r][0] > best_val:
                    best_val = tree[r][0]
                    best_idx = tree[r][1]
                r -= 1
            l //= 2
            r //= 2
        return (best_val, best_idx)
    
    NEG_INF = -10**18  # safely below any A_i
    
    def solve_range(l, r):
        """
        Return (best_score, max_value) for subarray A[l..r] inclusive.
        If l > r, returns (0, NEG_INF).
        """
        if l > r:
            return (0, NEG_INF)
        if l == r:
            return (0, A[l])
        val, m = query_max(l, r)
        left_best, left_mx = solve_range(l, m - 1)
        right_best, right_mx = solve_range(m + 1, r)
        # match element m with the best partner on either side
        partner_mx = left_mx if left_mx >= right_mx else right_mx
        extra = val - partner_mx
        if extra < 0:
            extra = 0
        best = left_best + right_best + extra
        return (best, val)
    
    ans, _ = solve_range(0, n - 1)
    print(ans)

if __name__ == "__main__":
    solve()