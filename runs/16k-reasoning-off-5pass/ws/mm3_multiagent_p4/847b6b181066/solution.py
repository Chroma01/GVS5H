import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].strip()
    
    # Direction mapping
    dr = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
    dc = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
    
    # Prefix sums P[0] = (0,0)
    pr, pc = 0, 0
    # Set of prefix sums for generation times, initially contains (0,0)
    prefix_set = {(0, 0)}
    
    result = []
    for t in range(N):
        # Apply wind at time t+1 (1-indexed)
        ch = S[t]
        pr += dr[ch]
        pc += dc[ch]
        # Check if (R,C) is occupied: need P[t] - (R,C) in prefix_set
        if (pr - R, pc - C) in prefix_set:
            result.append('1')
        else:
            result.append('0')
        # Add current prefix to set if not present (refill happens)
        if (pr, pc) not in prefix_set:
            prefix_set.add((pr, pc))
            
    sys.stdout.write(''.join(result))

if __name__ == "__main__":
    solve()