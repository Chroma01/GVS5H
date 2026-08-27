import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Precompute frequency and sum of 0-indexed positions for each value
    freq = [0] * M
    sum_pos = [0] * M
    for i, v in enumerate(A):
        freq[v] += 1
        sum_pos[v] += i
    
    # Compute initial inversion count (k=0) using Fenwick tree
    bit = [0] * (M + 1)
    def update(idx):
        idx += 1
        while idx <= M:
            bit[idx] += 1
            idx += idx & -idx
    def query(idx):
        # prefix sum of [0, idx]
        idx += 1
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s
    
    inv = 0
    for i, v in enumerate(A):
        # number of previous elements with value > v
        inv += i - query(v)
        update(v)
    
    results = [inv]
    cur = inv
    
    # For each subsequent shift, update based on the value that becomes M-1
    for k in range(1, M):
        v = (M - 1 - (k - 1)) % M  # the value that equals M-1 at shift k-1
        m = freq[v]
        # L = number of pairs (i, j) with i < j, A_i = v, A_j != v
        L = m * (N - 1) - sum_pos[v] - m * (m - 1) // 2
        # delta = pairs where M-1 is the second element (gained) 
        #         minus pairs where M-1 is the first element (lost)
        delta = m * (N - m) - 2 * L
        cur += delta
        results.append(cur)
    
    sys.stdout.write('\n'.join(map(str, results)) + '\n')

solve()