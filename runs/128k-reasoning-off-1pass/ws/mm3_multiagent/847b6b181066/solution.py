import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].strip()
    
    # Map directions to (dr, dc)
    # N: (-1, 0), W: (0, -1), S: (1, 0), E: (0, 1)
    move_map = {'N': (-1, 0), 'W': (0, -1), 'S': (1, 0), 'E': (0, 1)}
    
    # Set of visited prefix sums: using complex numbers for efficiency
    visited = {0}
    
    r, c = 0, 0
    res = []
    for ch in S:
        dr, dc = move_map[ch]
        r += dr
        c += dc
        # target is P[t] - (R, C)
        target_r = r - R
        target_c = c - C
        # Use complex number as key: target_r + target_c*j
        if (target_r + target_c * 1j) in visited:
            res.append('1')
        else:
            res.append('0')
        # Add current position to visited set for future checks
        visited.add(r + c * 1j)
    
    sys.stdout.write(''.join(res))

if __name__ == "__main__":
    solve()