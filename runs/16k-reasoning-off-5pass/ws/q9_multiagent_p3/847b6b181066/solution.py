import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse inputs
    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]

    # We need to check if smoke exists at (R, C) at time t (for t=1 to N).
    # Based on the problem logic:
    # Smoke at time t at (R, C) exists if there is some k in [0, t] such that:
    # (R, C) = PrefixSum[t] - PrefixSum[k]
    # where PrefixSum[t] is the cumulative displacement after t steps.
    # This rearranges to: PrefixSum[k] = PrefixSum[t] - (R, C).
    
    # We maintain a set of all PrefixSum[k] encountered so far (for k from 0 to t).
    # Initially at t=0, PrefixSum[0] = (0, 0).
    
    seen = set()
    seen.add((0, 0))
    
    curr_r, curr_c = 0, 0
    result = []
    
    # Directions mapping based on problem statement:
    # N: (r-1, c)
    # W: (r, c-1)
    # S: (r+1, c)
    # E: (r, c+1)
    
    for char in S:
        if char == 'N':
            curr_r -= 1
        elif char == 'W':
            curr_c -= 1
        elif char == 'S':
            curr_r += 1
        elif char == 'E':
            curr_c += 1
            
        # Current position is PrefixSum[t] where t is the current step index (1-based)
        # We need to check if (R, C) = PrefixSum[t] - PrefixSum[k]
        # => PrefixSum[k] = PrefixSum[t] - (R, C)
        
        target_r = curr_r - R
        target_c = curr_c - C
        
        if (target_r, target_c) in seen:
            result.append('1')
        else:
            result.append('0')
            
        # Add current position to seen set for future steps (k = t)
        seen.add((curr_r, curr_c))
        
    print("".join(result))

if __name__ == '__main__':
    solve()