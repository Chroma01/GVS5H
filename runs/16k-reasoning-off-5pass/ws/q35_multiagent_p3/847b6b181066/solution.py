import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]
    
    # Current position in the reverse trace, starting at (R, C) at time t+0.5
    curr_r, curr_c = R, C
    
    # Set of visited positions in the reverse trace (at times t-0.5, t-1.5, ..., 0.5)
    visited = set()
    
    result = []
    
    for i in range(N):
        wind = S[i]
        
        # Apply inverse wind move to get the position at time (i)-0.5
        # Wind N: moves r-1, so reverse is r+1
        # Wind S: moves r+1, so reverse is r-1
        # Wind E: moves c+1, so reverse is c-1
        # Wind W: moves c-1, so reverse is c+1
        
        if wind == 'N':
            curr_r += 1
        elif wind == 'S':
            curr_r -= 1
        elif wind == 'E':
            curr_c -= 1
        elif wind == 'W':
            curr_c += 1
            
        visited.add((curr_r, curr_c))
        
        if (0, 0) in visited:
            result.append('1')
        else:
            result.append('0')
            
    print(''.join(result))

if __name__ == '__main__':
    solve()