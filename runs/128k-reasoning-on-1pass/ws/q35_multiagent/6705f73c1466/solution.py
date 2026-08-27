import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    S = input_data[1]
    
    # Collect 0-based indices of all '1's
    ones_indices = [i for i, c in enumerate(S) if c == '1']
    k = len(ones_indices)
    
    # We want to move the 1s to a contiguous block of length k.
    # Let the starting position of the target block be x.
    # The j-th 1 (0-indexed from left) should move to position x + j.
    # The total number of swaps (cost) is sum(|p_j - (x + j)|) for j in 0..k-1.
    # This can be rewritten as sum(|(p_j - j) - x|).
    # Let q_j = p_j - j. The problem reduces to finding an integer x that minimizes sum(|q_j - x|).
    # This is a classic problem where the optimal x is the median of the values q_j.
    # Since p_j are sorted indices, q_j is also non-decreasing.
    # Thus, the median is simply q_{k // 2}.
    
    median_idx = k // 2
    median_val = ones_indices[median_idx] - median_idx
    
    ans = 0
    for j, p in enumerate(ones_indices):
        ans += abs((p - j) - median_val)
        
    print(ans)

if __name__ == '__main__':
    solve()