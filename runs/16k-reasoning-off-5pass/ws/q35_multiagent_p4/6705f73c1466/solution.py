import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    # Find positions of all '1's
    ones_positions = [i for i, char in enumerate(S) if char == '1']
    k = len(ones_positions)
    
    if k <= 1:
        print(0)
        return
    
    # Compute q_i = p_i - i
    # p_i is the original position of the i-th '1'
    # We want to move them to l, l+1, ..., l+k-1
    # Cost = sum(|p_i - (l + i)|) = sum(|(p_i - i) - l|)
    q = [ones_positions[i] - i for i in range(k)]
    
    # Sort q to find the median
    q.sort()
    
    # The optimal l is the median of q
    # For even k, any value between q[k//2 - 1] and q[k//2] is optimal.
    # We can pick q[k//2] (upper median) or q[k//2 - 1] (lower median).
    # Let's pick the element at index k//2.
    median_val = q[k // 2]
    
    # Calculate the total cost
    cost = sum(abs(val - median_val) for val in q)
    
    print(cost)

if __name__ == '__main__':
    solve()