import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))  # 1-indexed
    
    # Compute left[i] = distinct count in A[1..i]
    left = [0] * (N + 1)
    seen = [False] * (N + 1)
    cnt = 0
    for i in range(1, N + 1):
        if not seen[A[i]]:
            seen[A[i]] = True
            cnt += 1
        left[i] = cnt
    
    # Compute right[k] = distinct count in A[k..N] for k=1..N+1
    right = [0] * (N + 2)
    seen = [False] * (N + 1)
    cnt = 0
    for k in range(N, 0, -1):
        if not seen[A[k]]:
            seen[A[k]] = True
            cnt += 1
        right[k] = cnt
    right[N + 1] = 0
    
    # Build iterative segment tree with lazy propagation
    # We need indices 1..N-1 for i (end of first subarray)
    # Since i can be at most N-2 (because i < j <= N-1), we use size N+1 to be safe
    size = 1
    while size < N + 1:
        size <<= 1
    
    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    # Initialize with left[i] for i=1..N-2
    # We'll place values at positions i+size-1 for i=1..N-2
    for i in range(1, N - 1):
        pos = i + size - 1
        tree[pos] = left[i]
    for pos in range(size - 1, 0, -1):
        tree[pos] = max(tree[2 * pos], tree[2 * pos + 1])
    
    def range_add(l, r, v):
        if l > r:
            return
        l += size - 1
        r += size - 1
        l0, r0 = l, r
        while l <= r:
            if l % 2 == 1:
                tree[l] += v
                lazy[l] += v
                l += 1
            if r % 2 == 0:
                tree[r] += v
                lazy[r] += v
                r -= 1
            l //= 2
            r //= 2
        # Push updates back up
        for pos in [l0 // 2, r0 // 2]:
            while pos >= 1:
                tree[pos] = max(tree[2 * pos], tree[2 * pos + 1]) + lazy[pos]
                pos //= 2
    
    def range_max(l, r):
        if l > r:
            return -10**9
        l += size - 1
        r += size - 1
        res = -10**9
        while l <= r:
            if l % 2 == 1:
                res = max(res, tree[l])
                l += 1
            if r % 2 == 0:
                res = max(res, tree[r])
                r -= 1
            l //= 2
            r //= 2
        return res
    
    prev = [0] * (N + 1)
    ans = 0
    
    for j in range(2, N):
        p = prev[A[j]]
        l = max(1, p)
        r = j - 1
        if l <= r:
            range_add(l, r, 1)
        prev[A[j]] = j
        
        max_val = range_max(1, j - 1)
        candidate = max_val + right[j + 1]
        if candidate > ans:
            ans = candidate
    
    print(ans)

if __name__ == "__main__":
    solve()