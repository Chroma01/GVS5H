import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    iterator = iter(input_data)
    N = int(next(iterator))
    M = int(next(iterator))
    A = [int(next(iterator)) for _ in range(N)]
    
    # Precompute positions for each value
    # pos[v] stores the list of 1-based indices where A[i] == v
    pos = [[] for _ in range(M)]
    for i, x in enumerate(A):
        pos[x].append(i + 1)
        
    # Fenwick Tree (Binary Indexed Tree)
    bit = [0] * (M + 1)
    
    def update(i, delta):
        while i <= M:
            bit[i] += delta
            i += i & (-i)
            
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
        
    # Compute initial inversion count for k=0
    inv = 0
    for i, x in enumerate(A):
        idx = x + 1  # 1-based index for BIT
        # Count elements greater than x that have appeared so far
        inv += i - query(idx)
        update(idx, 1)
        
    results = []
    current_inv = inv
    
    # Iterate k from 0 to M-1
    # For each k, output current_inv, then update for k+1
    for k in range(M):
        results.append(str(current_inv))
        
        # Elements wrapping around are those with value M-1-k
        val = M - 1 - k
        indices = pos[val]
        cnt = len(indices)
        if cnt > 0:
            # Calculate S = sum(pos_x - x) for x=1..cnt
            # indices are already sorted in increasing order
            S = sum(indices) - cnt * (cnt + 1) // 2
            # Net change in inversion count
            # Gain from pairs (j, i) with j < i where B_i wraps to 0
            # Loss from pairs (i, j) with i < j where B_i wraps to 0
            change = 2 * S - cnt * (N - cnt)
            current_inv += change
            
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()