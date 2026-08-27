import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [0] * (N + 1)  # 1-indexed
    for i in range(1, N + 1):
        P[i] = int(next(it))
    
    # Fenwick tree implementation
    size = N
    bit = [0] * (size + 1)
    
    # Initialize BIT with all 1's (all positions free)
    # Instead of doing N updates, we can directly fill: bit[i] = i & -i
    for i in range(1, size + 1):
        bit[i] = i & -i
    
    def update(idx, delta):
        while idx <= size:
            bit[idx] += delta
            idx += idx & -idx
    
    def find_kth(k):
        # Find smallest idx such that prefix sum >= k
        # Assumes 1 <= k <= total sum
        idx = 0
        bit_mask = 1 << (size.bit_length())
        while bit_mask:
            t = idx + bit_mask
            if t <= size and bit[t] < k:
                idx = t
                k -= bit[t]
            bit_mask >>= 1
        return idx + 1
    
    result = [0] * N
    for i in range(N, 0, -1):
        pos = find_kth(P[i])
        update(pos, -1)
        result[pos - 1] = i
    
    sys.stdout.write(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()