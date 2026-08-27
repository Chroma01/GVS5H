import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    # Find positions of all '1's (0-indexed)
    ones_positions = [i for i, c in enumerate(S) if c == '1']
    k = len(ones_positions)
    
    if k <= 1:
        print(0)
        return
    
    # Compute q_j = p_j - j for each j in 0..k-1
    q = [ones_positions[j] - j for j in range(k)]
    
    # Sort q to find the median
    q.sort()
    
    # The median minimizes the sum of absolute differences
    # For even k, any value between q[k//2 - 1] and q[k//2] works.
    # We can pick q[k//2] (upper median) or q[k//2 - 1] (lower median).
    # Let's pick the element at index k//2.
    median = q[k // 2]
    
    # Calculate total cost
    total_cost = sum(abs(q_j - median) for q_j in q)
    
    print(total_cost)

if __name__ == '__main__':
    solve()