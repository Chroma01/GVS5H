import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Frequency and position sum
    S = [0] * M
    pos_sum = [0] * M
    for idx, val in enumerate(A, 1):  # 1-based index
        S[val] += 1
        pos_sum[val] += idx
    
    # Precompute D[x] = delta[x] (change in inversion count when value x wraps)
    D = [0] * M
    for x in range(M):
        sx = S[x]
        if sx == 0:
            continue
        # P[x] = pos_sum[x] - sx - sx*(sx-1)//2
        P = pos_sum[x] - sx - sx * (sx - 1) // 2
        total_pairs = sx * (N - sx)
        Q = total_pairs - P
        D[x] = P - Q  # = 2*P - total_pairs
    
    # Compute ans0 (inversion count for k=0) using a Fenwick tree
    size = M + 2
    bit = [0] * size
    def bit_add(i, v):
        i += 1  # convert to 1-indexed
        while i < size:
            bit[i] += v
            i += i & -i
    def bit_sum(i):
        # sum of [0, i]
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    
    inv0 = 0
    seen = 0
    for val in A:
        le = bit_sum(val)  # number of previous elements <= val
        inv0 += seen - le  # those > val form inversions
        bit_add(val, 1)
        seen += 1
    
    # Build answer list
    ans = [inv0]
    cur = inv0
    for k in range(1, M):
        idx = (M - k) % M
        cur += D[idx]
        ans.append(cur)
    
    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

if __name__ == "__main__":
    solve()