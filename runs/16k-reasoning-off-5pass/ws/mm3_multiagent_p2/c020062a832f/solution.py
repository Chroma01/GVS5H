import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Compute inv(0) using BIT
    size = M
    bit = [0] * (size + 1)
    def update(i):
        while i <= size:
            bit[i] += 1
            i += i & -i
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    
    inv0 = 0
    for idx, val in enumerate(A):
        # number of elements > val seen so far
        inv0 += idx - query(val + 1)
        update(val + 1)
    
    # Precompute positions for each value
    pos = [[] for _ in range(M)]
    for i, v in enumerate(A, 1):
        pos[v].append(i)
    
    # Precompute change[v] for each value v
    change = [0] * M
    for v in range(M):
        positions = pos[v]
        c = len(positions)
        if c == 0:
            continue
        prefix = 0
        total = 0
        for p in positions:
            # 2*p - N - 2 + c - 2*prefix
            total += 2 * p - N - 2 + c - 2 * prefix
            prefix += 1
        change[v] = total
    
    # Compute ans for all k
    ans = [0] * M
    ans[0] = inv0
    for k in range(1, M):
        v = (M - k) % M
        ans[k] = ans[k-1] + change[v]
    
    print('\n'.join(map(str, ans)))

solve()