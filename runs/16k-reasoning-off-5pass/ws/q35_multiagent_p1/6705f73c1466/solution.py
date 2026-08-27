import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # Find positions of all '1's (0-indexed)
    ones_positions = [i for i, char in enumerate(s) if char == '1']
    k = len(ones_positions)
    
    if k <= 1:
        print(0)
        return
    
    # Compute q_i = p_i - i for each 1
    # We want to find l that minimizes sum(|q_i - l|)
    # The optimal l is the median of q_i
    
    q = [ones_positions[i] - i for i in range(k)]
    
    # Sort q to find the median
    q.sort()
    
    # The median is q[k//2]
    median = q[k // 2]
    
    # Calculate the total cost
    cost = sum(abs(qi - median) for qi in q)
    
    print(cost)

if __name__ == '__main__':
    solve()