import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Compute inv(0) using BIT
    size = M + 2
    bit = [0] * size
    
    def update(i, v=1):
        i += 1
        while i < size:
            bit[i] += v
            i += i & -i
    
    def query(i):
        # sum of [0, i]
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    
    inv0 = 0
    for j in range(N - 1, -1, -1):
        a = A[j]
        # count of values < a seen so far
        inv0 += query(a - 1)
        update(a)
    
    # Compute freq and pos_sum (1-indexed positions)
    freq = [0] * M
    pos_sum = [0] * M
    for idx, a in enumerate(A, start=1):
        freq[a] += 1
        pos_sum[a] += idx
    
    # Output results
    out = []
    inv = inv0
    out.append(str(inv))
    for k in range(1, M):
        v = M - k
        inv += 2 * pos_sum[v] - freq[v] * (N + 1)
        out.append(str(inv))
    
    print('\n'.join(out))

solve()