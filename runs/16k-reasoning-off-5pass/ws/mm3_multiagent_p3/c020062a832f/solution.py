import sys
from sys import stdin, stdout

def solve():
    input = stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    
    # BIT implementation for 0-indexed values
    class BIT:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, idx, val):
            idx += 1  # convert to 1-indexed
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx
        def sum(self, idx):
            # sum from 0 to idx inclusive
            idx += 1
            s = 0
            while idx > 0:
                s += self.bit[idx]
                idx -= idx & -idx
            return s
    
    # 1. Compute inv_total (inversions in original sequence) using BIT over values
    bit_val = BIT(M)
    inv_total = 0
    for i in range(N):
        a = A[i]
        # Number of elements before i with value > a
        gt = i - bit_val.sum(a)
        inv_total += gt
        bit_val.add(a, 1)
    
    # 2. Count occurrences and positions of each value
    cnt = [0] * M
    pos = [[] for _ in range(M)]
    for i, a in enumerate(A):
        cnt[a] += 1
        pos[a].append(i)  # 0-indexed positions
    
    # 3. Prefix sums of counts: prefix[T] = number of elements with value < T
    prefix = [0] * (M + 1)
    for v in range(M):
        prefix[v+1] = prefix[v] + cnt[v]
    
    # 4. Compute H[T] for T=1..M
    H = [0] * (M + 1)  # H[0..M], H[M] = 0
    bit_pos = BIT(N)
    for v in range(M-1, -1, -1):
        total_low = prefix[v]
        delta = 0
        for i in pos[v]:
            high_before = bit_pos.sum(i)
            low_before = i - high_before
            low_after = total_low - low_before
            delta += low_after
        H[v] = H[v+1] + delta
        for i in pos[v]:
            bit_pos.add(i, 1)
    
    # 5. Compute answer for each k
    ans = []
    for k in range(M):
        T = M - k
        if T == 0:
            cnt_low = 0
            H_val = 0
        else:
            cnt_low = prefix[T]
            H_val = H[T]
        cnt_high = N - cnt_low
        ans.append(inv_total + cnt_low * cnt_high - 2 * H_val)
    
    stdout.write('\n'.join(map(str, ans)))

if __name__ == "__main__":
    solve()